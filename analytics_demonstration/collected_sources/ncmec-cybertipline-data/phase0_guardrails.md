# Phase 0 Guardrails — ncmec-cybertipline-data

**Chunk:** C2.A1  
**Mode:** single-document Path A  
**caseId:** `ncmec-cybertipline-data`  
**Declared example path:** `examples_knowledge_graphs/ncmec-cybertipline-data-example.ttl`  
**Collected (UTC):** 2026-07-19T05:03:58Z  

## Working assumptions (locked for C2.A2)

1. Source is **public high-level** NCMEC aggregate CyberTipline statistics (not a prosecution press release, not investigative holdings).
2. **IN_SCOPE** for domain modeling of program, reporting flows, aggregate metrics, partnerships, and high-level legal citations present on page.
3. **No new classes/properties by default** — Phase 3 skipped unless a later governance gate proves a strict gap.
4. Prefer **reuse** from `cacontology-us-ncmec`, hotlines, platforms, partnerships, international, taskforce, plus UCO/CASE foundations.
5. Prefer **statement/listing Actions** for aggregate statistics rather than synthesizing millions of individual tip instances.
6. Instance IRIs: **UUIDv5** under document namespace `3163ddce-323b-5805-b7d2-89b277787002`.
7. Evidence pointers: `normalized.txt` keypoint numbers (1–54).
8. Domain ABox typing uses existing domain/UCO/CASE classes (not bare `cac-core:` instance types).
9. Interactive chart values that render as empty/zero in HTML scrape are **not** evidence.
10. Company names appear only as NCMEC public transparency statements; model carefully with provenance; no defamation-style expansion.
11. Suicide aggregate awareness statement may be modeled only if grounded and privacy-safe (aggregate, no identifiers); may omit if connectivity cost exceeds signal.
12. Do not commit `testing/c*` or `docker-compose.override.yml`.

## Scope confirmation

| Decision | Value |
|---|---|
| Scope status | **IN_SCOPE** |
| Boundary status | Public only; no CSAM content; no individual case PII |
| Path A filter | -1 → 0 → 1 → 2 → **skip 3** → 4 → (5 optional) → 6 → 7 |

## Candidate modules (ceiling, not commitment)

Primary: `cacontology-us-ncmec`, `cacontology-hotlines`, `cacontology-platforms`, `cacontology-partnerships`, `cacontology-international`, `cacontology-taskforce`.  
Secondary if text-grounded: detection, sextortion, sex-trafficking, sadistic-online-exploitation, ai-csam, prevention.

## Quality gate status (C2.A1)

| Gate | Status |
|---|---|
| Public high-level source selected | PASS |
| Duplicate detection complete | PASS — proceed |
| Clean text produced | PASS — `source.txt` + `normalized.txt` |
| Provenance meta complete (URL, time, method, performer, hashes) | PASS — `manifest.yaml` |
| caseId frozen | PASS — `ncmec-cybertipline-data` |
| Scope decision recorded | PASS — IN_SCOPE |
| No ontology/example TTL generated yet | PASS (deferred to C2.A2) |
