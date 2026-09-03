import pytest
import xml.etree.ElementTree as ET
from unittest.mock import MagicMock

from enhanced_security_platform_real_connectors import NmapXmlParser, NessusXmlParser

# 1. XXE Mitigation Payload (Untrusted Input Testing)
MALICIOUS_XXE_XML = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<nmaprun>
  <host>
    <address addr="192.168.1.50" addrtype="ipv4"/>
    <ports>
      <port protocol="tcp" portid="80">
        <state state="open" reason="syn-ack"/>
        <service name="http" product="&xxe;"/>
      </port>
    </ports>
  </host>
</nmaprun>"""

# 2. Injection / Malformed Data Payload
MALFORMED_PORT_XML = """<?xml version="1.0" encoding="utf-8"?>
<nmaprun>
  <host>
    <address addr="10.0.0.1" addrtype="ipv4"/>
    <ports>
      <port protocol="tcp" portid="999999999999 OR 1=1">
        <state state="open" reason="syn-ack"/>
      </port>
    </ports>
  </host>
</nmaprun>"""

# Safe exception names — covers defusedxml and the stdlib UntrustedXMLParser
_SAFE_PARSE_ERRORS = ("EntitiesForbidden", "DtdForbidden", "ParseError", "ValueError")


@pytest.mark.asyncio
async def test_xxe_payload_is_defused():
    """
    Validates that the parser blocks external entity resolution,
    preventing file system leakage through service product parameters.
    """
    parser = NmapXmlParser()
    try:
        results = await parser.parse_string(MALICIOUS_XXE_XML)
        for finding in results:
            assert "root:" not in finding.service_product
            assert "&xxe;" not in finding.service_product
    except Exception as e:
        assert any(x in type(e).__name__ for x in _SAFE_PARSE_ERRORS), (
            f"Unexpected exception type: {type(e).__name__}: {e}"
        )


@pytest.mark.asyncio
async def test_malformed_port_handling():
    """
    Validates that non-integer port IDs are rejected before entering data structures.
    """
    parser = NmapXmlParser()
    with pytest.raises((ValueError, TypeError, ET.ParseError)):
        await parser.parse_string(MALFORMED_PORT_XML)


@pytest.mark.asyncio
async def test_billion_laughs_dos_protection():
    """
    Tests resilience against entity expansion loops (Billion Laughs DoS).
    """
    lol_xml = """<?xml version="1.0"?>
    <!DOCTYPE lolz [
     <!ENTITY lol "lol">
     <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
     <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
     <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
    ]>
    <nmaprun><host><ports><port portid="&lol3;"></port></ports></host></nmaprun>
    """
    parser = NmapXmlParser()
    with pytest.raises(Exception) as exc_info:
        await parser.parse_string(lol_xml)
    assert any(x in type(exc_info.value).__name__ for x in _SAFE_PARSE_ERRORS), (
        f"Unexpected exception type: {type(exc_info.value).__name__}: {exc_info.value}"
    )
