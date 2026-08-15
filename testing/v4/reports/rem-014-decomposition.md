# REM-014 OWL 2 DL Profile Decomposition

The earlier 7,287/7,289 figures were non-empty line counts. Multiline SPARQL annotation bodies inflated those totals. This decomposition counts only recognized ROBOT violation headers.

- C3 REM-014 baseline: **6,947**
- C5 REM-014 baseline: **6,949**
- C3 actual violations: **6,840**
- C5 actual violations: **6,842**
- C3 reduction from baseline: **-107**
- C5 reduction from baseline: **-107**
- C5 compatibility delta: **+2**

## Ownership

| Owner | C3 occurrences |
|---|---:|
| cac | 705 |
| shared-or-unattributed | 19 |
| upstream | 6,116 |

## Prioritized remediation units

| Priority | Root cause | Occurrences | Unique IRIs | Score |
|---:|---|---:|---:|---:|
| 1 | property-kind-punning | 2 | 1 | 40 |
| 2 | reserved-owl-vocabulary-as-domain-or-range | 6 | 1 | 32 |
| 3 | missing-or-invalid-first-party-declaration | 292 | 66 | 27 |
| 4 | unsupported-defined-datatype-literal | 14 | 1 | 21 |
| 5 | annotation-vocabulary-not-declared-for-owlapi | 412 | 19 | 15 |
| 6 | missing-or-invalid-upstream-declaration | 577 | 6 | 7 |
| 7 | embedded-shacl-vocabulary-not-declared-for-owlapi | 5,537 | 26 | 5 |

## Interpretation boundary

Ownership is inferred from the violated IRI and the axiom actor before the merged OntologyID suffix. `cac` findings are candidates for local repair. `upstream` findings remain pinned external evidence. `shared-or-unattributed` findings require source-level provenance before assignment. The unmodified full-import report remains authoritative.
