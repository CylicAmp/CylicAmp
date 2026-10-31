#!/usr/bin/env python3
"""
jpeg_provenance.py  --  JPEG container / C2PA / EXIF / XMP inspector.

Walks the JPEG marker stream and reports, without guessing:
  * every segment, with offset and length
  * APP11 (0xFFEB) JUMBF packets, reassembled, and any C2PA manifest store
  * APP1 EXIF (full IFD walk) and XMP / extended XMP packets
  * APP2 ICC_PROFILE
  * any DER X.509 certificates found inside the manifest, via `cryptography`

Usage:  python3 jpeg_provenance.py FILE.jpg [--dump-dir DIR]

Reports absence as absence. It never infers provenance that is not in the bytes.
"""
import sys, os, struct, json, hashlib, argparse

# markers that carry no length field
STANDALONE = {0xD8, 0xD9, 0x01} | set(range(0xD0, 0xD8))
NAMES = {
    0xD8: "SOI", 0xD9: "EOI", 0xDA: "SOS", 0xDB: "DQT", 0xC4: "DHT",
    0xDD: "DRI", 0xFE: "COM", 0xC0: "SOF0", 0xC1: "SOF1", 0xC2: "SOF2",
    0xC3: "SOF3", 0xC9: "SOF9", 0xCA: "SOF10", 0xCC: "DAC",
}
for i in range(16):
    NAMES[0xE0 + i] = f"APP{i}"


def segments(buf):
    """yield (marker, name, seg_offset, payload_bytes)."""
    n = len(buf)
    if n < 2 or buf[0] != 0xFF or buf[1] != 0xD8:
        raise ValueError("not a JPEG: missing SOI (FFD8)")
    i = 2
    yield 0xD8, "SOI", 0, b""
    while i < n - 1:
        if buf[i] != 0xFF:
            i += 1
            continue
        while i < n and buf[i] == 0xFF:
            i += 1
        if i >= n:
            break
        m = buf[i]
        off = i - 1
        i += 1
        if m in STANDALONE:
            yield m, NAMES.get(m, f"0x{m:02X}"), off, b""
            if m == 0xD9:
                return
            continue
        if i + 2 > n:
            return
        ln = struct.unpack(">H", buf[i:i + 2])[0]
        payload = buf[i + 2:i + ln]
        yield m, NAMES.get(m, f"0x{m:02X}"), off, payload
        i += ln
        if m == 0xDA:                      # entropy data: skip to next marker
            while i < n - 1:
                if buf[i] == 0xFF and buf[i + 1] not in (0x00,) and buf[i + 1] not in range(0xD0, 0xD8):
                    break
                i += 1


# ---------------------------------------------------------------- JUMBF / C2PA
def parse_boxes(data, depth=0, limit=64):
    """ISO BMFF-style box walk: LBox(4) TBox(4) [XLBox(8)] payload."""
    out, i = [], 0
    while i + 8 <= len(data) and len(out) < limit:
        lbox = struct.unpack(">I", data[i:i + 4])[0]
        tbox = data[i + 4:i + 8]
        hdr = 8
        if lbox == 1:
            if i + 16 > len(data):
                break
            lbox = struct.unpack(">Q", data[i + 8:i + 16])[0]
            hdr = 16
        elif lbox == 0:
            lbox = len(data) - i
        if lbox < hdr or i + lbox > len(data):
            out.append({"type": tbox.decode("latin1"), "error":
                        f"declared length {lbox} overruns {len(data) - i} available"})
            break
        body = data[i + hdr:i + lbox]
        box = {"type": tbox.decode("latin1"), "size": lbox, "offset": i}
        if tbox == b"jumb":
            box["children"] = parse_boxes(body, depth + 1)
        elif tbox == b"jumd":
            box.update(parse_jumd(body))
        else:
            box["payload_len"] = len(body)
            box["sha256"] = hashlib.sha256(body).hexdigest()[:32]
            box["_body"] = body
        out.append(box)
        i += lbox
    return out


