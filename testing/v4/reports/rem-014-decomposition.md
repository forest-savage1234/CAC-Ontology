# REM-014 OWL 2 DL Profile Decomposition

The earlier 7,287/7,289 figures were non-empty line counts. Multiline SPARQL annotation bodies inflated those totals. This decomposition counts only recognized ROBOT violation headers.

- C3 REM-014 baseline: **6,947**
- C5 REM-014 baseline: **6,949**
- C3 actual violations: **6,761**
- C5 actual violations: **6,763**
- C3 reduction from baseline: **-186**
- C5 reduction from baseline: **-186**
- C5 compatibility delta: **+2**

## Ownership

| Owner | C3 occurrences |
|---|---:|
| cac | 626 |
| shared-or-unattributed | 19 |
| upstream | 6,116 |

## Prioritized remediation units

| Priority | Root cause | Scope | CAC occurrences | Total occurrences | Unique IRIs | Score |
|---:|---|---|---:|---:|---:|---:|
| 1 | invalid-or-version-mismatched-external-reference | cac-actionable | 120 | 120 | 25 | 30 |
| 2 | unsupported-xsd-datatype-policy | cac-actionable | 68 | 68 | 2 | 21 |
| 3 | unsupported-defined-datatype-literal | cac-actionable | 14 | 14 | 1 | 21 |
| 4 | unimported-shared-vocabulary | cac-actionable | 31 | 31 | 2 | 18 |
| 5 | annotation-vocabulary-not-declared-for-owlapi | cac-actionable | 393 | 412 | 19 | 15 |
| 6 | embedded-shacl-vocabulary-not-declared-for-owlapi | external | 0 | 5,537 | 26 | 0 |
| 7 | missing-or-invalid-upstream-declaration | external | 0 | 577 | 6 | 0 |
| 8 | property-kind-punning | external | 0 | 2 | 1 | 0 |

## Interpretation boundary

Ownership is inferred from the violated IRI and the axiom actor before the merged OntologyID suffix. `cac` findings are candidates for local repair. `upstream` findings remain pinned external evidence. `shared-or-unattributed` findings require source-level provenance before assignment. The unmodified full-import report remains authoritative.
