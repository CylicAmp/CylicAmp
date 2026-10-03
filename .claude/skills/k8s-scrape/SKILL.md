---
name: k8s-scrape
description: Configure and debug Prometheus scraping in Kubernetes — PodMonitor, ServiceMonitor, and native kubernetes_sd_configs. Use when metrics are not appearing, a PodMonitor produces zero targets, a scrape fails, or a scrape config needs writing or reviewing. Walks the selector chain from the Prometheus CR down to the container port and reports an explicit four-state diagnosis (ZERO TARGETS / TARGET DOWN / UP-DATA-WRONG / HEALTHY) with the layer and the next check, because every link in that chain fails silently.
---

# k8s-scrape

Every selector in this chain fails **silently**. A mismatch produces zero
targets, no error, and a healthy-looking object. Walk the chain in order.

```
python3 .claude/skills/k8s-scrape/audit.py chain prom.yaml podmonitor.yaml deploy.yaml
python3 .claude/skills/k8s-scrape/audit.py classify "0 targets"
python3 .claude/skills/k8s-scrape/audit.py relabel-check config.yaml
```

## The chain

```
Prometheus.spec.podMonitorSelector      <- PodMonitor.metadata.labels
Prometheus.spec.podMonitorNamespaceSelector <- PodMonitor namespace
PodMonitor.spec.namespaceSelector       <- workload namespace
PodMonitor.spec.selector                <- pod LABELS (never annotations)
podMetricsEndpoints[].port              <- containers[].ports[].name
                                        -> listener actually bound
                                        -> /metrics responds
                                        -> Prometheus can reach the pod IP
```

Defaults that bite:

- `PodMonitor.spec.namespaceSelector` omitted → **the PodMonitor's own namespace only**
- `spec.selector: {}` → matches **every** pod in scope, not none
- `ContainerPort.name` is unique **per pod**, IANA_SVC_NAME, **max 15 chars**
- kube-prometheus-stack defaults `podMonitorSelector` to `release: <helm-release>`

## Four states, never collapsed

| State | Layer | Investigate |
|---|---|---|
| ZERO TARGETS | discovery | selectors, namespaces, port name |
| TARGET DOWN | transport | address, port, path, scheme, TLS, auth, listener |
| UP / DATA WRONG | ingestion | metricRelabelings, sample/label/target limits |
| UP / DATA CORRECT | — | healthy |

Report the state, the layer, and the next check. Never emit
"Prometheus scrape failed" — that discards the diagnosis.

## Two invariants

```
PodMonitor discovery  !=  network exposure
metricRelabelings     cannot repair a discovery failure
```

A PodMonitor creates no Service and opens no port. Keeping `:9100` off the
Service and Ingress keeps it off the VIP; only NetworkPolicy restricts who may
connect to the pod IP.

`relabelings` act on the **target** (`__address__`, `__metrics_path__`,
`__meta_kubernetes_*`). `metricRelabelings` act on **already-scraped samples**.
Annotation path rewrite belongs in the first.

## Native SD, when Prometheus is not Operator-managed

The port rewrite needs **both** source labels — `;` is the separator between
them, so a single-label form can never match and is a silent no-op:

```yaml
- source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
  action: replace
  target_label: __address__
  regex: ([^:]+)(?::\d+)?;(\d+)
  replacement: $1:$2
```

Raw config uses `source_labels` / `target_label`. The CRD uses `sourceLabels` /
`targetLabel`. A snake_case relabeling inside a PodMonitor is rejected by schema
validation.

## Which control plane

```
kubectl get crd podmonitors.monitoring.coreos.com
```

Present → Operator owns the config; raw `scrape_configs` in a ConfigMap are
regenerated and lost. Absent → native config is the artifact. Never maintain
both for the same target.

## Version-dependent, do not assume

- The generated scrape configuration is **Operator-managed**. How and where it
  is stored varies by version and configuration; do not prescribe a particular
  Secret as the inspection point, and never hand-edit it to fix a PodMonitor.
- `port` / `portNumber` / `targetPort` precedence and mutual exclusivity depend
  on the installed CRD schema. Set exactly one. Do not assume the name wins.
- Available auth fields (`authorization`, `basicAuth`, `oauth2`,
  `bearerTokenSecret`) depend on the CRD version. Check the installed schema.

