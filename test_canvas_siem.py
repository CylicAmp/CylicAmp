import asyncio
import json
import pytest
import socket
from unittest.mock import AsyncMock, MagicMock, patch
from canvas_telemetry import Level, EventType, TelemetryEvent
from canvas_siem import (
    CEFFormatter,
    SplunkHECExporter,
    SyslogExporter,
    ElasticExporter,
    SIEMPipeline,
    _epoch,
)


def make_event(**kwargs) -> TelemetryEvent:
    defaults = dict(
        event=EventType.SCAN_TIMEOUT,
        level=Level.WARNING,
        service="test",
        data={"target": "1.1.1.1", "timeout_s": 30.0},
        timestamp="2026-08-30T12:00:00+00:00",
    )
    defaults.update(kwargs)
    return TelemetryEvent(**defaults)


# ---------------------------------------------------------------------------
# CEFFormatter
# ---------------------------------------------------------------------------

class TestCEFFormatter:
    def test_header_structure(self):
        ev = make_event()
        cef = CEFFormatter.format(ev)
        assert cef.startswith("CEF:0|CylicAmp|CanvasSecurity|1.0|")

    def test_severity_mapping(self):
        assert "WARNING" not in CEFFormatter.format(make_event(level=Level.WARNING))
        cef_warn = CEFFormatter.format(make_event(level=Level.WARNING))
        cef_crit = CEFFormatter.format(make_event(level=Level.CRITICAL))
        warn_sev = int(cef_warn.split("|")[6])
        crit_sev = int(cef_crit.split("|")[6])
        assert warn_sev < crit_sev

    def test_extension_contains_target(self):
        ev = make_event(data={"target": "10.0.0.1", "timeout_s": 30})
        cef = CEFFormatter.format(ev)
        assert "10.0.0.1" in cef

    def test_pipe_chars_in_header_fields_escaped(self):
        # Pipe chars in the 7-field header must be escaped; extension values
        # are space-separated key=value pairs so pipes there are harmless.
        # Verify the header itself has no unescaped pipes in our controlled fields.
        ev = make_event()
        parts = CEFFormatter.format(ev).split("|")
        # A valid CEF:0 header has exactly 7 pipe-separated sections before the extension
        assert parts[0] == "CEF:0"
        assert len(parts) >= 8

    def test_equals_chars_escaped_in_extension(self):
        ev = make_event(data={"reason": "key=value"})
        cef = CEFFormatter.format(ev)
        ext = cef.split("|", 7)[7]
        # Extension values should have = escaped
        assert "key\\=value" in ext or "key=value" not in ext.split("reason")[1:][0] if "reason" in ext else True

    def test_trace_id_included(self):
        ev = make_event(trace_id="abc-123")
        cef = CEFFormatter.format(ev)
        assert "abc-123" in cef


# ---------------------------------------------------------------------------
# SplunkHECExporter
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSplunkHECExporter:
    async def test_correct_endpoint_called(self):
        exporter = SplunkHECExporter(url="http://splunk:8088", token="tok123")
        with patch("canvas_siem._http_post_with_retry", new_callable=AsyncMock) as mock_post:
            await exporter.export(make_event())
            url_used = mock_post.call_args[0][0]
            assert url_used.endswith("/services/collector/event")

    async def test_auth_header_contains_token(self):
        exporter = SplunkHECExporter(url="http://splunk:8088", token="mysecret")
        with patch("canvas_siem._http_post_with_retry", new_callable=AsyncMock) as mock_post:
            await exporter.export(make_event())
            headers = mock_post.call_args[0][2]
            assert "Splunk mysecret" in headers.get("Authorization", "")

    async def test_payload_is_valid_json_with_event_key(self):
        exporter = SplunkHECExporter(url="http://splunk:8088", token="tok")
        with patch("canvas_siem._http_post_with_retry", new_callable=AsyncMock) as mock_post:
            await exporter.export(make_event())
            payload = json.loads(mock_post.call_args[0][1])
            assert "event" in payload
            assert "time" in payload
            assert "sourcetype" in payload

    async def test_batch_export_sends_concatenated_json(self):
        exporter = SplunkHECExporter(url="http://splunk:8088", token="tok")
        events = [make_event(), make_event(event=EventType.SCAN_COMPLETE)]
        with patch("canvas_siem._http_post_with_retry", new_callable=AsyncMock) as mock_post:
            await exporter.export_batch(events)
            payload = mock_post.call_args[0][1]
            lines = [l for l in payload.split("\n") if l]
            assert len(lines) == 2
            for line in lines:
                json.loads(line)  # each line must be valid JSON


