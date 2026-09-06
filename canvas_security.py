"""
canvas_security — Containerized security scanning platform with process isolation.

Components:
  ContainerizedScannerConnector  — runs scans inside container sandboxes
  ProcessExecutionPolicy         — validates targets, args, engine/image allowlists
  EnhancedSecurityPlatform       — orchestrates connectors, isolates failures
  HostProcessTelemetry           — monitors host-side zombie processes
"""

import asyncio
import os
import re
import signal
from dataclasses import dataclass, field
from typing import Dict, List, Optional

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False


# ---------------------------------------------------------------------------
# Data transfer objects
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    id: str
    raw_output: str = ""
    target: str = ""


@dataclass
class ScanResult:
    success: bool
    findings: List[Finding] = field(default_factory=list)
    error: Optional[str] = None
    failed: bool = False


@dataclass
class ConnectorResult:
    success: bool
    failed: bool
    findings: List[Finding] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class PlatformResult:
    connector_results: List[ConnectorResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Policy enforcement
# ---------------------------------------------------------------------------

class ProcessExecutionPolicy:
    # Reject any target containing shell-special characters
    _TARGET_FORBIDDEN = re.compile(r'[;&|$`()\\\'"<>\s]')
    # Accept only IP addresses, hostnames, and domains
    _TARGET_VALID = re.compile(r'^[a-zA-Z0-9.\-]+$')

    def __init__(self, config: dict):
        self.allowed_engines: List[str] = config.get("allowed_engines", [])
        self.allowed_images: List[str] = config.get("allowed_images", [])

    def validate_target(self, target: str) -> None:
        if self._TARGET_FORBIDDEN.search(target) or not self._TARGET_VALID.match(target):
            raise ValueError(f"Policy Violation: invalid target '{target}'")

    def validate_argument(self, arg: str) -> None:
        # Reject flags (leading dash) and any shell injection characters
        if arg.startswith("-") or re.search(r'[;&|$`()\\\'"<>]', arg):
            raise ValueError(f"Policy Violation: invalid argument '{arg}'")

    def validate_engine_and_image(self, engine: str, image: str) -> None:
        if self.allowed_engines and engine not in self.allowed_engines:
            raise ValueError(f"Untrusted container engine: '{engine}'")
        if self.allowed_images and image not in self.allowed_images:
            raise ValueError(f"Untrusted container image: '{image}'")


# ---------------------------------------------------------------------------
# Containerized scanner connector
# ---------------------------------------------------------------------------

class ContainerizedScannerConnector:
    _DEFAULT_TIMEOUT_TERM = 30.0
    _DEFAULT_TIMEOUT_KILL = 10.0

    def __init__(self, config: dict):
        self.config = config
        self.engine: str = config.get("container_engine", "docker")
        self.image: str = config.get("image_name", "")
        self.timeout_term: float = float(config.get("timeout_term", self._DEFAULT_TIMEOUT_TERM))
        self.timeout_kill: float = float(config.get("timeout_kill", self._DEFAULT_TIMEOUT_KILL))
        self.policy = ProcessExecutionPolicy(config)

    async def search(self, targets: List[str]) -> ScanResult:
        findings: List[Finding] = []

        for target in targets:
            self.policy.validate_target(target)

            cmd = [self.engine, "run", "--rm", "--network=none", self.image, target]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                start_new_session=True,
            )

            try:
                stdout, _ = await asyncio.wait_for(
                    proc.communicate(),
                    timeout=self.timeout_term,
                )
            except asyncio.TimeoutError:
                await self._terminate_process_group(proc)
                await self._cleanup_container(target)
                findings.append(Finding(
                    id=f"canvas-scan-{target}",
                    raw_output="TIMEOUT",
                    target=target,
                ))
                continue

            findings.append(Finding(
                id=f"canvas-scan-{target}",
                raw_output=stdout.decode("utf-8", errors="replace"),
                target=target,
            ))

        return ScanResult(success=True, findings=findings)

    async def _terminate_process_group(self, proc) -> None:
        # SIGTERM the whole process group
        try:
            pgid = os.getpgid(proc.pid)
            os.killpg(pgid, signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass

        # Wait briefly, then SIGKILL if still alive
        try:
            await asyncio.wait_for(proc.wait(), timeout=self.timeout_kill)
        except asyncio.TimeoutError:
            try:
                pgid = os.getpgid(proc.pid)
                os.killpg(pgid, signal.SIGKILL)
            except (ProcessLookupError, OSError):
                pass

    async def _cleanup_container(self, target: str) -> None:
        container_name = f"scan-{target}"
        cleanup_cmd = [self.engine, "rm", "-f", container_name]
        try:
            cleanup_proc = await asyncio.create_subprocess_exec(
                *cleanup_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await cleanup_proc.communicate()
        except Exception as exc:
            raise RuntimeError(f"CLEANUP_FAILURE: {exc}") from exc


# ---------------------------------------------------------------------------
# Platform orchestrator
# ---------------------------------------------------------------------------

class EnhancedSecurityPlatform:
    def __init__(self, config: dict):
        self.config = config
        self._connectors: Dict[str, ContainerizedScannerConnector] = {}

        connector_cfg: dict = config.get("connectors", {})
        if connector_cfg.get("container_scanner", {}).get("enabled", False):
            scanner_cfg = dict(connector_cfg.get("container_scanner", {}))
            self._connectors["container_scanner"] = ContainerizedScannerConnector(scanner_cfg)

    async def run_enhanced_scan(self, targets: List[str]) -> PlatformResult:
        results: List[ConnectorResult] = []

        for _name, connector in self._connectors.items():
            try:
                scan = await connector.search(targets)
                results.append(ConnectorResult(
                    success=scan.success,
                    failed=not scan.success,
                    findings=scan.findings,
                ))
            except Exception as exc:
                results.append(ConnectorResult(
                    success=False,
                    failed=True,
                    error=str(exc),
                ))

        return PlatformResult(connector_results=results)


# ---------------------------------------------------------------------------
# Host process telemetry
# ---------------------------------------------------------------------------

class HostProcessTelemetry:
    @staticmethod
    def count_zombies() -> int:
        if not _PSUTIL_AVAILABLE:
            return 0
        my_pid = os.getpid()
        count = 0
        for proc in psutil.process_iter(["status", "ppid"]):
            info = proc.info
            if info.get("status") == "zombie" and info.get("ppid") == my_pid:
                count += 1
        return count