## PodMonitor vs ServiceMonitor

| | PodMonitor | ServiceMonitor |
|---|---|---|
| selects | pods | Services → Endpoints |
| needs a Service | no | yes |
| port field | container port **name** | Service port **name** |
| use for | private metrics port | metrics behind a ClusterIP |

## Terminology — four distinct things

| Term | Meaning |
|---|---|
| Pod | workload instance |
| endpoint configuration | one `podMetricsEndpoints[]` entry — a template, not a destination |
| target | resolved Pod + endpoint = a concrete scrape identity |
| sample | one datum returned by a scrape of a target |

```
target T = (Pod P, endpoint config E, resolved params R)
R = address + port + path + scheme + auth/TLS + target labels
```

An endpoint configuration is **not** a target; it participates in building many.

## Cardinality — conditional, not a product

```
T = { (P, e, rho(P,e))  |  P in P_M,  e in E(P),  R(P,e) }
|T| = sum over P in P_M of |{ e in E(P) : R(P,e) }|
```

`|T| = |P| x |E|` holds **only** when every selected pod is eligible, every
pod has the same applicable endpoint set, every endpoint resolves for every
pod, and nothing is filtered afterwards. A single Deployment satisfies the
second condition — all replicas share one template — so the product is valid
there and `audit.py` uses it, saying so. A DaemonSet across heterogeneous
nodes, or two workloads under one selector, does not.

`targetLimit` bounds `|T|` — not pods, not endpoint configs.

## Two axes, never one status

```
Discovery State   ABSENT | PRESENT           was a target generated?
Scrape State      N/A | FAILED | SUCCEEDED   given one, did the scrape work?
Data State        N/A | LIMITED | ACCEPTED   what happened to the samples?

D = ABSENT  =>  S = N/A          a nonexistent target cannot fail to scrape
```

**Zero targets is an outcome, not a cause.** Always report the cause class:

```
selection    Prometheus does not adopt the PodMonitor, or namespace/label
             selection matched nothing
eligibility  pod matched but is not eligible for this endpoint
resolution   pod and endpoint matched but the named port does not resolve
constraint   candidates were generated then rejected by targetLimit
```

`audit.py chain` emits the full record — SELECTION / ENDPOINT RESOLUTION /
TARGET GENERATION with candidate and generated counts — so "3 pods selected,
0 targets generated, cause: resolution" is never reported as "no pods found".

Target identity is `T = (P, E, rho)`. The address `10.42.1.17:9100` is the
target's **resolved address**, not its whole identity; two endpoint configs
can resolve to one address with different paths.

## Which limit acts where

| Mechanism | Unit | Stage | Failure |
|---|---|---|---|
| `selector`, `namespaceSelector` | pods, namespaces | discovery | zero targets |
| `targetLimit` | targets | target generation | target-limit exceeded |
| `port` (named) | endpoint | target generation | wrong or missing target |
| `path`, `scheme` | endpoint | scrape | HTTP / TLS failure |
| `scrapeTimeout` | one scrape | scrape | context deadline exceeded |
| `interval` | one target | scheduling | — |
| `metricRelabelings` | samples | post-scrape | series dropped or renamed |
| `sampleLimit` | samples | scrape/ingestion boundary | too many samples |
| `labelLimit`, label name/value limits | sample labels | ingestion | rejected labels |

```
scrapeTimeout  = time allowed to OBTAIN the response
sampleLimit    = samples permitted FROM that response
targetLimit    = how many targets may exist at all
```

HTTP 200 does not mean every sample was ingested. A timeout is a transport
failure, not an ingestion one. Availability of individual fields is CRD-version
dependent.

## Failure vocabulary

| Avoid | Use |
|---|---|
| "endpoint failed" | target is down |
| "no endpoint" | zero targets were generated |
| "endpoint limit" | target limit, or name the specific endpoint constraint |
| "PodMonitor is down" | PodMonitor generated zero targets |
| "Prometheus can't find the endpoint" | Prometheus has no matching target |
| "metrics failed" | scrape failed, or samples were limited |

`audit.py classify` emits the state, the layer, and the ordered checks, and
refuses to cross layers: no relabeling advice while zero targets exist, no
selector advice once discovery has succeeded.