def parse_jumd(body):
    """JUMBF description box: 16-byte type UUID, 1-byte toggles, optional label."""
    if len(body) < 17:
        return {"error": "jumd too short"}
    uuid, toggles = body[:16], body[16]
    info = {"content_uuid": uuid.hex(), "toggles": toggles}
    rest = body[17:]
    if toggles & 0x02:                      # label present, NUL-terminated
        z = rest.find(b"\x00")
        if z >= 0:
            info["label"] = rest[:z].decode("utf-8", "replace")
            rest = rest[z + 1:]
    if toggles & 0x04 and len(rest) >= 4:
        info["box_id"] = struct.unpack(">I", rest[:4])[0]
    return info


def app11_packets(segs):
    """Reassemble APP11 JUMBF: CI('JP') box-instance(2) packet-seq(4) then data."""
    streams, malformed = {}, []
    for m, name, off, p in segs:
        if m != 0xEB:
            continue
        if len(p) < 8:
            malformed.append((off, "APP11 shorter than 8 bytes"))
            continue
        ci = p[:2]
        if ci != b"JP":
            malformed.append((off, f"APP11 common identifier {ci!r}, expected b'JP'"))
            continue
        inst = struct.unpack(">H", p[2:4])[0]
        seq = struct.unpack(">I", p[4:8])[0]
        streams.setdefault(inst, []).append((seq, off, p[8:]))
    out = {}
    for inst, chunks in streams.items():
        chunks.sort()
        out[inst] = {
            "packets": [(s, o, len(d)) for s, o, d in chunks],
            "data": b"".join(d for _, _, d in chunks),
        }
    return out, malformed


# ---------------------------------------------------------------------- EXIF
EXIF_TAGS = {
    0x010F: "Make", 0x0110: "Model", 0x0131: "Software", 0x0132: "DateTime",
    0x013B: "Artist", 0x8298: "Copyright", 0x9003: "DateTimeOriginal",
    0x9004: "DateTimeDigitized", 0x927C: "MakerNote", 0xA430: "CameraOwnerName",
    0xA431: "BodySerialNumber", 0xA433: "LensMake", 0xA434: "LensModel",
    0x8769: "ExifIFDPointer", 0x8825: "GPSInfoIFDPointer", 0x0112: "Orientation",
    0x9286: "UserComment", 0x010E: "ImageDescription",
}
TYPE_SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 7: 1, 9: 4, 10: 8, 11: 4, 12: 8}


def parse_exif(payload):
    if not payload.startswith(b"Exif\x00\x00"):
        return None
    tiff = payload[6:]
    if len(tiff) < 8:
        return {"error": "TIFF header truncated"}
    bo = tiff[:2]
    if bo == b"II":
        e = "<"
    elif bo == b"MM":
        e = ">"
    else:
        return {"error": f"bad byte order {bo!r}"}
    magic, ifd0 = struct.unpack(e + "HI", tiff[2:8])
    if magic != 42:
        return {"error": f"bad TIFF magic {magic}"}
    out, seen = {"byte_order": "little" if e == "<" else "big", "ifds": {}}, set()

    def walk(off, label):
        if off in seen or off + 2 > len(tiff):
            return
        seen.add(off)
        cnt = struct.unpack(e + "H", tiff[off:off + 2])[0]
        entries = {}
        for k in range(cnt):
            b = off + 2 + k * 12
            if b + 12 > len(tiff):
                break
            tag, typ, num = struct.unpack(e + "HHI", tiff[b:b + 8])
            sz = TYPE_SIZE.get(typ, 0) * num
            if sz == 0:
                continue
            if sz <= 4:
                raw = tiff[b + 8:b + 8 + sz]
            else:
                vo = struct.unpack(e + "I", tiff[b + 8:b + 12])[0]
                raw = tiff[vo:vo + sz] if vo + sz <= len(tiff) else b""
            nm = EXIF_TAGS.get(tag, f"0x{tag:04X}")
            if typ == 2:
                val = raw.rstrip(b"\x00").decode("utf-8", "replace")
            elif typ == 3 and num == 1:
                val = struct.unpack(e + "H", raw[:2])[0]
            elif typ == 4 and num == 1:
                val = struct.unpack(e + "I", raw[:4])[0]
            elif typ == 7:
                val = f"<{len(raw)} bytes> {raw[:16].hex()}"
            else:
                val = f"<type {typ} x{num}> {raw[:16].hex()}"
            entries[nm] = val
            if nm in ("ExifIFDPointer", "GPSInfoIFDPointer") and isinstance(val, int):
                walk(val, nm)
        out["ifds"][label] = entries
        nxt_off = off + 2 + cnt * 12
        if nxt_off + 4 <= len(tiff):
            nxt = struct.unpack(e + "I", tiff[nxt_off:nxt_off + 4])[0]
            if nxt and label == "IFD0":
                walk(nxt, "IFD1")

    walk(ifd0, "IFD0")
    return out


