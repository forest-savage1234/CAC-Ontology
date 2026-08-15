# CAC v4 Foundational Proposal — Gate 4 Review

**Recommendation:** **HOLD the strict release gate; retain the candidate for remediation and maintainer review. The candidate is published only as a draft in the contributor's personal fork.**

Gate 4 is now executed against the exact UCO gUFO Profile revision and a content-addressed runtime import closure. The candidate's bounded architecture is coherent in all gated diagnostic configurations, but the unmodified full import closure does not satisfy the normative OWL 2 DL gate. This is a foundational proposal under issue #44, not a v4.0.0 release artifact.

## Source identity

| Item | Value |
|---|---|
| Frozen base | `93de063951b758dd68a27611638c177fcf910eab` (`v3.1.0`) |
| Clean evidence candidate | `129fc1f1efe772e8eac5a2a9be4c819d5f7af49a` |
| Candidate tree | `96a78e3dbacc941936111a8f7ce5b61311508c64` |
| Local commits from base | 19 |
| Missing DCO sign-offs | 0 |
| Tracked source dirty during evidence run | No |
| Detection-shape file changed | No |
| GitHub publication | Contributor-fork draft only; no upstream mutation |

## Evidence outcome

| Configuration/layer | Result | Meaning |
|---|---|---|
| C1 frozen v3.1 asserted baseline | Observed: 148 findings | Preserved baseline evidence, not a v4 failure |
| C2 v3.1 + exact profile | Asserted: 263; RDFS: 271 findings | Baseline overlay demonstrates the pre-v4 incompatibility |
| C3 v4 architecture | Asserted/RDFS pass: 0 findings | Proposed architecture satisfies the bounded diagnostics |
| C4 v4 + exact profile | Asserted/RDFS pass: 0 findings | Exact profile overlay does not restore the diagnosed level conflicts |
| C5 v4 + bounded compatibility | Asserted/RDFS pass: 0 findings | Compatibility axioms do not restore the diagnosed conflation |
| Executable unit/fixture tests | Pass: 58/58 | Original Gate 4 controls plus REM-014 decomposition and repair regressions pass |
| Embedded SHACL SPARQL | 459 audited; 0 proposal failures | Seven failures remain isolated to the untouched detection shapes owned by PR #48 |
| Dependency closure | Pass: 75/75 imports resolved | 48 local and 27 vendored resolutions; zero unresolved imports |
| Dependency Turtle syntax | Pass: 27/27 locked Turtle artifacts | Every content-addressed Turtle artifact in the runtime closure parses |
| Exact profile OWL/RDF structures | Fail upstream: 8 findings | Four malformed negative assertions and four malformed reified axioms block OWLAPI |
| HermiT diagnostic projections | Pass: C3, C4, C5 | No remaining named-class/property incoherence in the bounded projections |
| Strict full-closure OWL 2 DL | Fail: C3, C4, C5 | Normative gate remains unsatisfied |

## Gate 4 repairs completed locally

- Vendored and hashed the exact UCO gUFO Profile and its runtime dependency closure, including exact UCO, CDO-Shapes-gufo, Collections, SPAR Error, CASE, and W3C SHACL artifacts.
- Added pinned Java 21 and ROBOT 1.9.10 runtime evidence and deterministic strict-profile report compression.
- Corrected five CAC bridge metadata records that were malformed as incomplete `owl:Axiom` resources.
- Removed the UCO object/inherent-characterization contradiction from the CAC perceptual-hash classes.
- Corrected property alignments whose domains, ranges, or inverse direction forced bottom properties under the profile.
- Corrected 28 exact-profile class-category collisions across hotline, evidence, production, taskforce, and victim-impact branches.
- Added regression controls for hash categories, OWLAPI structures, profile category compatibility, and property coherence.

## Strict blockers preserved for remediation

1. REM-014 established true C3/C5 baselines of 6,947 and 6,949 recognized ROBOT violation headers; the earlier 7,287/7,289 figures counted multiline report text. The first repair slice removed 21 CAC-owned single-operand equivalence violations, producing current totals of 6,926/6,928. The remaining findings are decomposed in `rem-014-decomposition.*`; strict OWL 2 DL conformance is not yet claimed.
2. The exact UCO gUFO Profile contains eight malformed OWL/RDF structures. These cause the C4 strict profile and HermiT routes to fail before logical classification.
3. The pinned UCO profile makes `uco-action:phase` a subproperty of `uco-action:subaction` while their inherited range categories are disjoint, producing an upstream bottom-property condition.
4. The pinned Collections ontology contains SWRL built-in atoms unsupported by the selected HermiT execution route, blocking strict C3/C5 classification through that route.
5. The seven detection-shape SPARQL findings remain external to this branch and require PR #48 integration or maintainer disposition.

The diagnostic projection removes only explicitly inventoried upstream/tooling blockers to isolate logical root causes. Its pass is evidence that the repaired CAC candidate is coherent under that bounded projection; it is not a substitute for the strict gate.

## Gate decision

Gate 4 is **complete as an evaluation** and **HOLD as a release decision**. The candidate, dependency closure, tests, reasoner results, and remediation records are ready for continued work. Later authorization permitted publication as a draft in the contributor's personal fork; Project VIC's upstream repository remains untouched.
