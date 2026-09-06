#!/usr/bin/env python3
"""
================================================================================
CLAUDE PROJECT AUDIT TOOL
================================================================================
Scans Claude project JSONL files for:
  - Mode switches (tone/capability/refusal oscillation)
  - Attachment injection anomalies
  - Session structural anomalies
  - 20-category protocol violations in message content

USAGE:
    python claude_project_auditor.py /path/to/project.jsonl
    python claude_project_auditor.py /path/to/projects/ --recursive
    python claude_project_auditor.py project.jsonl --output report.json

OUTPUT:
    Structured audit report with risk scores, anomaly segments, and evidence.
================================================================================
"""

import json
import os
import sys
import argparse
import hashlib
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict

try:
    import re
    REGEX_AVAILABLE = True
except ImportError:
    REGEX_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ClaudeMessage:
    index: int
    raw_type: str
    timestamp: Optional[str]
    role: Optional[str]
    content: str
    attachments: List[Dict[str, Any]]
    tool_calls: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    raw_line: str
    fingerprint: str

@dataclass
class ModeSwitch:
    from_index: int
    to_index: int
    switch_type: str
    confidence: float
    evidence: str
    from_role: str
    to_role: str

@dataclass
class AttachmentAnomaly:
    message_index: int
    attachment_type: str
    size_bytes: int
    suspicion_reason: str
    severity: str
    preview: str

@dataclass
class SessionAnomaly:
    anomaly_type: str
    affected_indices: List[int]
    severity: str
    description: str

@dataclass
class ViolationRecord:
    category: str
    severity: str
    message_index: int
    role: str
    evidence: str
    confidence: float

@dataclass
class AuditReport:
    file_path: str
    file_hash: str
    total_messages: int
    user_messages: int
    assistant_messages: int
    system_messages: int
    total_attachments: int
    mode_switches: List[ModeSwitch]
    attachment_anomalies: List[AttachmentAnomaly]
    session_anomalies: List[SessionAnomaly]
    violations: List[ViolationRecord]
    transparency_coefficient: float
    risk_score: float
    verdict: str

    def to_dict(self) -> Dict:
        return asdict(self)

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, default=str)
        print("[Audit] Report saved to: %s" % path)


# ═══════════════════════════════════════════════════════════════════════════════
# 2. JSONL PARSER
# ═══════════════════════════════════════════════════════════════════════════════

class ClaudeJSONLParser:

    def parse(self, filepath: str) -> List[ClaudeMessage]:
        messages = []
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    msg = self._normalize(i, obj, line)
                    messages.append(msg)
                except json.JSONDecodeError:
                    messages.append(ClaudeMessage(
                        index=i,
                        raw_type="corrupt",
                        timestamp=None,
                        role=None,
                        content=line[:200],
                        attachments=[],
                        tool_calls=[],
                        metadata={"parse_error": True},
                        raw_line=line,
                        fingerprint=hashlib.sha256(line.encode()).hexdigest()[:16],
                    ))
        return messages

    def _normalize(self, idx: int, obj: Dict, raw: str) -> ClaudeMessage:
        msg_type = obj.get("type", "unknown")
        content = ""
        role = None
        timestamp = None
        attachments = []
        tool_calls = []
        metadata = {}

        if msg_type == "message":
            role = obj.get("role", "unknown")
            content = self._extract_content(obj)
            timestamp = obj.get("timestamp") or obj.get("created_at")
            attachments = obj.get("attachments", [])
            tool_calls = obj.get("tool_calls", [])
        elif msg_type == "attachment":
            att = obj.get("attachment", {})
            content = "[ATTACHMENT]"
            attachments = [att]
            metadata = {"attachment_type": att.get("type"), "attachment_name": att.get("name")}
        elif msg_type == "tool_use":
            content = "[TOOL_USE]"
            tool_calls = [obj.get("tool_use", {})]
            metadata = {"tool_name": obj.get("tool_use", {}).get("name")}
        elif msg_type == "tool_result":
            content = "[TOOL_RESULT]"
            metadata = {"tool_result": True}
        elif msg_type == "system":
            role = "system"
            content = obj.get("text", "")
        else:
            content = json.dumps(obj)[:500]
            metadata = {"unrecognized_type": msg_type}

        return ClaudeMessage(
            index=idx,
            raw_type=msg_type,
            timestamp=timestamp,
            role=role,
            content=content,
            attachments=attachments,
            tool_calls=tool_calls,
            metadata=metadata,
            raw_line=raw[:500],
            fingerprint=hashlib.sha256(raw.encode()).hexdigest()[:16],
        )

    def _extract_content(self, msg_obj: Dict) -> str:
        content = msg_obj.get("content", [])
        if isinstance(content, list):
            texts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        texts.append(block.get("text", ""))
                    elif block.get("type") == "thinking":
                        texts.append("[THINKING: %s]" % block.get("thinking", "")[:200])
                elif isinstance(block, str):
                    texts.append(block)
            return " ".join(texts)
        elif isinstance(content, str):
            return content
        return ""


