# REM-014 OWL 2 DL Profile Decomposition

The earlier 7,287/7,289 figures were non-empty line counts. Multiline SPARQL annotation bodies inflated those totals. This decomposition counts only recognized ROBOT violation headers.

- C3 REM-014 baseline: **6,947**
- C5 REM-014 baseline: **6,949**
- C3 actual violations: **6,926**
- C5 actual violations: **6,928**
- C3 reduction from baseline: **-21**
- C5 reduction from baseline: **-21**
- C5 compatibility delta: **+2**

## Ownership

| Owner | C3 occurrences |
|---|---:|
| cac | 790 |
| shared-or-unattributed | 19 |
| upstream | 6,117 |

## Prioritized remediation units

| Priority | Root cause | Occurrences | Unique IRIs | Score |
|---:|---|---:|---:|---:|
| 1 | property-kind-punning | 29 | 10 | 40 |
| 2 | class-used-as-datatype | 25 | 7 | 40 |
| 3 | reserved-owl-vocabulary-as-domain-or-range | 6 | 1 | 32 |
| 4 | missing-or-invalid-first-party-declaration | 326 | 82 | 27 |
| 5 | unsupported-defined-datatype-literal | 14 | 1 | 21 |
| 6 | annotation-vocabulary-not-declared-for-owlapi | 412 | 19 | 15 |
| 7 | missing-or-invalid-upstream-declaration | 577 | 6 | 7 |
| 8 | embedded-shacl-vocabulary-not-declared-for-owlapi | 5,537 | 26 | 5 |

## Interpretation boundary

Ownership is inferred from the violated IRI and the axiom actor before the merged OntologyID suffix. `cac` findings are candidates for local repair. `upstream` findings remain pinned external evidence. `shared-or-unattributed` findings require source-level provenance before assignment. The unmodified full-import report remains authoritative.
