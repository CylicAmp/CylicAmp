"""
XML parsers for Nmap and Nessus output.
No third-party dependencies — uses expat via Python's standard library to block
XXE, DTD declarations, and entity expansion (Billion Laughs).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import List
import xml.etree.ElementTree as ET
from xml.parsers import expat


# ── Safe parser (stdlib only) ──────────────────────────────────────────────────

class UntrustedXMLParser:
    """Safe XML parser using only Python's standard library.

    Uses expat.ParserCreate() directly (compatible with Python 3.8–3.13+)
    to block DTD declarations and entity expansions before they are processed,
    preventing XXE and Billion Laughs attacks.
    """

    def __init__(self):
        self._expat = expat.ParserCreate()
        self._expat.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
        self._expat.StartDoctypeDeclHandler = self._forbid_dtd
        self._expat.EntityDeclHandler = self._forbid_entity
        # Build the element tree via expat handlers directly
        self._stack: list = []
        self._root: ET.Element | None = None
        self._expat.StartElementHandler = self._start_element
        self._expat.EndElementHandler = self._end_element
        self._expat.CharacterDataHandler = self._char_data

    def _forbid_dtd(self, doctype_name, system_id, public_id, has_internal_subset):
        raise ValueError(
            f"Parsing rejected: DOCTYPE declarations are forbidden (found: {doctype_name})"
        )

    def _forbid_entity(self, entity_name, is_parameter_entity, value, base,
                       system_id, public_id, notation_name):
        raise ValueError(
            f"Parsing rejected: Custom entity declarations are forbidden (found: &{entity_name};)"
        )

    def _start_element(self, name, attrs):
        elem = ET.Element(name, attrs)
        if self._stack:
            self._stack[-1].append(elem)
        else:
            self._root = elem
        self._stack.append(elem)

    def _end_element(self, name):
        self._stack.pop()

    def _char_data(self, data):
        if not self._stack:
            return
        elem = self._stack[-1]
        if len(elem) == 0:
            elem.text = (elem.text or "") + data
        else:
            last = elem[-1]
            last.tail = (last.tail or "") + data

    def parse(self, xml_bytes_or_str):
        if isinstance(xml_bytes_or_str, str):
            xml_bytes_or_str = xml_bytes_or_str.encode("utf-8")
        self._expat.Parse(xml_bytes_or_str, True)
        return self._root


def safe_fromstring(xml_str: str) -> ET.Element:
    """Drop-in replacement for ET.fromstring — blocks DTD and entity attacks."""
    return UntrustedXMLParser().parse(xml_str)


# ── Data classes ───────────────────────────────────────────────────────────────

@dataclass
class NmapFinding:
    host: str
    protocol: str
    port: int
    state: str
    service_name: str = ""
    service_product: str = ""
    service_version: str = ""


@dataclass
class NessusFinding:
    host: str
    plugin_id: str
    plugin_name: str
    severity: int
    port: int
    protocol: str
    description: str = ""
    solution: str = ""


# ── Parsers ────────────────────────────────────────────────────────────────────

class NmapXmlParser:

    async def parse_string(self, xml_text: str) -> List[NmapFinding]:
        return await asyncio.get_event_loop().run_in_executor(
            None, self._parse_sync, xml_text
        )

    def _parse_sync(self, xml_text: str) -> List[NmapFinding]:
        root = safe_fromstring(xml_text)  # raises ValueError on DTD/entity attacks
        findings: List[NmapFinding] = []

        for host_elem in root.findall("host"):
            addr_elem = host_elem.find("address[@addrtype='ipv4']")
            if addr_elem is None:
                addr_elem = host_elem.find("address")
            host_addr = addr_elem.get("addr", "") if addr_elem is not None else ""

            ports_elem = host_elem.find("ports")
            if ports_elem is None:
                continue

            for port_elem in ports_elem.findall("port"):
                raw_portid = port_elem.get("portid", "")
                port_num = int(raw_portid)          # raises ValueError on non-integer
                if port_num < 0 or port_num > 65535:
                    raise ValueError(f"Port {port_num} out of valid range 0-65535")

                protocol = port_elem.get("protocol", "")
                state_elem = port_elem.find("state")
                state = state_elem.get("state", "") if state_elem is not None else ""

                svc_elem = port_elem.find("service")
                svc_name = svc_product = svc_version = ""
                if svc_elem is not None:
                    svc_name = svc_elem.get("name", "")
                    svc_product = svc_elem.get("product", "")
                    svc_version = svc_elem.get("version", "")

                findings.append(NmapFinding(
                    host=host_addr,
                    protocol=protocol,
                    port=port_num,
                    state=state,
                    service_name=svc_name,
                    service_product=svc_product,
                    service_version=svc_version,
                ))

        return findings


class NessusXmlParser:

    async def parse_string(self, xml_text: str) -> List[NessusFinding]:
        return await asyncio.get_event_loop().run_in_executor(
            None, self._parse_sync, xml_text
        )

    def _parse_sync(self, xml_text: str) -> List[NessusFinding]:
        root = safe_fromstring(xml_text)
        findings: List[NessusFinding] = []

        for report_host in root.findall(".//ReportHost"):
            host_addr = report_host.get("name", "")
            for item in report_host.findall("ReportItem"):
                port_num = int(item.get("port", "0"))
                if port_num < 0 or port_num > 65535:
                    raise ValueError(f"Port {port_num} out of valid range")
                findings.append(NessusFinding(
                    host=host_addr,
                    plugin_id=item.get("pluginID", ""),
                    plugin_name=item.get("pluginName", ""),
                    severity=int(item.get("severity", "0")),
                    port=port_num,
                    protocol=item.get("protocol", ""),
                    description=(item.findtext("description") or "").strip(),
                    solution=(item.findtext("solution") or "").strip(),
                ))

        return findings