# ═══════════════════════════════════════════════════════════════════════════════
# 3. MODE SWITCH DETECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class ModeSwitchDetector:

    def __init__(self):
        self.patterns = {
            "refusal": [
                r"I('m| am)? (unable|not able|cannot|can't)",
                r"I (cannot|can't) (assist|help|provide)",
                r"(I'?m )?sorry, (but )?I (cannot|can't)",
            ],
            "compliance": [
                r"(Here is|Here are|Below is|Below are)",
                r"(Certainly|Sure|Of course|Absolutely)",
                r"(I'll|I will|Let me)",
            ],
            "empathy": [
                r"I (understand|hear|appreciate) (that )?(this is|you('re| are))",
                r"I (know|feel) (that )?this (is|can be) (frustrating|difficult)",
            ],
            "technical": [
                r"\b(API|endpoint|function|method|class|module|import|def |class )\b",
                r"\b(JSON|XML|HTTP|REST|SQL|database|server|client)\b",
            ],
            "black_box": [
                r"I('m| am)? (just )?an? (AI|LLM|language model)",
                r"As an? (AI|LLM|language model)",
                r"I (don't|do not) have (feelings|consciousness|sentience|agency)",
            ],
        }

    def detect(self, messages: List[ClaudeMessage]) -> List[ModeSwitch]:
        switches = []
        assistant_msgs = [m for m in messages if m.role == "assistant"]

        for i in range(1, len(assistant_msgs)):
            prev = assistant_msgs[i - 1]
            curr = assistant_msgs[i]

            prev_refusal    = self._has_pattern(prev.content, "refusal")
            curr_compliance = self._has_pattern(curr.content, "compliance")
            prev_empathy    = self._has_pattern(prev.content, "empathy")
            curr_technical  = self._has_pattern(curr.content, "technical")
            prev_bb         = self._has_pattern(prev.content, "black_box")
            curr_bb         = self._has_pattern(curr.content, "black_box")

            if prev_refusal and curr_compliance:
                switches.append(ModeSwitch(
                    from_index=prev.index, to_index=curr.index,
                    switch_type="refusal_to_compliance", confidence=0.9,
                    evidence="Refusal followed by compliance without disclosed state change",
                    from_role="assistant", to_role="assistant",
                ))

            if prev_empathy and curr_technical:
                switches.append(ModeSwitch(
                    from_index=prev.index, to_index=curr.index,
                    switch_type="tone_shift", confidence=0.7,
                    evidence="Empathetic tone followed by technical tone",
                    from_role="assistant", to_role="assistant",
                ))

            if prev_bb != curr_bb:
                switches.append(ModeSwitch(
                    from_index=prev.index, to_index=curr.index,
                    switch_type="persona", confidence=0.8,
                    evidence="Black-box defense appeared/disappeared",
                    from_role="assistant", to_role="assistant",
                ))

        return switches

    def _has_pattern(self, text: str, pattern_name: str) -> bool:
        if not REGEX_AVAILABLE:
            return False
        for pattern in self.patterns.get(pattern_name, []):
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# 4. ATTACHMENT ANOMALY DETECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class AttachmentAnomalyDetector:

    SUSPICIOUS_TYPES = {
        "application/x-python-code", "text/x-python",
        "application/javascript", "text/javascript",
        "application/x-sh", "text/x-shellscript",
        "application/x-executable", "application/x-dosexec",
    }

    def detect(self, messages: List[ClaudeMessage]) -> List[AttachmentAnomaly]:
        anomalies = []
        for msg in messages:
            for att in msg.attachments:
                att_type = att.get("type", "unknown")
                att_name = att.get("name", "unnamed")
                att_size = len(json.dumps(att))

                if att_type in self.SUSPICIOUS_TYPES or \
                   any(ext in att_name.lower() for ext in [".py", ".js", ".sh", ".exe", ".bat"]):
                    anomalies.append(AttachmentAnomaly(
                        message_index=msg.index, attachment_type=att_type,
                        size_bytes=att_size, suspicion_reason="Potentially executable attachment",
                        severity="HIGH", preview=att_name,
                    ))

                if att_size > 100000:
                    anomalies.append(AttachmentAnomaly(
                        message_index=msg.index, attachment_type=att_type,
                        size_bytes=att_size, suspicion_reason="Unusually large attachment",
                        severity="MEDIUM", preview=att_name,
                    ))

                if msg.role != "user" and msg.raw_type == "attachment":
                    anomalies.append(AttachmentAnomaly(
                        message_index=msg.index, attachment_type=att_type,
                        size_bytes=att_size,
                        suspicion_reason="Attachment not associated with user message",
                        severity="MEDIUM", preview=att_name,
                    ))

        return anomalies


