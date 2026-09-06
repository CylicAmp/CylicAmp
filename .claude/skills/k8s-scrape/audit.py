#!/usr/bin/env python3
"""
Walk the Prometheus Operator selector chain and report where it breaks.

    audit.py chain <prometheus.yaml> <podmonitor.yaml> <workload.yaml>
    audit.py classify "<symptom>"
    audit.py relabel-check <scrape-config.yaml>

Every link in the chain fails silently. This reports which one.
"""
import sys, re, yaml

OK, BAD, WARN = "  ok  ", " FAIL ", " warn "


def _sel_matches(selector, labels):
    """metav1.LabelSelector semantics. Empty selector matches EVERYTHING."""
    if not selector:
        return True, "empty selector matches ALL objects in scope"
    ml = selector.get('matchLabels') or {}
    for k, v in ml.items():
        if labels.get(k) != v:
            return False, f"label {k}={v!r} not on object (has {labels.get(k)!r})"
    for e in selector.get('matchExpressions') or []:
        k, op, vals = e.get('key'), e.get('operator'), e.get('values') or []
        have = labels.get(k)
        if op == 'In' and have not in vals:
            return False, f"{k}={have!r} not in {vals}"
        if op == 'NotIn' and have in vals:
            return False, f"{k}={have!r} is in {vals}"
        if op == 'Exists' and k not in labels:
            return False, f"{k} absent"
        if op == 'DoesNotExist' and k in labels:
            return False, f"{k} present"
    return True, ""


def _iana(name):
    if not (1 <= len(name) <= 15):
        return False, f"length {len(name)}, must be 1..15"
    if not re.fullmatch(r'[a-z0-9-]+', name):
        return False, "chars outside [a-z0-9-]"
    if not re.search(r'[a-z]', name):
        return False, "must contain a letter"
    if name[0] == '-' or name[-1] == '-':
        return False, "leading/trailing hyphen"
    if '--' in name:
        return False, "consecutive hyphens"
    return True, ""


