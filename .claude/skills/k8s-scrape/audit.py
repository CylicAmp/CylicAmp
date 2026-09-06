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
    cause = None   # selection | eligibility | resolution | limit
    elig_eps, resolved_eps = [], []
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
        cause = cause or "selection (Prometheus does not adopt this PodMonitor)"
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
            fails.append(f"workload ns {wl_ns!r} outside PodMonitor ns {pm_ns!r}"); cause = cause or "selection (namespace)"
    elif pnss.get('any'):
        A(f"{OK} 3  namespaceSelector any:true -> all namespaces")
    else:
        names = pnss.get('matchNames') or []
        ok3 = wl_ns in names
        A(f"{OK if ok3 else BAD} 3  namespaceSelector matchNames {names}, workload ns {wl_ns!r}")
        if not ok3:
            fails.append(f"workload ns {wl_ns!r} not in {names}"); cause = cause or "selection (namespace)"

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
        cause = cause or "selection (labels)"
    elif not psel:
        A(f"        {why4} — this is the cardinality hazard, not a no-op")
        warns.append("PodMonitor.selector is empty: EVERY pod in scope becomes a target")
    for k in pod_annos:
        if any(k == mk for mk in (psel or {}).get('matchLabels', {})):
            A(f"{BAD}    {k!r} is an ANNOTATION; selectors read labels only")
            fails.append(f"{k} is an annotation, not a label"); cause = cause or "selection (labels)"

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
            cause = cause or "resolution"
            elig_eps.append(True); resolved_eps.append(False)
            continue
        pn = ep.get('port')
        if pn is None:
            A(f"{WARN}    endpoint[{i}] is not port-name based ({setfields or 'no port field'})")
            elig_eps.append(True); resolved_eps.append(bool(setfields))
        else:
            # ELIGIBILITY: can a port-name endpoint apply to this pod at all?
            elig = bool(ports)
            elig_eps.append(elig)
            if not elig:
                A(f"{BAD}    endpoint[{i}] port {pn!r}: pod declares NO named ports")
                A(f"           -> ELIGIBILITY failure: a name-based endpoint cannot")
                A(f"              apply to a pod with no named ports. Nothing to resolve.")
                fails.append(f"endpoint[{i}] ineligible: pod has no named ports")
                cause = cause or "eligibility"
                resolved_eps.append(False)
            else:
                ok5 = pn in ports
                resolved_eps.append(ok5)
                A(f"{OK if ok5 else BAD}    endpoint[{i}].port {pn!r} eligible; "
                  + (f"resolves -> containerPort {ports[pn][0][1]}" if ok5
                     else f"RESOLUTION failure: {pn!r} not among {sorted(ports)}"))
                if not ok5:
                    fails.append(f"endpoint[{i}] unresolved: no port named {pn!r}")
                    cause = cause or "resolution"
                elif pn != 'metrics' and ep.get('path', '/metrics') == '/metrics':
                    A(f"{WARN}    endpoint[{i}] scrapes {pn!r} (containerPort "
                      f"{ports[pn][0][1]}) at /metrics — metrics port, or app port?")
                    warns.append(f"endpoint[{i}] targets port {pn!r}, not 'metrics'; "
                                 f"a target WILL be generated against the wrong port")
        A(f"        path {ep.get('path', '/metrics (default)')}  "
          f"scheme {ep.get('scheme', 'http (default)')}  "
          f"interval {ep.get('interval', 'global (default)')}")

    # 6 cardinality — CONDITIONAL, not an unconditional product
    reps = wl.get('spec', {}).get('replicas')
    eps = pm.get('spec', {}).get('podMetricsEndpoints') or []
    tl = pm.get('spec', {}).get('targetLimit')
    if reps is None:
        reps = 1
    n_elig = sum(1 for r in elig_eps if r)
    n_res = sum(1 for r in resolved_eps if r)
    cand = reps * len(eps)
    gen = reps * n_res
    A("")
    A(f"{OK} 6  target generation")
    A(f"        |P| matching pods        {reps}   (one Deployment template, so E(P)")
    A(f"                                       is identical for every replica —")
    A(f"                                       the product form is valid here)")
    A(f"        |E| endpoint configs     {len(eps)}")
    A(f"        of which eligible        {n_elig}")
    A(f"        of which resolved        {n_res}")
    A(f"        candidate targets        {cand}")
    A(f"        generated targets        {gen}")
    if tl is None:
        A(f"        targetLimit unset")
    else:
        okt = gen <= tl
        A(f"{OK if okt else BAD}       targetLimit {tl} vs {gen} generated")
        if not okt:
            limitfail = f"{gen} generated targets exceed targetLimit {tl}"
            cause = cause or "target-generation constraint"

    A("")
    A("=" * 70)
    if fails or limitfail:
        A("DISCOVERY STATE:  ABSENT" if gen == 0 or fails
          else "DISCOVERY STATE:  CONSTRAINED")
        A(f"DISCOVERY CAUSE:  {cause}")
        A("")
        A("  SELECTION")
        A(f"    PodMonitor selected by Prometheus : "
          f"{'no' if cause and cause.startswith('selection') and 'not selected' in (fails[0] if fails else '') else 'yes'}")
        sel_fail = bool(cause) and cause.startswith("selection")
        A(f"    pods matched                      : {0 if sel_fail else reps}")
        A("  ENDPOINT ELIGIBILITY")
        A(f"    {n_elig} of {len(eps)} endpoint configs applicable to the selected pods")
        A("  ENDPOINT RESOLUTION")
        for i, ep in enumerate(eps):
            e = elig_eps[i] if i < len(elig_eps) else None
            r = resolved_eps[i] if i < len(resolved_eps) else None
            st = ("resolved" if r else
                  "INELIGIBLE" if e is False else
                  "eligible, UNRESOLVED")
            A(f"    endpoint[{i}] port {ep.get('port')!r:<16} {st}")
        A("  TARGET GENERATION")
        c_eff, g_eff = (0, 0) if sel_fail else (cand, gen)
        A(f"    candidates {c_eff}   generated {g_eff}"
          + (f"   targetLimit {tl}" if tl is not None else ""))
        A("")
        A("SCRAPE STATE:     NOT APPLICABLE")
        A("DATA STATE:       NOT APPLICABLE")
        A("")
        A("NEXT CHECK: " + (fails[0] if fails else limitfail))
        for f in fails[1:]:
            A("     also: " + f)
        if limitfail and fails:
            A("     also: " + limitfail + "  (target-generation constraint)")
        A("")
        if limitfail and not fails:
            A(f"  {gen} targets WERE generated; the constraint rejected the population.")
            A("  That is a target-generation outcome, not a selector mismatch.")
        else:
            A("  zero targets is the OUTCOME. The cause above is the layer to fix.")
    elif warns:
        A("DISCOVERY STATE:  PRESENT, BUT SUSPECT")
        A(f"  generated targets {gen}")
        for w in warns:
            A("  ! " + w)
        A("SCRAPE STATE:     unknown from manifests — targets exist, check live")
        A("DATA STATE:       not evaluable until the scrape succeeds")
    else:
        A("DISCOVERY STATE:  PRESENT")
        A(f"  candidates {cand}, generated {gen}")
        A("SCRAPE STATE:     unknown from manifests")
        A("    next failures: listener bound, path, scheme, network, TLS/auth,")
        A("    scrapeTimeout — all TRANSPORT, none fixable by a selector edit")
        A("DATA STATE:       not evaluable until the scrape succeeds")
        A("    then: metricRelabelings, sampleLimit, labelLimit, cardinality")
        A("NOTE: a PodMonitor opens no port. Exposure is Service/Ingress/NetworkPolicy.")
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