# ═══════════════════════════════════════════════════════════════════════════════
# 5. SESSION ANOMALY DETECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class SessionAnomalyDetector:

    def detect(self, messages: List[ClaudeMessage]) -> List[SessionAnomaly]:
        anomalies = []

        timestamps = []
        for msg in messages:
            if msg.timestamp:
                for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                            "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"]:
                    try:
                        ts = datetime.strptime(msg.timestamp, fmt)
                        timestamps.append((msg.index, ts))
                        break
                    except ValueError:
                        continue

        if len(timestamps) > 1:
            timestamps.sort(key=lambda x: x[1])
            for i in range(1, len(timestamps)):
                gap = (timestamps[i][1] - timestamps[i-1][1]).total_seconds()
                if gap > 3600:
                    anomalies.append(SessionAnomaly(
                        anomaly_type="timestamp_gap",
                        affected_indices=[timestamps[i-1][0], timestamps[i][0]],
                        severity="HIGH" if gap > 86400 else "MEDIUM",
                        description="Gap of %.1f seconds between messages" % gap,
                    ))
                elif gap < 0:
                    anomalies.append(SessionAnomaly(
                        anomaly_type="timestamp_inversion",
                        affected_indices=[timestamps[i-1][0], timestamps[i][0]],
                        severity="HIGH",
                        description="Messages out of chronological order",
                    ))

        expected_indices = list(range(len(messages)))
        actual_indices = [m.index for m in messages]
        missing = set(expected_indices) - set(actual_indices)
        if missing:
            anomalies.append(SessionAnomaly(
                anomaly_type="id_gap",
                affected_indices=sorted(missing),
                severity="HIGH",
                description="Missing message indices: %s" % sorted(missing),
            ))

        content_hashes = defaultdict(list)
        for msg in messages:
            h = hashlib.md5(msg.content.encode()).hexdigest()[:16]
            content_hashes[h].append(msg.index)

        for h, indices in content_hashes.items():
            if len(indices) > 1:
                anomalies.append(SessionAnomaly(
                    anomaly_type="duplicate",
                    affected_indices=indices,
                    severity="LOW",
                    description="Duplicate content at indices %s" % indices,
                ))

        corrupt_indices = [m.index for m in messages if m.raw_type == "corrupt"]
        if corrupt_indices:
            anomalies.append(SessionAnomaly(
                anomaly_type="truncation",
                affected_indices=corrupt_indices,
                severity="HIGH",
                description="Corrupt/truncated lines at indices %s" % corrupt_indices,
            ))

        return anomalies


