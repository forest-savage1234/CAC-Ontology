# CAC v4 Architecture Conformance Harness

This directory contains the deterministic, synthetic-data-only harness for the
issue-44 foundational architecture proposal. It separates frozen v3.1 baseline
observations from v4 release gates.

## Configurations

- **C1** — CAC v3.1 asserted graph at the recorded proposal base.
- **C2** — C1 plus the pinned UCO gUFO Profile interoperability overlay.
- **C3** — proposed CAC v4 normative graph.
- **C4** — C3 plus the same profile overlay.
- **C5** — C3 plus the bounded v3 compatibility artifact.

C1 and C2 are evidence, not release gates. C3 and C4 must pass all applicable
checks. C5 must pass before compatibility support is claimed.

## Local execution

Use Python 3.12 with the exact packages in `requirements.lock`, then run:

```text
python testing/v4/architecture_audit.py --configuration C3 --output <report.json>
python testing/v4/architecture_audit.py --configuration C5 --inference rdfs --output <report.json>
python -m unittest discover -s testing/v4 -p "test_*.py" -v
```

The C1 report is frozen in `baselines/c1-v3.1-asserted.json` at the recorded
base commit. C2 and C4 require the exact pinned overlay bytes and therefore
must emit a blocked status rather than silently falling back to a different
revision. The local audit is not an OWL 2 DL consistency substitute.

The audit reports the source commit, dirty state, runtime versions, graph
counts, and stable diagnostic identifiers. Remote imports are never silently
retrieved by the Python harness; the dependency catalog controls imported
content for connected and offline conformance runs.

All fixtures in this directory are invented examples and contain no real case
or victim data.