XMP_SIG = b"http://ns.adobe.com/xap/1.0/\x00"
XMP_EXT_SIG = b"http://ns.adobe.com/xmp/extension/\x00"


def analyze(path, dump_dir=None):
    buf = open(path, "rb").read()
    print(f"FILE      {path}")
    print(f"SIZE      {len(buf):,} bytes")
    print(f"SHA256    {hashlib.sha256(buf).hexdigest()}")
    soi_ok = "JPEG SOI ok" if buf[:2] == b"\xff\xd8" else "NOT a JPEG"
    eoi_ok = "EOI ok" if buf[-2:] == b"\xff\xd9" else "no EOI at end"
    print(f"MAGIC     {buf[:4].hex()}  ({soi_ok})")
    print(f"TRAILER   {buf[-2:].hex()}  ({eoi_ok})")

    segs = list(segments(buf))
    print(f"\n--- MARKER STREAM ({len(segs)} segments) ---")
    for m, name, off, p in segs:
        extra = ""
        if m in (0xE0 + i for i in range(16)):
            sig = bytes(p[:32]).split(b"\x00")[0]
            extra = f"  sig={sig[:40]!r}"
        print(f"  @0x{off:08X}  {name:<6} len={len(p):<8}{extra}")

    # ---- C2PA / JUMBF
    print("\n--- C2PA / JUMBF (APP11, 0xFFEB) ---")
    streams, malformed = app11_packets(segs)
    for off, why in malformed:
        print(f"  MALFORMED @0x{off:08X}: {why}")
    if not streams:
        print("  ABSENT: no APP11 segment present.")
        print("  => no embedded C2PA manifest store in this file.")
    for inst, s in sorted(streams.items()):
        print(f"  box instance {inst}: {len(s['packets'])} packet(s), "
              f"{len(s['data']):,} bytes reassembled")
        boxes = parse_boxes(s["data"])
        def show(bs, d=2):
            for b in bs:
                pad = " " * d
                line = f"{pad}[{b['type']}] size={b.get('size')}"
                if "label" in b:
                    line += f" label={b['label']!r}"
                if "content_uuid" in b:
                    line += f" uuid={b['content_uuid']}"
                if "error" in b:
                    line += f" ERROR: {b['error']}"
                print(line)
                if "children" in b:
                    show(b["children"], d + 2)
        show(boxes)
        if dump_dir:
            os.makedirs(dump_dir, exist_ok=True)
            fp = os.path.join(dump_dir, f"jumbf_instance_{inst}.bin")
            open(fp, "wb").write(s["data"])
            print(f"    raw store written to {fp}")
        find_certs(s["data"])

    # ---- EXIF
    print("\n--- EXIF (APP1 'Exif\\0\\0') ---")
    found = False
    for m, name, off, p in segs:
        if m == 0xE1 and p.startswith(b"Exif\x00\x00"):
            found = True
            ex = parse_exif(p)
            if "error" in ex:
                print(f"  @0x{off:08X} ERROR: {ex['error']}")
                continue
            print(f"  @0x{off:08X} byte order: {ex['byte_order']}")
            for lbl, entries in ex["ifds"].items():
                print(f"    {lbl}:")
                for k, v in entries.items():
                    sv = str(v)
                    print(f"      {k:<22} {sv[:110]}")
    if not found:
        print("  ABSENT: no EXIF APP1 segment.")

    # ---- XMP
    print("\n--- XMP (APP1) ---")
    found = False
    for m, name, off, p in segs:
        if m != 0xE1:
            continue
        if p.startswith(XMP_SIG):
            found = True
            xml = p[len(XMP_SIG):].decode("utf-8", "replace")
            print(f"  @0x{off:08X} standard XMP, {len(xml)} chars")
            for key in ("xmp:CreatorTool", "xmp:ModifyDate", "xmp:CreateDate",
                        "photoshop:History", "stEvt:action", "stEvt:softwareAgent",
                        "dc:creator", "c2pa", "GCamera", "Composite"):
                if key in xml:
                    j = xml.find(key)
                    print(f"      contains {key!r}: ...{xml[max(0,j-40):j+120]}...")
            print("      ---- full packet ----")
            print("      " + xml.replace("\n", "\n      ")[:4000])
        elif p.startswith(XMP_EXT_SIG):
            found = True
            print(f"  @0x{off:08X} EXTENDED XMP, {len(p)-len(XMP_EXT_SIG)} bytes")
    if not found:
        print("  ABSENT: no XMP packet.")

    # ---- ICC
    print("\n--- ICC PROFILE (APP2) ---")
    icc = b"".join(p[14:] for m, nm, o, p in segs
                   if m == 0xE2 and p.startswith(b"ICC_PROFILE\x00"))
    if icc:
        print(f"  present, {len(icc):,} bytes; "
              f"desc tag search: {b'desc' in icc}")
        if len(icc) >= 128:
            print(f"  CMM={icc[4:8]!r} class={icc[12:16]!r} space={icc[16:20]!r} "
                  f"platform={icc[40:44]!r}")
    else:
        print("  ABSENT: no ICC profile.")