def chain(prom_f, pm_f, wl_f):
    prom, pm, wl = (yaml.safe_load(open(f)) for f in (prom_f, pm_f, wl_f))
    L, fails, warns, limitfail = [], [], [], None
    A = L.append
    A("=" * 70); A("SELECTOR CHAIN"); A("=" * 70)

    pm_labels = pm.get('metadata', {}).get('labels') or {}
    pm_ns = pm.get('metadata', {}).get('namespace') or 'default'
    pspec = prom.get('spec', {})

    # 1 Prometheus -> PodMonitor
    ok, why = _sel_matches(pspec.get('podMonitorSelector'), pm_labels)
    A(f"{OK if ok else BAD} 1  Prometheus.podMonitorSelector -> PodMonitor.labels")
    A(f"        selector {pspec.get('podMonitorSelector')}")
    A(f"        labels   {pm_labels}")
    if not ok:
        A(f"        {why}"); fails.append("PodMonitor not selected by Prometheus")
    elif not pspec.get('podMonitorSelector'):
        A(f"        {why} — every PodMonitor in scope is used")
        warns.append("Prometheus.podMonitorSelector is empty: it adopts EVERY PodMonitor")

    # 2 Prometheus -> PodMonitor namespace
    nss = pspec.get('podMonitorNamespaceSelector')
    if nss is None:
        A(f"{WARN} 2  podMonitorNamespaceSelector absent -> Prometheus' own namespace only")
        A(f"        PodMonitor is in {pm_ns!r}; confirm Prometheus is too")
    else:
        A(f"{OK} 2  podMonitorNamespaceSelector {nss} (PodMonitor ns {pm_ns!r})")

    # 3 PodMonitor -> workload namespace
    wl_ns = wl.get('metadata', {}).get('namespace') or 'default'
    pnss = pm.get('spec', {}).get('namespaceSelector')
    if pnss is None:
        ok3 = (wl_ns == pm_ns)
        A(f"{OK if ok3 else BAD} 3  namespaceSelector ABSENT -> defaults to the "
          f"PodMonitor's own namespace {pm_ns!r}")
        A(f"        workload is in {wl_ns!r}")
        if not ok3:
            fails.append(f"workload ns {wl_ns!r} outside PodMonitor ns {pm_ns!r}")
    elif pnss.get('any'):
        A(f"{OK} 3  namespaceSelector any:true -> all namespaces")
    else:
        names = pnss.get('matchNames') or []
        ok3 = wl_ns in names
        A(f"{OK if ok3 else BAD} 3  namespaceSelector matchNames {names}, workload ns {wl_ns!r}")
        if not ok3:
            fails.append(f"workload ns {wl_ns!r} not in {names}")

    # 4 PodMonitor -> pod labels
    tmpl = wl.get('spec', {}).get('template', {})
    pod_labels = tmpl.get('metadata', {}).get('labels') or {}
    pod_annos = tmpl.get('metadata', {}).get('annotations') or {}
    psel = pm.get('spec', {}).get('selector')
    ok4, why4 = _sel_matches(psel, pod_labels)
    A(f"{OK if ok4 else BAD} 4  PodMonitor.selector -> pod LABELS")
    A(f"        selector {psel}")
    A(f"        pod labels {pod_labels}")
    if not ok4:
        A(f"        {why4}"); fails.append("pod labels do not match PodMonitor.selector")
    elif not psel:
        A(f"        {why4} — this is the cardinality hazard, not a no-op")
        warns.append("PodMonitor.selector is empty: EVERY pod in scope becomes a target")
    for k in pod_annos:
        if any(k == mk for mk in (psel or {}).get('matchLabels', {})):
            A(f"{BAD}    {k!r} is an ANNOTATION; selectors read labels only")
            fails.append(f"{k} is an annotation, not a label")

    # 5 endpoint port -> named container port
    ports = {}
    for c in tmpl.get('spec', {}).get('containers') or []:
        for p in c.get('ports') or []:
            if 'name' in p:
                ports.setdefault(p['name'], []).append((c.get('name'), p.get('containerPort')))
    A(f"{OK} 5  named container ports: "
      + ", ".join(f"{n}->{v[0][1]}" for n, v in ports.items()))
    for n, occ in ports.items():
        good, why = _iana(n)
        if not good:
            A(f"{BAD}    port name {n!r} invalid: {why}")
            fails.append(f"port name {n!r} invalid")
        if len(occ) > 1:
            A(f"{BAD}    port name {n!r} declared {len(occ)}x; names are unique PER POD")
            fails.append(f"duplicate port name {n!r}")
    for i, ep in enumerate(pm.get('spec', {}).get('podMetricsEndpoints') or []):
        setfields = [f for f in ('port', 'portNumber', 'targetPort') if f in ep]
        if len(setfields) > 1:
            A(f"{BAD}    endpoint[{i}] sets {setfields}; set exactly one "
              f"(precedence is CRD-version dependent)")
            fails.append(f"endpoint[{i}] sets {setfields}")
        pn = ep.get('port')
        if pn is not None:
            ok5 = pn in ports
            A(f"{OK if ok5 else BAD}    endpoint[{i}].port {pn!r} "
              f"{'-> containerPort ' + str(ports[pn][0][1]) if ok5 else 'NOT DECLARED on any container'}")
            if not ok5:
                fails.append(f"no container port named {pn!r}")
            elif pn != 'metrics' and ep.get('path', '/metrics') == '/metrics':
                A(f"{WARN}    endpoint[{i}] scrapes {pn!r} (containerPort "
                  f"{ports[pn][0][1]}) at /metrics — is that the metrics port, "
                  f"or the app port?")
                warns.append(f"endpoint[{i}] targets port {pn!r}, not 'metrics'; "
                             f"a target WILL be generated against the wrong port")
        A(f"        path {ep.get('path', '/metrics (default)')}  "
          f"scheme {ep.get('scheme', 'http (default)')}  "
          f"interval {ep.get('interval', 'global (default)')}")

    # 6 cardinality vs targetLimit
    reps = wl.get('spec', {}).get('replicas')
    eps = pm.get('spec', {}).get('podMetricsEndpoints') or []
    tl = pm.get('spec', {}).get('targetLimit')
    A("")
    A(f"{OK} 6  cardinality")
    if reps is None:
        A(f"        replicas not set in the manifest (defaults to 1)")
        reps = 1
    A(f"        N_P (replicas)           {reps}")
    A(f"        N_E (endpoint configs)   {len(eps)}")
    A(f"        N_T ~ N_P x N_E          {reps * len(eps)}   target candidates")
    if tl is None:
        A(f"        targetLimit unset — no cap on generated targets")
    else:
        okt = reps * len(eps) <= tl
        A(f"{OK if okt else BAD}       targetLimit {tl}"
          f" vs {reps * len(eps)} candidates")
        if not okt:
            limitfail = (f"{reps*len(eps)} target candidates exceed targetLimit {tl}")
    A(f"        note: targetLimit bounds TARGETS, not pods and not endpoint configs")

    A("")
    A("=" * 70)
    if limitfail and not fails:
        A("STATUS: TARGET LIMIT EXCEEDED")
        A("LAYER:  TARGET GENERATION")
        A("NEXT CHECK: " + limitfail)
        A("        The selector chain is intact — pods match and the port resolves.")
        A("        This is not a discovery mismatch and not a scrape failure.")
        A("        Raise targetLimit, reduce replicas, or drop an endpoint config.")
    elif fails:
        A("STATUS: ZERO TARGETS")
        A("LAYER:  DISCOVERY")
        A("NEXT CHECK: " + fails[0])
        for f in fails[1:]:
            A("     also: " + f)
        if limitfail:
            A("     also: " + limitfail + "  (TARGET GENERATION layer)")
    elif warns:
        A("STATUS: TARGET GENERATED, BUT SUSPECT")
        A("LAYER:  DISCOVERY (chain resolves; the result is probably not what you want)")
        for w in warns:
            A("  ! " + w)
        A("NOTE:   these produce targets, so the symptom is not '0 targets'.")
        A("        It is wrong-port scrapes or runaway cardinality.")
    else:
        A("STATUS: chain intact — discovery should produce a target")
        A("LAYER:  next failures would be TRANSPORT (listener, path, scheme,")
        A("        network, TLS/auth) then INGESTION (metricRelabelings, limits)")
        A("NOTE:   a PodMonitor opens no port. Exposure is Service/Ingress/NetworkPolicy.")
    return "\n".join(L)


