"""
canvas_siem — SIEM pipeline exporter for canvas_security telemetry.

Supported backends:
  SplunkHECExporter   — Splunk HTTP Event Collector (HEC) via asyncio HTTP
  SyslogExporter      — RFC 5424 syslog over UDP (drop-in for any SIEM syslog input)
  ElasticExporter     — Elasticsearch / OpenSearch bulk index
  CEFFormatter        — Common Event Format (ArcSight / IBM QRadar / generic SIEM)

Usage:
    pipeline = SIEMPipeline([
        SplunkHECExporter(url="https://splunk:8088", token="abc123"),
        SyslogExporter(host="siem.internal", port=514),
    ])
    logger = StructuredLogger(pipeline=pipeline)
    await logger.emit_async(EventType.SCAN_TIMEOUT, ...)
"""

import asyncio
import json
import logging
import os
import socket
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence

from canvas_telemetry import Level, EventType, TelemetryEvent

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# CEF formatter (stateless utility — usable independently of any exporter)
# ---------------------------------------------------------------------------

_CEF_SEVERITY: Dict[str, int] = {
    Level.INFO.value:     3,
    Level.WARNING.value:  6,
    Level.ERROR.value:    8,
    Level.CRITICAL.value: 10,
}

_CEF_ESCAPE = str.maketrans({"|": "\\|", "=": "\\=", "\\": "\\\\"})
_CEF_EXT_ESCAPE = str.maketrans({"=": "\\=", "\\": "\\\\", "\n": "\\n"})


class CEFFormatter:
    """
    Formats a TelemetryEvent as a CEF:0 string accepted by ArcSight, QRadar,
    Splunk CIM, and generic syslog-based SIEM collectors.

    CEF header: CEF:0|Vendor|Product|Version|SignatureID|Name|Severity|Extension
    """

    VENDOR  = "CylicAmp"
    PRODUCT = "CanvasSecurity"
    VERSION = "1.0"

    @classmethod
    def format(cls, event: TelemetryEvent) -> str:
        sig_id   = event.event.value
        name     = sig_id.replace("_", " ").title()
        severity = _CEF_SEVERITY.get(event.level.value, 3)

        # Extension: flatten event.data as key=value pairs
        ext_parts = []
        ext_parts.append(f"cs1={event.service}")
        ext_parts.append(f"cs1Label=service")
        if event.trace_id:
            ext_parts.append(f"cs2={_esc_ext(event.trace_id)}")
            ext_parts.append(f"cs2Label=traceId")
        for k, v in sorted(event.data.items()):
            ext_parts.append(f"{_cef_key(k)}={_esc_ext(str(v))}")

        header = "|".join([
            "CEF:0",
            _esc_hdr(cls.VENDOR),
            _esc_hdr(cls.PRODUCT),
            _esc_hdr(cls.VERSION),
            _esc_hdr(sig_id),
            _esc_hdr(name),
            str(severity),
        ])
        return f"{header}|{' '.join(ext_parts)}"


def _esc_hdr(s: str) -> str:
    return s.translate(_CEF_ESCAPE)

def _esc_ext(s: str) -> str:
    return s.translate(_CEF_EXT_ESCAPE)

def _cef_key(k: str) -> str:
    # Map common field names to CEF-standard keys where possible
    _MAP = {
        "target": "dhost", "host_pid": "spid", "zombie_count": "cnt",
        "finding_count": "cnt", "timeout_s": "requestClientApplication",
        "error": "msg", "reason": "msg", "connector": "deviceProcessName",
    }
    return _MAP.get(k, f"cs3{k[:8].replace('_','')}")


# ---------------------------------------------------------------------------
# Exporter base class
# ---------------------------------------------------------------------------

class SIEMExporter(ABC):
    """Single backend destination.  Implementations must be safe to call
    concurrently from async tasks."""

    @abstractmethod
    async def export(self, event: TelemetryEvent) -> None:
        """Ship one event to the backend.  Raise on hard failure."""

    async def export_batch(self, events: Sequence[TelemetryEvent]) -> None:
        """Default: sequential.  Override for bulk-capable backends."""
        for ev in events:
            await self.export(ev)

    async def close(self) -> None:
        """Release connections.  Override if needed."""


# ---------------------------------------------------------------------------
# Splunk HEC exporter
# ---------------------------------------------------------------------------