def find_certs(blob):
    """Scan a blob for DER X.509 certificates, using a stdlib-only parser.

    The `cryptography` package is deliberately NOT used: in some containers it
    imports but its native backend (_cffi_backend / _rust) is missing, which
    fails at parse time rather than import time. derx509 has no dependencies.
    """
    try:
        import derx509
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import derx509
    n, i = 0, 0
    while True:
        i = blob.find(b"\x30\x82", i)
        if i < 0:
            break
        try:
            info = derx509.parse_cert(blob[i:])
            n += 1
            print(f"    CERT @{i}  ({info['der_len']} bytes, v{info['version']})")
            print(f"      subject : {info['subject']}")
            print(f"      issuer  : {info['issuer']}")
            print(f"      valid   : {info.get('not_before')} .. {info.get('not_after')}")
            print(f"      serial  : {info['serial']}")
            print(f"      sig alg : {info.get('sig_alg')}")
            i += info["der_len"]
        except Exception:
            i += 2
    if n == 0:
        print("    no parseable X.509 certificate found in this store")
    return n



# =====================================================================
# SELF-TEST -- builds its own fixtures, asserts the parse, needs no input
# =====================================================================

def _box(t, payload):
    return struct.pack(">I", 8 + len(payload)) + t + payload


C2PA_UUID = bytes.fromhex("6332706100110010800000aa00389b71")


