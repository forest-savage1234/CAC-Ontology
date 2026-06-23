# Contribution prep — CaseLinker state machine extensions

Local checklist only. Complete before opening a PR to Project VIC. **No git actions required to use this file.**

## What you are contributing

| Module | New terms |
|--------|-----------|
| `cacontology-sextortion` | `CoercionCycle` + 4 properties |
| `cacontology-platforms` | `PlatformAffordance` (+ 8 subclasses), `ChannelMigrationEvent`, `AffordanceMisuse` |
| `cacontology-grooming` | `AccountReplacementEvent` + 4 properties |

Supporting: SHACL shapes, example TTL/JSON-LD, SPARQL query, optional Python SDK, unit tests.

## Documentation hygiene (done in this branch)

- [x] `CHANGELOG.md` — `[Unreleased]` entry
- [x] `docs/glossary.md` — new classes and key properties
- [x] `docs/user_doc.md` — usage section with IRIs and validation commands
- [x] `contexts/cacontology-{sextortion,platforms,grooming,state-machine-extensions}.jsonld`
- [x] `example_SPARQL_queries/caselinker-state-machine-analytics.rq`
- [x] `testing/shacl_validation.py` — domain cross-checks for example graph

## Validation checklist (run locally)

```bash
cd /path/to/CAC-Ontology
python3 -m venv .venv && source .venv/bin/activate
pip install rdflib pyshacl

# 1. Full SHACL suite (must be 0 failures)
python testing/shacl_validation.py

# 2. State-machine unit tests (8 tests)
python testing/test_state_machine_extensions.py -v

# 3. Per-module example validation
python -m pyshacl -s ontology/cacontology-sextortion-shapes.ttl \
  -d examples_knowledge_graphs/caselinker-state-machine-extensions-example.ttl
python -m pyshacl -s ontology/cacontology-platforms-shapes.ttl \
  -d examples_knowledge_graphs/caselinker-state-machine-extensions-example.ttl
python -m pyshacl -s ontology/cacontology-grooming-shapes.ttl \
  -d examples_knowledge_graphs/caselinker-account-replacement-example.ttl

# 4. Optional: ROBOT syntax check (if installed)
# robot validate --input ontology/cacontology-sextortion.ttl
# robot validate --input ontology/cacontology-platforms.ttl
# robot validate --input ontology/cacontology-grooming.ttl

# 5. Optional: Docker validation (CONTRIBUTING.md)
# cd testing && docker compose up -d && docker compose run pyshacl
```

Record results here before PR:

| Check | Pass? | Notes |
|-------|-------|-------|
| `shacl_validation.py` | Yes | 158 pass / 0 fail |
| `test_state_machine_extensions.py` | Yes | 8/8 |
| Example vs sextortion shapes | Yes | `caselinker-state-machine-extensions-example.ttl` |
| Example vs platforms shapes | Yes | same file |
| Example vs grooming shapes | Yes | `caselinker-account-replacement-example.ttl` (separate file avoids cross-module Phase shape conflicts) |
| `cac-core:precedes` SHACL | Yes | **New property** in `cacontology-core-spine.ttl` (not on main before this branch); shapes in `cacontology-core-shapes.ttl` |
| Module JSON-LD contexts | Yes | `contexts/cacontology-{sextortion,platforms,grooming}.jsonld` |
| ROBOT (optional) | | See below |

## Before you commit (your steps — not done by agent)

1. `git checkout -b feat/caselinker-state-machine-extensions`
2. `git add` only contribution files (review `git status` — exclude `.cursor/`, local secrets)
3. Commit with conventional message, e.g.:

```
feat: add CaseLinker state machine offense trajectory classes

- Add CoercionCycle, ChannelMigrationEvent, AffordanceMisuse, AccountReplacementEvent
- SHACL shapes, example KG, JSON-LD context, SPARQL analytics query
- Optional Python SDK bindings and unit tests
```

4. Add DCO sign-off line to commit body:

```
Signed-off-by: Your Name <your.email@example.com>
```

## PR description draft (fill in when ready)

**Title:** `feat: add CaseLinker state machine offense trajectory classes`

**Summary:**
- Closes gap for cyclic sextortion leverage (`CoercionCycle`)
- Cross-platform migration as typed event (`ChannelMigrationEvent`)
- Transition-level platform affordance annotation (`AffordanceMisuse`)
- Post-ban account reset (`AccountReplacementEvent`)

**Motivation:** CaseLinker maps ICAC case features to a formal exploitation state machine; these four constructs were missing from CAC.

**Validation:** pyshacl 158/158 pass; unit tests 8/8. ROBOT validation not run (not installed locally).

**Note for reviewers:** `coercionCycleDemandType` is intentionally separate from `ExtortionDemand.demandType`. `cac-core:precedes` is a **new** spine property introduced in this PR (git blame: commit `1a9deca`); prior ordering used module-local properties (`transitionsTo`, `temporallyPrecedes`, `precedesPhase`). UCO/CASE define no equivalent. `sdk/python/` is optional — happy to drop or relocate per project preference.

## Files touched (review `git diff`)

**Ontology:** `ontology/cacontology-sextortion.ttl`, `ontology/cacontology-platforms.ttl`, `ontology/cacontology-grooming.ttl`, `ontology/cacontology-core-spine.ttl`, matching `*-shapes.ttl` (including `cacontology-core-shapes.ttl`)

**Examples:** `examples_knowledge_graphs/caselinker-state-machine-extensions-example.ttl`, `examples_knowledge_graphs/caselinker-account-replacement-example.ttl`, `examples_knowledge_graphs/jsonld/*.jsonld`

**Docs:** `CHANGELOG.md`, `docs/glossary.md`, `docs/user_doc.md`

**Other:** `contexts/`, `example_SPARQL_queries/`, `sdk/python/`, `testing/test_state_machine_extensions.py`, `testing/shacl_validation.py`
