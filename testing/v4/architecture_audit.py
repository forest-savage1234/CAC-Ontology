#!/usr/bin/env python3
"""Deterministic asserted-graph diagnostics for the CAC v4 architecture."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS, Graph, Namespace, URIRef

CAC_CORE = Namespace("https://cacontology.projectvic.org/core#")
GUFO = Namespace("http://purl.org/nemo/gufo#")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_value(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def ontology_files(repo: Path) -> list[Path]:
    return sorted(
        path
        for path in (repo / "ontology").glob("*.ttl")
        if "-shapes" not in path.name
    )


def load_graph(paths: list[Path]) -> Graph:
    graph = Graph()
    for path in paths:
        graph.parse(path, format="turtle")
    return graph


def subclass_index(graph: Graph) -> dict[URIRef, set[URIRef]]:
    parents: dict[URIRef, set[URIRef]] = defaultdict(set)
    for child, parent in graph.subject_objects(RDFS.subClassOf):
        if isinstance(child, URIRef) and isinstance(parent, URIRef):
            parents[child].add(parent)
    changed = True
    while changed:
        changed = False
        for child in list(parents):
            inherited = set().union(*(parents.get(p, set()) for p in parents[child]))
            if not inherited.issubset(parents[child]):
                parents[child].update(inherited)
                changed = True
    return parents


def audit_graph(graph: Graph) -> dict:
    parents = subclass_index(graph)
    # OWL-RL closure entails that owl:Nothing is a subclass of every class.
    # It is the built-in bottom class, not a modeled CAC term or a conflict.
    classes = {
        s
        for s in graph.subjects(RDF.type, OWL.Class)
        if isinstance(s, URIRef) and s != OWL.Nothing
    }
    role_branch = {c for c in classes if c == CAC_CORE.Role or CAC_CORE.Role in parents.get(c, set())}
    phase_branch = {c for c in classes if c == CAC_CORE.Phase or CAC_CORE.Phase in parents.get(c, set())}
    enduring_branch = {
        c for c in classes if c == CAC_CORE.EnduringEntity or CAC_CORE.EnduringEntity in parents.get(c, set())
    }
    event_branch = {c for c in classes if c == CAC_CORE.Event or CAC_CORE.Event in parents.get(c, set())}

    diagnostics = {
        "META001_OPERATIONAL_ROLE_AS_GUFO_CLASSIFIER": sorted(
            str(c) for c in role_branch if (c, RDF.type, GUFO.Role) in graph
        ),
        "META002_OPERATIONAL_PHASE_AS_GUFO_CLASSIFIER": sorted(
            str(c) for c in phase_branch if (c, RDF.type, GUFO.Phase) in graph
        ),
        "META003_ENDURING_PHASE_OVERLAP": sorted(str(c) for c in enduring_branch & phase_branch),
        "META004_CORE_ROLE_SUBCLASSES_GUFO_ROLE": sorted(
            str(o) for o in graph.objects(CAC_CORE.Role, RDFS.subClassOf) if o == GUFO.Role
        ),
        "META005_CORE_PHASE_SUBCLASSES_GUFO_PHASE": sorted(
            str(o) for o in graph.objects(CAC_CORE.Phase, RDFS.subClassOf) if o == GUFO.Phase
        ),
        "META006_ROLE_ASSIGNMENT_INSTANCE_AS_GUFO_CLASSIFIER": sorted(
            str(node)
            for node in graph.subjects(RDF.type, CAC_CORE.RoleAssignment)
            if (node, RDF.type, GUFO.Role) in graph
        ),
        "META007_PHASE_OCCURRENCE_AS_GUFO_CLASSIFIER": sorted(
            str(node)
            for node in graph.subjects(RDF.type, CAC_CORE.Phase)
            if (node, RDF.type, GUFO.Phase) in graph and (node, RDF.type, OWL.Class) not in graph
        ),
        "META008_OPERATIONAL_ROLE_ENDURING_OVERLAP": sorted(str(c) for c in role_branch & enduring_branch),
        "META009_OPERATIONAL_ROLE_PHASE_OVERLAP": sorted(str(c) for c in role_branch & phase_branch),
        "META010_OPERATIONAL_PHASE_EVENT_OVERLAP": sorted(str(c) for c in phase_branch & event_branch),
        "META011_GUFO_ROLE_CLASSIFIER_WITHOUT_ENDURING_BEARER_BRANCH": sorted(
            str(c)
            for c in classes
            if str(c).startswith("https://cacontology.projectvic.org/")
            and (c, RDF.type, GUFO.Role) in graph
            and c not in enduring_branch
        ),
    }
    return {
        "counts": {
            "triples": len(graph),
            "owl_classes": len(classes),
            "role_branch_classes": len(role_branch),
            "phase_branch_classes": len(phase_branch),
            "enduring_branch_classes": len(enduring_branch),
            "diagnostic_findings": sum(len(values) for values in diagnostics.values()),
        },
        "diagnostics": diagnostics,
    }


def build_report(repo: Path, configuration: str) -> dict:
    paths = ontology_files(repo)
    graph = load_graph(paths)
    result = audit_graph(graph)
    dirty = bool(git_value(repo, "status", "--porcelain"))
    result.update(
        {
            "schema_version": 1,
            "configuration": configuration,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source": {
                "commit": git_value(repo, "rev-parse", "HEAD"),
                "tree": git_value(repo, "rev-parse", "HEAD^{tree}"),
                "branch": git_value(repo, "branch", "--show-current"),
                "dirty": dirty,
            },
            "runtime": {
                "python": platform.python_version(),
                "rdflib": rdflib.__version__,
                "platform": platform.platform(),
            },
            "inputs": [
                {"path": path.relative_to(repo).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)}
                for path in paths
            ],
            "sensitive_data": "Synthetic fixtures only; no real sensitive case data.",
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--configuration", choices=("C1", "C2", "C3", "C4", "C5"), required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    report = build_report(repo, args.configuration)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
