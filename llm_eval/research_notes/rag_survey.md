# RAG Techniques — Research Survey Notes

## 1. Chunking Strategies for Code Completion RAG

**Finding:** Function-level chunking is suboptimal for code RAG.
Sliding window and cAST (context-aware AST) strategies outperform it.
Cross-file context length is a significant performance variable.

**Implication for llm_eval:**
The `context` dict passed to each invariant in `InvariantExecutionKernel`
needs to carry chunk-boundary metadata. An invariant could penalise
transitions where the retrieved chunk truncates a function mid-body.

---

## 2. CAR — Confidence-Aware Reranking

**Method:** Query-guided, training-free reranking framework.
Ranks candidate documents by estimating the generator's confidence
*change* when each document is added. Higher confidence delta → higher rank.
No training required; operates on the live model.

**Implication for llm_eval:**
The `integrity_delta` field in `ContractDecision` is already the right
primitive. CAR's confidence-change score maps directly onto it:
a retrieved document that increases generator confidence should reduce
the violation count and push `integrity_delta` toward zero.
`EvidenceDebtManager` could weight debt by inverse CAR score.

---

## 3. PG-RAG — Political Knowledge Graph + GNN

**Method:** Graph Neural Networks fused with LLMs.
A political knowledge graph encodes inter-entity relationships
(MPs, parties, votes, policies). GNN propagates relational signals;
LLM handles generation. Applied to ideology prediction of Swiss MPs.

**Finding:** Inter-entity relationship information is essential;
flat document retrieval misses structural signals.

**Implication for llm_eval:**
`CategoryStats.manifold_distance_mean` is currently a proxy scalar.
A GNN over the invariant dependency graph would give a proper
manifold distance — violations that cluster in related invariants
signal higher systemic risk than isolated failures.

---

## 4. DoGMaTiQ — Automatic QA Nugget Generation

**Method:** Decomposes reports into atomic fact QA nuggets.
Each nugget = one verifiable claim + question + expected answer.
Nuggets are assessed for coverage in cross-lingual evaluation settings.
Improves evaluation automation and granularity over holistic scoring.

**Implication for llm_eval:**
DoGMaTiQ's atomic-fact decomposition is the natural input format for
`EvidenceDebtManager`. Each nugget is an evidence unit; failing to
cover a nugget increments debt in the `compliance` bucket.
`CategoryStats.sample_size` should count nuggets, not full documents.

---

## Connection Map

```
CAR confidence delta  →  ContractDecision.integrity_delta
DoGMaTiQ nuggets      →  EvidenceDebtManager evidence units
PG-RAG GNN distance   →  CategoryStats.manifold_distance_mean (replace proxy)
Chunking strategy     →  context dict chunk metadata invariant
```
