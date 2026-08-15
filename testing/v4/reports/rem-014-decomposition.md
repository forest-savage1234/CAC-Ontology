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

| Priority | Root cause | Scope | CAC occurrences | Total occurrences | Unique IRIs | Score |
|---:|---|---|---:|---:|---:|---:|
| 1 | missing-local-declaration | cac-actionable | 75 | 75 | 37 | 36 |
| 2 | invalid-or-version-mismatched-external-reference | cac-actionable | 120 | 120 | 25 | 30 |
| 3 | unsupported-xsd-datatype-policy | cac-actionable | 68 | 68 | 2 | 21 |
| 4 | unsupported-defined-datatype-literal | cac-actionable | 14 | 14 | 1 | 21 |
| 5 | unimported-shared-vocabulary | cac-actionable | 29 | 29 | 2 | 18 |
| 6 | annotation-vocabulary-not-declared-for-owlapi | cac-actionable | 393 | 412 | 19 | 15 |
| 7 | embedded-shacl-vocabulary-not-declared-for-owlapi | external | 0 | 5,537 | 26 | 0 |
| 8 | missing-or-invalid-upstream-declaration | external | 0 | 577 | 6 | 0 |
| 9 | property-kind-punning | external | 0 | 2 | 1 | 0 |

## Interpretation boundary

Ownership is inferred from the violated IRI and the axiom actor before the merged OntologyID suffix. `cac` findings are candidates for local repair. `upstream` findings remain pinned external evidence. `shared-or-unattributed` findings require source-level provenance before assignment. The unmodified full-import report remains authoritative.
