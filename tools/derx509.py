"""Minimal stdlib-only DER / X.509 reader. No cffi, no OpenSSL bindings."""
import struct

OIDS = {
    "2.5.4.3": "CN", "2.5.4.6": "C", "2.5.4.7": "L", "2.5.4.8": "ST",
    "2.5.4.10": "O", "2.5.4.11": "OU", "2.5.4.5": "serialNumber",
    "1.2.840.113549.1.9.1": "email", "2.5.4.4": "SN", "2.5.4.42": "GN",
    "1.2.840.113549.1.1.11": "sha256WithRSAEncryption",
    "1.2.840.113549.1.1.1": "rsaEncryption",
    "1.2.840.10045.4.3.2": "ecdsa-with-SHA256",
    "1.2.840.10045.2.1": "id-ecPublicKey",
    "1.3.101.112": "Ed25519",
}


def read_tlv(b, i):
    """return (tag, header_len, length, value_start, next_index)"""
    if i >= len(b):
        raise ValueError("truncated")
    tag = b[i]
    j = i + 1
    if j >= len(b):
        raise ValueError("truncated length")
    n = b[j]
    j += 1
    if n & 0x80:
        k = n & 0x7F
        if k == 0 or j + k > len(b):
            raise ValueError("bad long form length")
        n = int.from_bytes(b[j:j + k], "big")
        j += k
    if j + n > len(b):
        raise ValueError("length overruns buffer")
    return tag, j - i, n, j, j + n


def children(b, start, end):
    i = start
    while i < end:
        tag, hl, ln, vs, nxt = read_tlv(b, i)
        yield tag, vs, vs + ln, nxt
        i = nxt


def decode_oid(b):
    if not b:
        return ""
    first = b[0]
    parts = [str(first // 40), str(first % 40)]
    val = 0
    for byte in b[1:]:
        val = (val << 7) | (byte & 0x7F)
        if not byte & 0x80:
            parts.append(str(val))
            val = 0
    return ".".join(parts)


def decode_time(tag, b):
    s = b.decode("ascii", "replace")
    if tag == 0x17:                      # UTCTime YYMMDDHHMMSSZ
        yy = int(s[:2])
        year = 2000 + yy if yy < 50 else 1900 + yy
        rest = s[2:]
    else:                                # GeneralizedTime YYYYMMDD...
        year = int(s[:4])
        rest = s[4:]
    return f"{year:04d}-{rest[0:2]}-{rest[2:4]} {rest[4:6]}:{rest[6:8]}:{rest[8:10]}Z"


def decode_name(b, start, end):
    """Name ::= SEQUENCE OF SET OF AttributeTypeAndValue"""
    out = []
    for _t, rs, re_, _n in children(b, start, end):          # each RDN (SET)
        for _t2, as_, ae, _n2 in children(b, rs, re_):       # AttributeTypeAndValue
            kids = list(children(b, as_, ae))
            if len(kids) < 2:
                continue
            (_, os_, oe, _), (vt, vs, ve, _) = kids[0], kids[1]
            oid = decode_oid(b[os_:oe])
            val = b[vs:ve].decode("utf-8", "replace")
            out.append(f"{OIDS.get(oid, oid)}={val}")
    return ", ".join(out)


def parse_cert(der):
    """returns dict with serial, issuer, subject, not_before, not_after, sig_alg."""
    tag, hl, ln, vs, nxt = read_tlv(der, 0)
    if tag != 0x30:
        raise ValueError("certificate is not a SEQUENCE")
    top = list(children(der, vs, vs + ln))
    if len(top) < 3:
        raise ValueError("certificate SEQUENCE has too few members")
    _, ts, te, _ = top[0]                                    # tbsCertificate
    tbs = list(children(der, ts, te))
    k = 0
    info = {"version": 1}
    if tbs and tbs[0][0] == 0xA0:                            # [0] version
        vkids = list(children(der, tbs[0][1], tbs[0][2]))
        if vkids:
            info["version"] = int.from_bytes(der[vkids[0][1]:vkids[0][2]], "big") + 1
        k = 1
    info["serial"] = int.from_bytes(der[tbs[k][1]:tbs[k][2]], "big"); k += 1
    algk = list(children(der, tbs[k][1], tbs[k][2]))
    if algk:
        info["sig_alg"] = OIDS.get(decode_oid(der[algk[0][1]:algk[0][2]]),
                                   decode_oid(der[algk[0][1]:algk[0][2]]))
    k += 1
    info["issuer"] = decode_name(der, tbs[k][1], tbs[k][2]); k += 1
    vkids = list(children(der, tbs[k][1], tbs[k][2]))
    if len(vkids) >= 2:
        info["not_before"] = decode_time(der[vkids[0][1] - 2], der[vkids[0][1]:vkids[0][2]])
        info["not_after"] = decode_time(der[vkids[1][1] - 2], der[vkids[1][1]:vkids[1][2]])
    k += 1
    info["subject"] = decode_name(der, tbs[k][1], tbs[k][2])
    info["der_len"] = nxt
    return info


def pem_to_ders(text):
    import base64
    out, buf, inb = [], [], False
    for line in text.splitlines():
        if "BEGIN CERTIFICATE" in line:
            inb, buf = True, []
        elif "END CERTIFICATE" in line:
            if buf:
                out.append(base64.b64decode("".join(buf)))
            inb = False
        elif inb:
            buf.append(line.strip())
    return out
