import pytest
import asyncio
import sys
from unittest.mock import AsyncMock, patch, MagicMock
from canvas_security import (
    EnhancedSecurityPlatform,
    ContainerizedScannerConnector,
    ProcessExecutionPolicy,
    HostProcessTelemetry
)

# Mock definitions for cross-platform process isolation mechanics
class MockProcess:
    def __init__(self, returncode=0, stdout=b"", stderr=b""):
        self.returncode = returncode
        self.pid = 12345
        self._stdout = stdout
        self._stderr = stderr

    async def communicate(self):
        return self._stdout, self._stderr

    async def wait(self):
        return self.returncode

class MockTimeoutProcess(MockProcess):
    async def communicate(self):
        await asyncio.sleep(10)
        return b"", b""
    async def wait(self):
        await asyncio.sleep(10)
        return 0


@pytest.mark.asyncio
async def test_successful_scan_execution():
    """Verifies standard clean validation pathway returns parsing matrices correctly."""
    config = {
        "container_engine": "docker",
        "image_name": "security-scanner-image:latest",
        "allowed_engines": ["docker"],
        "allowed_images": ["security-scanner-image:latest"]
    }
    connector = ContainerizedScannerConnector(config)

    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_exec.return_value = MockProcess(returncode=0, stdout=b"open ports: 80, 443")
        res = await connector.search(["127.0.0.1"])
        assert res.success is True
        assert len(res.findings) == 1
        assert res.findings[0].id == "canvas-scan-127.0.0.1"


@pytest.mark.asyncio
async def test_empty_results_handling():
    """Verifies systems function correctly when scanners register blank findings portfolios."""
    config = {
        "container_engine": "docker",
        "image_name": "security-scanner-image:latest"
    }
    connector = ContainerizedScannerConnector(config)
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_exec.return_value = MockProcess(returncode=0, stdout=b"")
        res = await connector.search(["8.8.8.8"])
        assert res.success is True
        assert len(res.findings) == 1


@pytest.mark.asyncio
async def test_timeout_cleanup_escalation_and_container_eviction():
    """Ensures timeout transitions trigger process tree destruction policies."""
    config = {
        "container_engine": "docker",
        "image_name": "security-scanner-image:latest",
        "timeout_term": 0.01,
        "timeout_kill": 0.01
    }
    connector = ContainerizedScannerConnector(config)

    with patch('asyncio.create_subprocess_exec') as mock_exec, \
         patch('os.killpg') as mock_killpg, \
         patch('os.getpgid', return_value=999):

        mock_exec.side_effect = [MockTimeoutProcess(), MockProcess(returncode=0)]
        res = await connector.search(["1.1.1.1"])

        assert mock_killpg.called
        assert mock_exec.call_count == 2  # Main execution run process + Cleanup container call process


@pytest.mark.asyncio
async def test_cleanup_failure_isolation():
    """Validates runtime exceptions generate alerts when containers defy host cleanup constraints."""
    config = {
        "container_engine": "docker",
        "image_name": "security-scanner-image:latest",
        "timeout_term": 0.001
    }
    connector = ContainerizedScannerConnector(config)
    with patch('asyncio.create_subprocess_exec') as mock_exec:
        mock_exec.side_effect = [MockTimeoutProcess(), RuntimeError("Engine lock failure")]
        with pytest.raises(RuntimeError, match="CLEANUP_FAILURE"):
            await connector.search(["1.1.1.1"])


def test_target_policy_bypass_attempts():
    """Asserts input scrubbing models catch complex URL/Domain masquerade strings."""
    policy = ProcessExecutionPolicy({})
    malicious_targets = [
        "127.0.0.1; rm -rf /",
        "google.com&&wget",
        "vulnerable.target.org|cat /etc/passwd",
        "subdomain$.domain.com"
    ]
    for target in malicious_targets:
        with pytest.raises(ValueError, match="Policy Violation"):
            policy.validate_target(target)


def test_malicious_nmap_arguments_injection():
    """Asserts input scrubbing models reject inline flags or leading option blocks."""
    policy = ProcessExecutionPolicy({})
    malicious_args = [
        "--privileged",
        "-v; reboot",
        "512m && echo malicious",
        "--cpu-shares=999"
    ]
    for arg in malicious_args:
        with pytest.raises(ValueError, match="Policy Violation"):
            policy.validate_argument(arg)


def test_malicious_container_engine_or_image_configuration():
    """Ensures untrusted binary/image environments fail to mount parsing context boundaries."""
    policy = ProcessExecutionPolicy({
        "allowed_engines": ["docker"],
        "allowed_images": ["security-scanner-image:latest"]
    })
    with pytest.raises(ValueError, match="Untrusted container engine"):
        policy.validate_engine_and_image("untrusted-engine", "security-scanner-image:latest")

    with pytest.raises(ValueError, match="Untrusted container image"):
        policy.validate_engine_and_image("docker", "malicious-crawler:v3")


@pytest.mark.asyncio
async def test_connector_failure_orchestrator_isolation():
    """Ensures a catastrophic failure inside one loop step does not disrupt adjacent elements."""
    config = {
        "connectors": {"container_scanner": {"enabled": True}}
    }
    platform = EnhancedSecurityPlatform(config)

    # Force search to raise a raw core system level crash
    with patch.object(ContainerizedScannerConnector, 'search', side_effect=Exception("Database cluster vanished")):
        result = await platform.run_enhanced_scan(["127.0.0.1"])
        assert len(result.connector_results) == 1
        assert result.connector_results[0].failed is True
        assert result.connector_results[0].success is False


def test_zombie_detection_telemetry():
    """Confirms psutil status scanning tracks structural zombie process layers accurately."""
    with patch('sys.platform', 'linux'), \
         patch('os.getpid', return_value=500), \
         patch('psutil.process_iter') as mock_iter:

        proc_mock1 = MagicMock()
        proc_mock1.info = {'status': 'zombie', 'ppid': 500}
        proc_mock2 = MagicMock()
        proc_mock2.info = {'status': 'running', 'ppid': 500}

        mock_iter.return_value = [proc_mock1, proc_mock2]
        assert HostProcessTelemetry.count_zombies() == 1