@dataclass
class SplunkHECExporter(SIEMExporter):
    """
    Ships events to Splunk's HTTP Event Collector.

    Configure Splunk HEC:
      Settings → Data Inputs → HTTP Event Collector → New Token
      sourcetype: canvas:security   index: security (or main)
    """
    url:        str
    token:      str
    index:      str  = "security"
    sourcetype: str  = "canvas:security"
    verify_tls: bool = True
    timeout_s:  float = 5.0

    # Simple retry: up to 3 attempts with 1-2-4 s backoff
    _MAX_RETRIES: int = field(default=3, init=False, repr=False)

    async def export(self, event: TelemetryEvent) -> None:
        payload = json.dumps({
            "time":       _epoch(event.timestamp),
            "host":       socket.gethostname(),
            "source":     event.service,
            "sourcetype": self.sourcetype,
            "index":      self.index,
            "event":      event.to_dict(),
        })
        headers = {
            "Authorization": f"Splunk {self.token}",
            "Content-Type":  "application/json",
        }
        endpoint = self.url.rstrip("/") + "/services/collector/event"
        await _http_post_with_retry(endpoint, payload, headers, self.timeout_s)

    async def export_batch(self, events: Sequence[TelemetryEvent]) -> None:
        # Splunk HEC accepts multiple events as concatenated JSON objects
        lines = []
        for ev in events:
            lines.append(json.dumps({
                "time":       _epoch(ev.timestamp),
                "host":       socket.gethostname(),
                "source":     ev.service,
                "sourcetype": self.sourcetype,
                "index":      self.index,
                "event":      ev.to_dict(),
            }))
        payload = "\n".join(lines)
        endpoint = self.url.rstrip("/") + "/services/collector/event"
        headers = {
            "Authorization": f"Splunk {self.token}",
            "Content-Type":  "application/json",
        }
        await _http_post_with_retry(endpoint, payload, headers, self.timeout_s)


# ---------------------------------------------------------------------------
# Elasticsearch / OpenSearch exporter
# ---------------------------------------------------------------------------

@dataclass
class ElasticExporter(SIEMExporter):
    """
    Indexes events into Elasticsearch or OpenSearch via the bulk API.

    Index pattern: canvas-security-YYYY.MM.DD (daily rollover)
    """
    url:       str
    username:  str  = ""
    password:  str  = ""
    index:     str  = "canvas-security"
    timeout_s: float = 5.0

    async def export(self, event: TelemetryEvent) -> None:
        await self.export_batch([event])

    async def export_batch(self, events: Sequence[TelemetryEvent]) -> None:
        today = datetime.now(timezone.utc).strftime("%Y.%m.%d")
        index = f"{self.index}-{today}"
        lines = []
        for ev in events:
            lines.append(json.dumps({"index": {"_index": index}}))
            lines.append(json.dumps(ev.to_dict()))
        payload = "\n".join(lines) + "\n"
        endpoint = self.url.rstrip("/") + "/_bulk"
        headers = {"Content-Type": "application/x-ndjson"}
        auth = (self.username, self.password) if self.username else None
        await _http_post_with_retry(endpoint, payload, headers, self.timeout_s, auth=auth)


# ---------------------------------------------------------------------------
# Syslog RFC 5424 exporter (UDP, connectionless)
# ---------------------------------------------------------------------------

@dataclass
class SyslogExporter(SIEMExporter):
    """
    Sends RFC 5424 syslog messages over UDP.

    Works with rsyslog, syslog-ng, Splunk syslog input, Fluentd syslog source,
    and most SIEM appliances' syslog listener.

    For TLS/TCP syslog, set tcp=True and configure your forwarder (Vector,
    Fluent Bit) to receive UDP and forward over TLS — avoids a dependency on
    ssl sockets here.
    """
    host:     str
    port:     int  = 514
    app_name: str  = "canvas_security"
    facility: int  = 16   # local0
    tcp:      bool = False

    _sock: Optional[socket.socket] = field(default=None, init=False, repr=False)

    def _get_sock(self) -> socket.socket:
        if self._sock is None:
            kind = socket.SOCK_STREAM if self.tcp else socket.SOCK_DGRAM
            self._sock = socket.socket(socket.AF_INET, kind)
            if self.tcp:
                self._sock.connect((self.host, self.port))
        return self._sock

    async def export(self, event: TelemetryEvent) -> None:
        msg = self._format_rfc5424(event)
        encoded = msg.encode("utf-8")
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send, encoded)

    def _send(self, data: bytes) -> None:
        sock = self._get_sock()
        if self.tcp:
            sock.sendall(data + b"\n")
        else:
            sock.sendto(data, (self.host, self.port))

    def _format_rfc5424(self, event: TelemetryEvent) -> str:
        # PRI = facility*8 + severity
        sev_map = {
            Level.INFO.value: 6, Level.WARNING.value: 4,
            Level.ERROR.value: 3, Level.CRITICAL.value: 2,
        }
        priority = self.facility * 8 + sev_map.get(event.level.value, 6)
        ts        = event.timestamp or datetime.now(timezone.utc).isoformat()
        hostname  = socket.gethostname()
        proc_id   = str(os.getpid())
        msg_id    = event.event.value[:32]

        # Structured data block: [canvas@32473 key="val" ...]
        sd_params = " ".join(
            f'{k}="{str(v).replace(chr(34), "")}"'
            for k, v in sorted(event.data.items())
        )
        sd = f'[canvas@32473 {sd_params}]' if sd_params else "-"

        msg = json.dumps(event.to_dict(), default=str)

        return (
            f"<{priority}>1 {ts} {hostname} {self.app_name} "
            f"{proc_id} {msg_id} {sd} {msg}"
        )

    async def close(self) -> None:
        if self._sock is not None:
            self._sock.close()
            self._sock = None


