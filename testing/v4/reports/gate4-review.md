# CAC v4 Foundational Proposal — Gate 4.1 Implementation Review

**Recommendation:** **Advance the local candidate to Gate 4.2 publication review, while retaining HOLD on any v4.0.0 release claim.**

Gate 4.1 is complete on the dedicated issue-44 proposal branch. All accepted first-party semantic, datatype, and vocabulary policies are implemented and regression-controlled. The unmodified full-import closure still does not satisfy the normative OWL 2 DL gate, but the recognized C3/C5 remainder is now entirely attributable to pinned upstream dependencies. This is a reviewable foundational proposal, not a release artifact.

No GitHub mutation occurred during Gate 4.1.

## Source identity

| Item | Value |
|---|---|
| Frozen base | `93de063951b758dd68a27611638c177fcf910eab` (`v3.1.0`) |
| Sealed source candidate | `3dbea97053b8fd212b1ff14cfd531cd7415d43cf` |
| Candidate tree | `9ab6e3cae18cdc2a5bf06d632d6abfe075330388` |
| Branch | `proposal/issue-44-v4-foundational-architecture` |
| DCO status | All 31 local commits from the frozen base contain sign-off trailers |
| Pre-existing unsigned commits reported by the manifest | 0 |
| Tracked source dirty during final evidence run | No |
| GitHub publication | Gate 4.2 authorized; not yet pushed at evidence time |

## Gate 4.1 acceptance outcome

| Control | Result |
|---|---|
| C3 architecture, asserted/RDFS | Pass/pass; 0 findings |
| C4 architecture, asserted/RDFS | Pass/pass; 0 findings |
| C5 architecture, asserted/RDFS | Pass/pass; 0 findings |
| Executable tests | Pass; 91/91 |
| Import closure | Pass; 75/75 resolved, 0 remote gaps |
| Locked Turtle dependencies | Pass; 28/28 parse |
| Proposal-owned SHACL SPARQL syntax | Pass; 0 failures |
| Diagnostic HermiT projections | Pass for C3, C4, and C5 |
| C3 strict profile | 6,116 findings: 0 CAC, 0 shared, 6,116 upstream |
| C5 strict profile | 6,116 findings: 0 CAC, 0 shared, 6,116 upstream |
| C4 strict ingestion | Upstream failure before classification due to malformed exact-profile RDF structures |
| Normative full-import OWL 2 DL | HOLD; upstream/tool-route blockers remain |

## Implemented policy surface

1. Applied all twenty reviewed semantic mapping families, including event/role direction, qualified participation, lifecycle, record/classifier, service/device/call, norm/artifact, planning-artifact, phone-account/facet, and temporal-ordering corrections.
2. Replaced unsupported normative `xsd:duration` and `xsd:gYear` usage with the approved lexical-string and integer-year policies while preserving all fourteen existing duration values exactly.
3. Added positive and negative SHACL fixtures for datatype behavior and structured phone-account traces.
4. Added bounded SKOS/DCMI declarations with content-addressed authoritative snapshots; no uncontrolled full standards import was introduced.
5. Centralized the six CAC design-note predicates as annotation properties and removed literal-valued `skos:exactMatch` assertions.
6. Regenerated the dependency lock, architecture reports, strict-profile reports, REM-014 decomposition, and complete regression transcript.
7. Canonicalized first-party text hashing so Git-equivalent LF and CRLF checkouts produce identical dependency identities.

## Measured REM-014 result

- C3 moved from 6,947 to 6,116 recognized findings: **831 removed**.
- C5 moved from 6,949 to 6,116 recognized findings: **833 removed**.
- C3 CAC-owned findings moved from 812 to **0**.
- C3 shared/header findings moved from 19 to **0**.
- The 6,116 upstream-owned findings did not change.
- C3 and C5 now have exact parity; the compatibility artifact adds no strict-profile finding.

## Preserved boundaries and residual risks

- The exact pinned dependency bytes were not edited.
- C3/C5 HermiT strict reasoning still encounters imported SWRL built-ins unsupported by the pinned route.
- The exact profile still contains malformed OWL/RDF structures that block C4 OWLAPI ingestion.
- Diagnostic projections demonstrate bounded CAC coherence but are not represented as normative full-import conformance.
- PR #48 and issue/PR #46 remain outside this Gate 4.1 change.
- The exhaustive post-v4 remediation charter remains active for upstream coordination, tooling alternatives, documentation, and future findings.

## Gate 4.2 boundary

Gate 4.2 authorizes pushing the dedicated issue-44 branch and opening one draft PR after DCO and identity-sensitive controls pass. It does not authorize a release claim, merge, tag, or modification of PR #48 or issue/PR #46.