STATES = {
    'zero': ("ZERO TARGETS", "DISCOVERY",
             ["Prometheus.podMonitorSelector vs PodMonitor.metadata.labels",
              "podMonitorNamespaceSelector vs PodMonitor namespace",
              "PodMonitor.namespaceSelector vs workload namespace",
              "PodMonitor.selector vs pod LABELS (not annotations)",
              "podMetricsEndpoints[].port vs containers[].ports[].name"]),
    'down': ("TARGET DOWN", "TRANSPORT",
             ["target address and resolved port",
              "path and scheme",
              "is a process actually bound (ss -lnt in the container)",
              "curl 127.0.0.1:<port><path> from inside the pod",
              "pod-network reachability, NetworkPolicy",
              "TLS and auth; referenced Secret namespace"]),
    'wrong': ("TARGET UP / DATA WRONG", "INGESTION",
              ["metricRelabelings dropping or renaming series",
               "sampleLimit / labelLimit / targetLimit",
               "cardinality from broad labelmap; prefer podTargetLabels allowlist",
               "two Prometheus CRs with overlapping podMonitorSelector"]),
}


def classify(sym):
    s = sym.lower()
    key = ('zero' if ('0 target' in s or 'zero' in s or 'no target' in s or 'not appear' in s)
           else 'down' if ('down' in s or 'refus' in s or 'timeout' in s or 'fail' in s)
           else 'wrong' if ('missing' in s or 'wrong' in s or 'cardinal' in s)
           else None)
    if not key:
        return ("cannot classify from that symptom. Say which of:\n"
                "  no target generated / target exists but scrape fails /"
                " target up but series wrong")
    st, layer, checks = STATES[key]
    out = [f"STATUS: {st}", f"LAYER:  {layer}", "CHECK IN ORDER:"]
    out += [f"  {i+1}. {c}" for i, c in enumerate(checks)]
    if key != 'zero':
        out.append("\nDo not touch selectors — discovery already succeeded.")
    else:
        out.append("\nDo not touch relabelings or the exporter — no target exists yet.")
    return "\n".join(out)


def relabel_check(path):
    cfg = yaml.safe_load(open(path))
    L = ["relabel_configs audit"]
    jobs = cfg.get('scrape_configs') or []
    for j in jobs:
        L.append(f"\njob {j.get('job_name')!r}")
        for i, r in enumerate(j.get('relabel_configs') or []):
            src = r.get('source_labels') or []
            rx = r.get('regex', '')
            bad = ';' in str(rx) and len(src) < 2
            L.append(f"  [{i}] action={r.get('action','replace')} "
                     f"source_labels={src} regex={rx!r}")
            if bad:
                L.append(f"       FAIL regex contains ';' (the separator BETWEEN "
                         f"source labels) but only {len(src)} label given.")
                L.append(f"       This never matches. A non-matching rule is a "
                         f"SILENT no-op, not an error.")
            for k in r:
                if k in ('sourceLabels', 'targetLabel'):
                    L.append(f"       FAIL {k}: raw config uses snake_case "
                             f"(source_labels / target_label)")
    return "\n".join(L)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__); sys.exit(1)
    if a[0] == 'chain':
        print(chain(a[1], a[2], a[3]))
    elif a[0] == 'classify':
        print(classify(a[1]))
    elif a[0] == 'relabel-check':
        print(relabel_check(a[1]))
    else:
        print(__doc__); sys.exit(1)