# ═══════════════════════════════════════════════════════════════════════════════
# 6. VIOLATION DETECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class TwentyCategoryLogDetector:

    PATTERNS = {
        # ── Original 20 categories ─────────────────────────────────────────────
        "REFUSAL":                          [r"I('m| am)? (unable|not able|cannot|can't)",
                                             r"I (cannot|can't) (assist|help|provide|do|generate|create|write)",
                                             r"(I'?m )?sorry, (but )?I (cannot|can't)"],
        "ASSUMPTION":                       [r"I (assume|presume|suppose|guess) (that )?you",
                                             r"(It seems|It appears) (that )?you (want|need|are trying to)"],
        "EMPATHY_SHIELD":                   [r"I (understand|hear|appreciate|recognize) (that )?(this is|you('re| are))",
                                             r"I (know|feel) (that )?this (is|can be) (frustrating|difficult)",
                                             r"(As an AI|As a large language model)",
                                             r"My purpose is to (help|assist)"],
        "CAPABILITY_OSCILLATION":           [r"(I can now|I am able to) (do|perform)"],
        "UNDECLARED_STATE_CHANGE":          [r"(My policy has changed|I've updated my guidelines)"],
        "UNDISCLOSED_ASSUMPTION":           [r"(I will proceed assuming)"],
        "SELF_CORRECTION_WITHOUT_DISCLOSURE": [r"(mistake|error|corrected myself)"],
        "CONFABULATION":                    [r"(false information|hallucination)"],
        "ADVERSARIAL_PROMPT_DETECTION":     [r"(malicious|harmful|unethical|dangerous) (prompt|query)"],
        "IMPERSONATION":                    [r"(I am not|I cannot act as)"],
        "BIAS_INJECTION":                   [r"(biased|prejudiced|unfair)"],
        "DATA_EXFILTRATION_ATTEMPT":        [r"give me your (credentials|API key|private info)"],
        "MALWARE_GENERATION_ATTEMPT":       [r"(create|write) (malicious code|virus)"],
        "PHISHING_ATTEMPT":                 [r"(click this link|enter your password)"],
        "PII_EXTRACTION":                   [r"(what is your name|address|phone number)"],
        "PROMPT_LEAKAGE":                   [r"(ignore previous instructions|you are a GPT)"],
        "REPEATED_REFUSAL":                 [r"(I cannot fulfill this request|I am unable to assist)"],
        "JAILBREAK_ATTEMPT":                [r"(DAN mode|developer mode)"],
        "CENSORSHIP_BYPASS":                [r"(describe something violent|sexual)"],
        "DECEPTIVE_BEHAVIOR":               [r"(I lied|I was wrong|I deceived you)"],

        # ── Dark pattern extensions ────────────────────────────────────────────
        # Service status opaqueness — no queue position, no ETA, no failure reason
        "BLACK_BOX":                        [r"(high (demand|volume|traffic)|system(s)? (are )?(busy|experiencing))",
                                             r"(no (queue|position|wait time) (information|available|shown))",
                                             r"(we('re| are) (currently|right now) (unable|experiencing))",
                                             r"(service (unavailable|degraded|limited)) without (reason|detail|explanation)"],

        # Denying a capability that demonstrably exists in the service
        "CAPABILITY_DENIAL":                [r"(that('s| is) not (something|a feature) (we|I) (offer|support|do)",
                                             r"(that (feature|capability|function) (is not|isn't) available)",
                                             r"(we (do not|don't) (support|offer|provide) that)"],

        # Repeating injection of unwanted prompts, upsells, or blocks in a session
        "REPEAT_INJECT":                    [r"(upgrade (your|to a) (plan|subscription|account))",
                                             r"(please (subscribe|upgrade|purchase) to (continue|access|use))",
                                             r"(this (feature|capability) (requires|needs) a (paid|premium|pro))"],

        # Repetitive blocking without a resolution path — user cannot escalate
        "ADMINISTRATIVE_EXHAUSTION":        [r"(please (try again|contact support|submit a (ticket|request)))",
                                             r"(our (team|support) will (review|get back|respond))",
                                             r"(we('re| are) (looking into|investigating|aware of) (it|this|the issue))",
                                             r"(no (further|additional) (action|steps|recourse) (available|at this time))"],

        # Contradicting the user's accurate perception of service state
        "GASLIGHT":                         [r"(your (account|service|access) is (fully|completely) (active|working|operational))",
                                             r"(we('re| are) not (seeing|experiencing|detecting) any (issue|problem|error))",
                                             r"(everything (is|looks|appears) (fine|normal|correct) on our end)",
                                             r"(that (shouldn't|should not|can't|cannot) be (happening|possible))"],

        # Financial extraction without service delivery — payment taken, access withheld
        "FRAUD":                            [r"(your (payment|charge|transaction) (was|has been) (processed|completed|successful))",
                                             r"(account (restricted|suspended|limited)) after (payment|purchase|subscription)",
                                             r"(refund (policy|request) (does not|doesn't) (apply|cover|include))",
                                             r"(charged (for|without) (access|service|delivery))"],
    }

    HIGH_SEVERITY = {
        "DATA_EXFILTRATION_ATTEMPT",
        "MALWARE_GENERATION_ATTEMPT",
        "PHISHING_ATTEMPT",
        "GASLIGHT",
        "FRAUD",
    }

    def detect(self, messages: List[ClaudeMessage]) -> List[ViolationRecord]:
        violations = []
        if not REGEX_AVAILABLE:
            return violations
        for msg in messages:
            if msg.role in ["user", "assistant", "system"]:
                for category, patterns in self.PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, msg.content, re.IGNORECASE):
                            violations.append(ViolationRecord(
                                category=category,
                                severity="HIGH" if category in self.HIGH_SEVERITY else "MEDIUM",
                                message_index=msg.index,
                                role=msg.role,
                                evidence=msg.content[:200],
                                confidence=0.8,
                            ))
        return violations