def _fixture_big_endian_exif(cert_der=b""):
    """APP11 first, big-endian EXIF, jumd toggles 0x03, bidb content box."""
    tags = [(0x010F, b"FixtureCam\x00"), (0x0110, b"Model-137\x00"),
            (0x0131, b"FixtureWriter 1.0\x00"), (0x0132, b"2026:10:13 00:00:00\x00")]
    n = len(tags)
    ifd_end = 8 + 2 + n * 12 + 4
    entries, data = b"", b""
    for tag, val in tags:
        if len(val) <= 4:
            entries += struct.pack(">HHI", tag, 2, len(val)) + val.ljust(4, b"\x00")
        else:
            entries += struct.pack(">HHII", tag, 2, len(val), ifd_end + len(data))
            data += val
    tiff = (b"MM" + struct.pack(">HI", 42, 8) + struct.pack(">H", n)
            + entries + struct.pack(">I", 0) + data)
    body = b"Exif\x00\x00" + tiff
    exif = b"\xff\xe1" + struct.pack(">H", len(body) + 2) + body

    xb = (b"http://ns.adobe.com/xap/1.0/\x00"
          b'<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF '
          b'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
          b'<rdf:Description xmlns:xmp="http://ns.adobe.com/xap/1.0/" '
          b'xmp:CreatorTool="FixtureWriter 1.0"/></rdf:RDF></x:xmpmeta>')
    xmp = b"\xff\xe1" + struct.pack(">H", len(xb) + 2) + xb

    store = _box(b"jumb", _box(b"jumd", C2PA_UUID + bytes([0x03]) + b"c2pa\x00")
                 + _box(b"bidb", cert_der))
    ap = b"JP" + struct.pack(">HI", 1, 1) + store
    app11 = b"\xff\xeb" + struct.pack(">H", len(ap) + 2) + ap

    dqt = b"\xff\xdb" + struct.pack(">H", 67) + b"\x00" + bytes([16] * 64)
    sof = (b"\xff\xc0" + struct.pack(">H", 11) + b"\x08"
           + struct.pack(">HH", 16, 16) + b"\x01\x01\x11\x00")
    sos = b"\xff\xda" + struct.pack(">H", 8) + b"\x01\x01\x00\x00\x3f\x00"
    return (b"\xff\xd8" + app11 + xmp + exif + dqt + sof + sos
            + b"\x12\x34\x56" + b"\xff\xd9")


def _fixture_little_endian_exif():
    """EXIF first, little-endian TIFF, jumd toggles 0x02, c2ma content box.
    Deliberately a different layout from the other fixture."""
    val = b"ProvenanceTest\x00"
    tiff = (b"II\x2a\x00\x08\x00\x00\x00" + struct.pack("<H", 1)
            + struct.pack("<HHI", 0x0131, 2, len(val)) + struct.pack("<I", 26)
            + struct.pack("<I", 0) + val)
    body = b"Exif\x00\x00" + tiff
    exif = b"\xff\xe1" + struct.pack(">H", len(body) + 2) + body

    xb = (b"http://ns.adobe.com/xap/1.0/\x00"
          b"<x:xmpmeta xmlns:x='adobe:ns:meta/'><rdf:RDF "
          b"xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'>"
          b"<rdf:Description xmlns:dc='http://purl.org/dc/elements/1.1/'>"
          b"<dc:creator><rdf:Seq><rdf:li>ExactValidator</rdf:li></rdf:Seq>"
          b"</dc:creator></rdf:Description></rdf:RDF></x:xmpmeta>")
    xmp = b"\xff\xe1" + struct.pack(">H", len(xb) + 2) + xb

    store = _box(b"jumb", _box(b"jumd", C2PA_UUID + bytes([0x02]) + b"c2pa\x00")
                 + _box(b"c2ma", b'{"claim_generator":"Exact_Engine_v1"}'))
    ap = b"JP" + struct.pack(">HI", 1, 1) + store
    app11 = b"\xff\xeb" + struct.pack(">H", len(ap) + 2) + ap

    dqt = b"\xff\xdb" + struct.pack(">H", 67) + b"\x00" + bytes([16] * 64)
    sof = b"\xff\xc0" + struct.pack(">H", 11) + b"\x08" + struct.pack(">HH", 8, 8) + b"\x01\x01\x11\x00"
    sos = b"\xff\xda" + struct.pack(">H", 8) + b"\x01\x01\x00\x00\x3f\x00"
    return b"\xff\xd8" + exif + xmp + app11 + dqt + sof + sos + b"\x00" + b"\xff\xd9"


def _system_certs():
    import sys as _s
    _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import derx509
    for p in ("/etc/ssl/certs/ca-certificates.crt",
              "/etc/pki/tls/certs/ca-bundle.crt"):
        if os.path.exists(p):
            return derx509.pem_to_ders(open(p).read()), p
    return [], None