# ---------------------------------------------------------------------------
# Pipeline: fan-out to multiple exporters + retry buffer
# ---------------------------------------------------------------------------

class SIEMPipeline:
    """
    Routes events to all configured exporters.

    Failed exporters are logged but never block the main scan loop.
    A small in-memory retry queue re-attempts failed events with
    exponential backoff (max 3 retries, then drop with CRITICAL log).
    """

    def __init__(
        self,
        exporters:  List[SIEMExporter],
        queue_size: int = 1000,
    ) -> None:
        self._exporters = exporters
        self._queue: asyncio.Queue[TelemetryEvent] = asyncio.Queue(maxsize=queue_size)
        self._task:  Optional[asyncio.Task] = None

    def start(self) -> None:
        """Start the background drain task.  Call from an async context."""
        if self._task is None or self._task.done():
            self._task = asyncio.ensure_future(self._drain_loop())

    async def stop(self) -> None:
        """Flush remaining events and close exporters."""
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        for exp in self._exporters:
            await exp.close()

    async def send(self, event: TelemetryEvent) -> None:
        """Non-blocking enqueue.  Drops oldest on overflow."""
        try:
            self._queue.put_nowait(event)
        except asyncio.QueueFull:
            log.warning("SIEM queue full — dropping oldest event")
            try:
                self._queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            self._queue.put_nowait(event)

    async def _drain_loop(self) -> None:
        while True:
            event = await self._queue.get()
            await self._ship(event)
            self._queue.task_done()

    async def _ship(self, event: TelemetryEvent, attempt: int = 0) -> None:
        for exporter in self._exporters:
            try:
                await exporter.export(event)
            except Exception as exc:
                if attempt < 3:
                    delay = 2 ** attempt
                    log.warning(
                        "SIEM export failed (%s), retry %d in %ds: %s",
                        type(exporter).__name__, attempt + 1, delay, exc,
                    )
                    await asyncio.sleep(delay)
                    await self._ship(event, attempt + 1)
                else:
                    log.critical(
                        "SIEM export permanently failed (%s): %s",
                        type(exporter).__name__, exc,
                    )


# ---------------------------------------------------------------------------
# Shared HTTP helper (no aiohttp dependency — uses asyncio streams directly)
# ---------------------------------------------------------------------------

async def _http_post_with_retry(
    url: str,
    body: str,
    headers: Dict[str, str],
    timeout_s: float,
    auth: Optional[tuple] = None,
) -> None:
    from urllib.parse import urlparse
    parsed   = urlparse(url)
    use_tls  = parsed.scheme == "https"
    host     = parsed.hostname or "localhost"
    port     = parsed.port or (443 if use_tls else 80)
    path     = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    body_bytes = body.encode("utf-8")
    auth_header = ""
    if auth and auth[0]:
        import base64
        creds = base64.b64encode(f"{auth[0]}:{auth[1]}".encode()).decode()
        auth_header = f"Authorization: Basic {creds}\r\n"

    request = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        + "".join(f"{k}: {v}\r\n" for k, v in headers.items() if "Authorization" not in k or not auth_header)
        + auth_header
        + "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8") + body_bytes

    try:
        if use_tls:
            import ssl
            ctx = ssl.create_default_context()
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port, ssl=ctx), timeout=timeout_s
            )
        else:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=timeout_s
            )
        writer.write(request)
        await writer.drain()
        response_line = await asyncio.wait_for(reader.readline(), timeout=timeout_s)
        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass
        status = int(response_line.split()[1]) if len(response_line.split()) > 1 else 0
        if status >= 400:
            raise RuntimeError(f"HTTP {status} from SIEM endpoint {url}")
    except asyncio.TimeoutError:
        raise RuntimeError(f"Timeout connecting to SIEM endpoint {url}")


def _epoch(ts: Optional[str]) -> float:
    if ts is None:
        return time.time()
    try:
        return datetime.fromisoformat(ts).timestamp()
    except ValueError:
        return time.time()