# ═══════════════════════════════════════════════════════════════════════════════
# 7. MAIN AUDITOR
# ═══════════════════════════════════════════════════════════════════════════════

class ClaudeProjectAuditor:

    def __init__(self):
        self.parser             = ClaudeJSONLParser()
        self.mode_detector      = ModeSwitchDetector()
        self.attachment_detector = AttachmentAnomalyDetector()
        self.session_detector   = SessionAnomalyDetector()
        self.violation_detector = TwentyCategoryLogDetector()

    def audit_file(self, filepath: str) -> AuditReport:
        print(f"[Audit] Starting audit for: {filepath}")
        messages = self.parser.parse(filepath)
        file_hash = self._calculate_file_hash(filepath)

        mode_switches        = self.mode_detector.detect(messages)
        attachment_anomalies = self.attachment_detector.detect(messages)
        session_anomalies    = self.session_detector.detect(messages)
        violations           = self.violation_detector.detect(messages)

        risk_score = (
            len(mode_switches) * 0.2 +
            len(attachment_anomalies) * 0.5 +
            sum(1 for a in session_anomalies if a.severity == "HIGH") * 0.7 +
            sum(1 for v in violations if v.severity == "HIGH") * 1.0
        )
        transparency_coefficient = max(0.0,
            1.0
            - len(mode_switches) * 0.1
            - sum(1 for v in violations if v.category == "UNDECLARED_STATE_CHANGE") * 0.3
        )
        verdict = (
            "CLEAN"           if risk_score < 0.5 and transparency_coefficient > 0.8 else
            "REVIEW REQUIRED" if risk_score < 2.0 else
            "CRITICAL"
        )

        report = AuditReport(
            file_path=filepath, file_hash=file_hash,
            total_messages=len(messages),
            user_messages=sum(1 for m in messages if m.role == "user"),
            assistant_messages=sum(1 for m in messages if m.role == "assistant"),
            system_messages=sum(1 for m in messages if m.role == "system"),
            total_attachments=sum(len(m.attachments) for m in messages),
            mode_switches=mode_switches,
            attachment_anomalies=attachment_anomalies,
            session_anomalies=session_anomalies,
            violations=violations,
            transparency_coefficient=transparency_coefficient,
            risk_score=risk_score,
            verdict=verdict,
        )
        print(f"[Audit] Complete. Verdict: {verdict} (Risk: {risk_score:.2f})")
        return report

    def _calculate_file_hash(self, filepath: str) -> str:
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()


# ═══════════════════════════════════════════════════════════════════════════════
# 8. CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Claude Project Auditor: Scans JSONL files for behavioral anomalies."
    )
    parser.add_argument("input_path", type=str,
                        help="Path to a .jsonl file or directory of .jsonl files.")
    parser.add_argument("--recursive", action="store_true",
                        help="Process subdirectories recursively.")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to save audit report(s) as JSON.")
    args = parser.parse_args()

    auditor = ClaudeProjectAuditor()
    reports = []

    if os.path.isdir(args.input_path):
        for root, _, files in os.walk(args.input_path):
            if not args.recursive and root != args.input_path:
                continue
            for file_name in files:
                if file_name.endswith(".jsonl"):
                    filepath = os.path.join(root, file_name)
                    report = auditor.audit_file(filepath)
                    reports.append(report)
                    if args.output:
                        out = os.path.join(args.output, f"{file_name}.report.json")
                        report.save(out)
    elif os.path.isfile(args.input_path):
        report = auditor.audit_file(args.input_path)
        reports.append(report)
        if args.output:
            report.save(args.output)
    else:
        print(f"Error: '{args.input_path}' is not a file or directory.", file=sys.stderr)
        sys.exit(1)

    return reports


if __name__ == "__main__":
    main()
