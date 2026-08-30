"""
canvas_telemetry — Structured JSON telemetry for canvas_security.

Emits newline-delimited JSON (NDJSON) to stdout so any log pipeline
(Vector, Fluentd, Logstash, Splunk) can ingest events without a sidecar.

Also exposes a Prometheus text-exposition dump of cumulative counters so a
textfile collector (or push-gateway flush) can scrape them.

Usage:
    logger = StructuredLogger()
    await platform.run_enhanced_scan(targets, logger=logger)
    print(logger.prometheus_exposition())
"""

import json
import os
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, TextIO


# ---------------------------------------------------------------------------
# Event vocabulary
# ---------------------------------------------------------------------------

class Level(str, Enum):
    INFO     = "INFO"
    WARNING  = "WARNING"
    ERROR    = "ERROR"
    CRITICAL = "CRITICAL"


class EventType(str, Enum):
    SCAN_START        = "scan_start"
    SCAN_COMPLETE     = "scan_complete"
    SCAN_TIMEOUT      = "scan_timeout"
    CLEANUP_FAILURE   = "cleanup_failure"
    CONNECTOR_SUCCESS = "connector_success"
    CONNECTOR_FAILURE = "connector_failure"
    POLICY_VIOLATION  = "policy_violation"
    ZOMBIE_DETECTED   = "zombie_detected"
    PLATFORM_ERROR    = "platform_error"


# ---------------------------------------------------------------------------
# Event model
# ---------------------------------------------------------------------------

@dataclass
class TelemetryEvent:
    event:     EventType
    level:     Level              = Level.INFO
    service:   str                = "canvas_security"
    data:      Dict[str, Any]     = field(default_factory=dict)
    timestamp: Optional[str]      = None
    trace_id:  Optional[str]      = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "level":     self.level.value,
            "event":     self.event.value,
            "service":   self.service,
            **({"trace_id": self.trace_id} if self.trace_id else {}),
            **self.data,
        }


# ---------------------------------------------------------------------------
# Structured logger
# ---------------------------------------------------------------------------

class StructuredLogger:
    """
    Writes one JSON object per line to *stream* (default stdout).

    Maintains monotonic counters used by prometheus_exposition().  Labels
    come from the event type and the optional *labels* kwarg on emit().
    """

    def __init__(
        self,
        stream:  TextIO = sys.stdout,
        service: str    = "canvas_security",
    ) -> None:
        self._stream  = stream
        self._service = service
        # { event_type -> { label_hash -> (labels_dict, count) } }
        self._counters: Dict[str, Dict[str, list]] = {}

    # ------------------------------------------------------------------
    # Core emit
    # ------------------------------------------------------------------

    def emit(
        self,
        event:    EventType,
        level:    Level               = Level.INFO,
        data:     Optional[dict]      = None,
        labels:   Optional[dict]      = None,
        trace_id: Optional[str]       = None,
    ) -> TelemetryEvent:
        ev = TelemetryEvent(
            event    = event,
            level    = level,
            service  = self._service,
            data     = data or {},
            trace_id = trace_id,
        )
        self._stream.write(json.dumps(ev.to_dict(), default=str) + "\n")
        self._stream.flush()
        self._increment(event.value, labels or {})
        return ev

    # ------------------------------------------------------------------
    # Prometheus text exposition
    # ------------------------------------------------------------------

    def prometheus_exposition(self) -> str:
        """
        Return Prometheus text-exposition format (metric families, one counter
        per event type, broken down by label set).

        Flush the result to a textfile the node_exporter textfile collector
        watches, or POST it to a push-gateway endpoint.
        """
        lines: List[str] = []
        for ev_name, label_buckets in sorted(self._counters.items()):
            metric = f"canvas_security_{ev_name}_total"
            lines.append(f"# HELP {metric} Total occurrences of {ev_name}")
            lines.append(f"# TYPE {metric} counter")
            for label_set, (labels, count) in label_buckets.items():
                lstr = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
                lstr = f"service=\"{self._service}\",{lstr}" if lstr else f"service=\"{self._service}\""
                lines.append(f"{metric}{{{lstr}}} {count}")
        return "\n".join(lines) + ("\n" if lines else "")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _increment(self, event_name: str, labels: dict) -> None:
        bucket = self._counters.setdefault(event_name, {})
        key = json.dumps(labels, sort_keys=True)
        if key not in bucket:
            bucket[key] = [labels, 0]
        bucket[key][1] += 1

    def scan_start(self, targets: List[str], **kw) -> TelemetryEvent:
        return self.emit(EventType.SCAN_START, data={"target_count": len(targets), "targets": targets}, **kw)

    def scan_complete(self, target: str, finding_count: int, **kw) -> TelemetryEvent:
        return self.emit(EventType.SCAN_COMPLETE, data={"target": target, "finding_count": finding_count}, **kw)

    def scan_timeout(self, target: str, timeout_s: float, **kw) -> TelemetryEvent:
        return self.emit(
            EventType.SCAN_TIMEOUT, level=Level.WARNING,
            data={"target": target, "timeout_s": timeout_s},
            labels={"target": target}, **kw,
        )

    def cleanup_failure(self, target: str, reason: str, **kw) -> TelemetryEvent:
        return self.emit(
            EventType.CLEANUP_FAILURE, level=Level.CRITICAL,
            data={"target": target, "reason": reason},
            labels={"target": target}, **kw,
        )

    def connector_success(self, connector: str, finding_count: int, **kw) -> TelemetryEvent:
        return self.emit(
            EventType.CONNECTOR_SUCCESS,
            data={"connector": connector, "finding_count": finding_count},
            labels={"connector": connector}, **kw,
        )

    def connector_failure(self, connector: str, error: str, **kw) -> TelemetryEvent:
        return self.emit(
            EventType.CONNECTOR_FAILURE, level=Level.ERROR,
            data={"connector": connector, "error": error},
            labels={"connector": connector}, **kw,
        )

    def policy_violation(self, field_name: str, value: str, reason: str, **kw) -> TelemetryEvent:
        return self.emit(
            EventType.POLICY_VIOLATION, level=Level.WARNING,
            data={"field": field_name, "value": value, "reason": reason},
            labels={"field": field_name}, **kw,
        )

    def zombie_detected(self, count: int, host_pid: int, **kw) -> TelemetryEvent:
        return self.emit(
            EventType.ZOMBIE_DETECTED, level=Level.WARNING,
            data={"zombie_count": count, "host_pid": host_pid},
            labels={"severity": "high" if count > 5 else "low"}, **kw,
        )


# ---------------------------------------------------------------------------
# Telemetry-aware wrappers around HostProcessTelemetry
# ---------------------------------------------------------------------------

def emit_zombie_telemetry(logger: StructuredLogger) -> int:
    """
    Count zombie children and emit a structured event if any are found.
    Returns the zombie count.
    """
    from canvas_security import HostProcessTelemetry
    count = HostProcessTelemetry.count_zombies()
    if count > 0:
        logger.zombie_detected(count=count, host_pid=os.getpid())
    return count


# ---------------------------------------------------------------------------
# Prometheus textfile writer (for node_exporter --collector.textfile)
# ---------------------------------------------------------------------------

def write_prometheus_textfile(logger: StructuredLogger, path: str) -> None:
    """
    Write Prometheus counters to *path* atomically (write-then-rename)
    so the textfile collector never reads a partial file.
    """
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(logger.prometheus_exposition())
    os.replace(tmp, path)