def self_test():
    import sys as _s
    _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import derx509

    # 1. the DER parser against whatever real certificates this host has
    ders, src = _system_certs()
    if ders:
        ok = 0
        for d in ders:
            i = derx509.parse_cert(d)
            assert i["subject"] and i["issuer"] and i["not_after"], i
            ok += 1
        assert ok == len(ders)
        print(f"[ok] derx509: parsed all {ok} certificates in {src}")
    else:
        print("[skip] derx509: no system trust store found on this host")

    # 2. marker walk + JUMBF + EXIF + XMP on two DIFFERENT layouts
    cert = ders[0] if ders else b""
    for name, blob, want in (
        ("big-endian EXIF / bidb / toggles 0x03", _fixture_big_endian_exif(cert),
         {"endian": "big", "content": "bidb", "software": "FixtureWriter 1.0"}),
        ("little-endian EXIF / c2ma / toggles 0x02", _fixture_little_endian_exif(),
         {"endian": "little", "content": "c2ma", "software": "ProvenanceTest"}),
    ):
        segs = list(segments(blob))
        kinds = [s[1] for s in segs]
        assert kinds[0] == "SOI" and kinds[-1] == "EOI", kinds
        assert "APP11" in kinds and kinds.count("APP1") == 2, kinds

        streams, bad = app11_packets(segs)
        assert not bad, bad
        assert len(streams) == 1, streams.keys()
        boxes = parse_boxes(streams[1]["data"])
        assert len(boxes) == 1 and boxes[0]["type"] == "jumb", boxes
        kids = boxes[0]["children"]
        assert kids[0]["type"] == "jumd", kids
        assert kids[0]["label"] == "c2pa", kids[0]
        assert kids[0]["content_uuid"] == C2PA_UUID.hex(), kids[0]
        assert kids[1]["type"] == want["content"], kids[1]

        ex = None
        for m, nm, off, p in segs:
            if m == 0xE1 and p.startswith(b"Exif\x00\x00"):
                ex = parse_exif(p)
        assert ex and ex["byte_order"] == want["endian"], ex
        assert ex["ifds"]["IFD0"]["Software"] == want["software"], ex["ifds"]
        assert any(m == 0xE1 and p.startswith(XMP_SIG) for m, nm, o, p in segs)
        print(f"[ok] fixture: {name}")

    # 3. absence must report as absence, not as a finding
    bare = (b"\xff\xd8" + b"\xff\xdb" + struct.pack(">H", 67) + b"\x00"
            + bytes([16] * 64) + b"\xff\xd9")
    segs = list(segments(bare))
    streams, bad = app11_packets(segs)
    assert streams == {} and not bad, (streams, bad)
    assert not any(m == 0xE1 for m, nm, o, p in segs)
    print("[ok] absence: a bare JPEG yields no APP11, no EXIF, no XMP")

    # 4. a store with no certificate must NOT report one
    store = _box(b"jumb", _box(b"jumd", C2PA_UUID + bytes([0x02]) + b"c2pa\x00")
                 + _box(b"c2ma", b'{"claim_generator":"Trust DigiCert Adobe"}'))
    n = find_certs(store)
    assert n == 0, f"keyword-shaped content must not be reported as a certificate (got {n})"
    print("[ok] no false positives: 'Trust/DigiCert/Adobe' text is not a certificate")

    # 5. a malformed APP11 must be flagged, not silently parsed
    ap = b"XX" + struct.pack(">HI", 1, 1) + b"junk"
    seg = b"\xff\xeb" + struct.pack(">H", len(ap) + 2) + ap
    segs = list(segments(b"\xff\xd8" + seg + b"\xff\xd9"))
    streams, bad = app11_packets(segs)
    assert streams == {} and len(bad) == 1, (streams, bad)
    print("[ok] malformed APP11 (wrong common identifier) is reported, not parsed")

    print("\nAll self-tests passed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?", help="JPEG to inspect")
    ap.add_argument("--dump-dir", help="write raw JUMBF stores here")
    ap.add_argument("--self-test", action="store_true",
                    help="build fixtures and verify the parser; needs no input file")
    a = ap.parse_args()
    if a.self_test:
        self_test()
    elif a.file:
        analyze(a.file, a.dump_dir)
    else:
        ap.error("give a FILE, or --self-test")
