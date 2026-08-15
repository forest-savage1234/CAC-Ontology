# CAC v4 Foundational Proposal — Gate 4 Review

**Recommendation:** **HOLD for missing normative evidence; do not publish or open a GitHub PR yet.**

The approved local Gate 3 implementation is complete through Slices 1–8. The architecture corrections, consumer contracts, bounded compatibility layer, tests, and evidence generator are committed on `proposal/issue-44-v4-foundational-architecture`. This is a foundational proposal under issue #44, not a v4.0.0 release artifact.

## Source identity

| Item | Value |
|---|---|
| Frozen base | `93de063951b758dd68a27611638c177fcf910eab` (`v3.1.0`) |
| Evidence candidate | `b7a88c45c1bd7a0243c6f4c4f3959bbe9253685d` |
| Local commits | 15 |
| Missing DCO sign-offs | 0 |
| Tracked source dirty during evidence run | No |
| Detection-shape file changed | No |
| GitHub mutation | None |

## Evidence outcome

| Configuration/layer | Result | Meaning |
|---|---|---|
| C1 frozen v3.1 asserted baseline | Observed: 148 findings | Preserved baseline evidence, not a v4 failure |
| C2 v3.1 + pinned UCO gUFO overlay | Blocked | Exact profile bytes unavailable |
| C3 v4 asserted diagnostics | Pass: 0 findings | Proposed asserted architecture satisfies implemented diagnostics |
| C3 v4 RDFS diagnostics | Pass: 0 findings | RDFS closure does not restore a forbidden overlap |
| C4 v4 + pinned UCO gUFO overlay | Blocked | Same unavailable profile bytes as C2 |
| C5 v4 + bounded compatibility, asserted | Pass: 0 findings | Safe compatibility axioms do not restore conflation |
| C5 RDFS diagnostics | Pass: 0 findings | Compatibility remains clean under RDFS closure |
| Executable unit/fixture tests | Pass: 40/40 | Positive, negative, consumer, syntax, ledger, and closure controls pass |
| Term disposition ledger | Pass: 299 reviewed, 0 pending | Every in-scope candidate has a recorded disposition |
| Embedded SHACL SPARQL | 459 audited; 0 proposal failures | Seven remaining failures are confined to the untouched detection module owned by PR #48 |

## What was built

- Operational role records are separated from bearer classifiers through `RoleRecord` and `RoleAssignment`.
- Operational phase/state occurrences are separated from `gufo:Phase` classifiers and support repeated history.
- Custodial relationships and arrangements are separated from `CustodyState` occurrences.
- `MembershipTier` is a controlled concept without unsafe operational domains.
- Reviewed role, phase, enduring, and event terms have explicit, tested dispositions.
- SHACL `SELECT`, `ASK`, and `CONSTRUCT` bodies are repository-audited; 99 non-detection syntax failures discovered during QC were repaired (40 direct constraints and 59 rule bodies).
- JSON-LD and SPARQL consumer contracts are executable against synthetic fixtures.
- The v3 compatibility artifact contains only one-way, deprecated custody-property bridges and no class equivalence.

## Blocking evidence still required

1. Resolve all 13 remote-only imports through an approved catalog and record byte length, final target, SHA-256, retrieval date, and source/license note.
2. Obtain the exact UCO gUFO Profile artifacts at commit `4b98b9881aa29ed80f39b589d15725fa696c921a`; run C2 and C4 with those locked bytes.
3. Run an approved ROBOT/HermiT OWL 2 DL profile, consistency, classification, and unsatisfiable-named-class check for C3, C4, and C5. Java and ROBOT are absent, and the installed Docker client has no running engine, so no OWL 2 DL result is claimed.
4. After PR #48 merges, rebase this branch and require the detection-module query findings to fall from 7 to 0 without duplicating #48’s commits.
5. Re-run the complete evidence generator on the rebased, dependency-locked tree and obtain maintainer Gate 4 publication approval.

## Gate decision

The local proposal is ready for technical review as a coherent implementation, but it is **not release-ready and not publication-authorized**. Applicable local evidence is green; missing deterministic closure, overlay, and OWL 2 DL evidence remain hard release blockers under the approved charter.