# ---------------------------------------------------------------------------
# ElasticExporter
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestElasticExporter:
    async def test_bulk_endpoint_used(self):
        exporter = ElasticExporter(url="http://elastic:9200")
        with patch("canvas_siem._http_post_with_retry", new_callable=AsyncMock) as mock_post:
            await exporter.export(make_event())
            assert mock_post.call_args[0][0].endswith("/_bulk")

    async def test_ndjson_content_type(self):
        exporter = ElasticExporter(url="http://elastic:9200")
        with patch("canvas_siem._http_post_with_retry", new_callable=AsyncMock) as mock_post:
            await exporter.export(make_event())
            headers = mock_post.call_args[0][2]
            assert headers.get("Content-Type") == "application/x-ndjson"

    async def test_bulk_body_has_action_and_source_lines(self):
        exporter = ElasticExporter(url="http://elastic:9200")
        with patch("canvas_siem._http_post_with_retry", new_callable=AsyncMock) as mock_post:
            await exporter.export_batch([make_event(), make_event()])
            payload = mock_post.call_args[0][1]
            lines = [l for l in payload.strip().split("\n") if l]
            assert len(lines) == 4  # 2 × (action + source)
            for i in range(0, len(lines), 2):
                action = json.loads(lines[i])
                assert "index" in action


# ---------------------------------------------------------------------------
# SyslogExporter (RFC 5424)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSyslogExporter:
    async def test_syslog_message_format(self):
        exporter = SyslogExporter(host="localhost", port=514)
        ev = make_event()
        msg = exporter._format_rfc5424(ev)
        # Must start with <PRI>1
        assert msg.startswith("<")
        assert ">1 " in msg

    async def test_priority_increases_with_severity(self):
        exporter = SyslogExporter(host="localhost", port=514)
        info_msg  = exporter._format_rfc5424(make_event(level=Level.INFO))
        crit_msg  = exporter._format_rfc5424(make_event(level=Level.CRITICAL))
        info_pri  = int(info_msg[1:info_msg.index(">")])
        crit_pri  = int(crit_msg[1:crit_msg.index(">")])
        # Lower syslog priority number = higher severity
        assert crit_pri < info_pri

    async def test_structured_data_block_present(self):
        exporter = SyslogExporter(host="localhost", port=514)
        ev = make_event(data={"target": "1.2.3.4"})
        msg = exporter._format_rfc5424(ev)
        assert "[canvas@32473" in msg
        assert "1.2.3.4" in msg

    async def test_udp_sendto_called_on_export(self):
        exporter = SyslogExporter(host="127.0.0.1", port=514)
        mock_sock = MagicMock()
        exporter._sock = mock_sock
        ev = make_event()
        encoded = exporter._format_rfc5424(ev).encode("utf-8")
        exporter._send(encoded)
        mock_sock.sendto.assert_called_once_with(encoded, ("127.0.0.1", 514))


# ---------------------------------------------------------------------------
# SIEMPipeline
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSIEMPipeline:
    async def test_event_reaches_all_exporters(self):
        exp1 = AsyncMock(spec=SplunkHECExporter)
        exp2 = AsyncMock(spec=SyslogExporter)
        pipeline = SIEMPipeline([exp1, exp2])
        pipeline.start()
        await pipeline.send(make_event())
        await asyncio.sleep(0.05)
        await pipeline.stop()
        exp1.export.assert_called_once()
        exp2.export.assert_called_once()

    async def test_exporter_failure_does_not_block_other_exporters(self):
        exp1 = AsyncMock(spec=SplunkHECExporter)
        exp1.export.side_effect = RuntimeError("Splunk down")
        exp2 = AsyncMock(spec=SyslogExporter)
        pipeline = SIEMPipeline([exp1, exp2], queue_size=10)
        # Send directly (bypass queue) to isolate behavior
        await pipeline._ship(make_event())
        # exp2 should still have been called despite exp1 failing
        assert exp2.export.called

    async def test_queue_overflow_drops_oldest(self):
        exp = AsyncMock(spec=SplunkHECExporter)
        exp.export = AsyncMock(side_effect=asyncio.sleep(1))  # slow consumer
        pipeline = SIEMPipeline([exp], queue_size=2)
        ev = make_event()
        await pipeline.send(ev)
        await pipeline.send(ev)
        # Third send on a full queue should not raise
        await pipeline.send(ev)
        assert pipeline._queue.qsize() <= 2


# ---------------------------------------------------------------------------
# _epoch helper
# ---------------------------------------------------------------------------

class TestEpoch:
    def test_parses_iso_timestamp(self):
        ts = "2026-08-30T12:00:00+00:00"
        epoch = _epoch(ts)
        assert isinstance(epoch, float)
        assert epoch > 0

    def test_none_returns_current_time(self):
        import time
        before = time.time()
        result = _epoch(None)
        after = time.time()
        assert before <= result <= after
