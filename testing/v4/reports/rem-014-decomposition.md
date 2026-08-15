# REM-014 OWL 2 DL Profile Decomposition

The earlier 7,287/7,289 figures were non-empty line counts. Multiline SPARQL annotation bodies inflated those totals. This decomposition counts only recognized ROBOT violation headers.

- C3 REM-014 baseline: **6,947**
- C5 REM-014 baseline: **6,949**
- C3 actual violations: **6,834**
- C5 actual violations: **6,836**
- C3 reduction from baseline: **-113**
- C5 reduction from baseline: **-113**
- C5 compatibility delta: **+2**

## Ownership

| Owner | C3 occurrences |
|---|---:|
| cac | 699 |
| shared-or-unattributed | 19 |
| upstream | 6,116 |

## Prioritized remediation units

| Priority | Root cause | Occurrences | Unique IRIs | Score |
|---:|---|---:|---:|---:|
| 1 | property-kind-punning | 2 | 1 | 40 |
| 2 | missing-or-invalid-first-party-declaration | 292 | 66 | 27 |
| 3 | unsupported-defined-datatype-literal | 14 | 1 | 21 |
| 4 | annotation-vocabulary-not-declared-for-owlapi | 412 | 19 | 15 |
| 5 | missing-or-invalid-upstream-declaration | 577 | 6 | 7 |
| 6 | embedded-shacl-vocabulary-not-declared-for-owlapi | 5,537 | 26 | 5 |

## Interpretation boundary

Ownership is inferred from the violated IRI and the axiom actor before the merged OntologyID suffix. `cac` findings are candidates for local repair. `upstream` findings remain pinned external evidence. `shared-or-unattributed` findings require source-level provenance before assignment. The unmodified full-import report remains authoritative.
