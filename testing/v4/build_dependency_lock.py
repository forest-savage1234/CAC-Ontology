#!/usr/bin/env python3
"""Generate the local/remote import catalog without retrieving remote content."""

from __future__ import annotations

import hashlib
import json
from importlib.metadata import version
from pathlib import Path

from rdflib import Graph, OWL, RDF, URIRef

PACKAGES = ("rdflib", "pyshacl", "owlrl", "html5rdf", "packaging", "prettytable", "pyparsing", "wcwidth")
OVERLAY_REVISION = "4b98b988"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    declarations: dict[str, Path] = {}
    imports: set[str] = set()
    local_files = []
    for path in sorted((repo / "ontology").glob("*.ttl")):
        graph = Graph().parse(path, format="turtle")
        for ontology in graph.subjects(RDF.type, OWL.Ontology):
            if isinstance(ontology, URIRef):
                declarations[str(ontology)] = path
            for iri in graph.objects(ontology, OWL.versionIRI):
                if isinstance(iri, URIRef):
                    declarations[str(iri)] = path
        imports.update(str(value) for value in graph.objects(None, OWL.imports))
        local_files.append(
            {
                "path": path.relative_to(repo).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    catalog = []
    for iri in sorted(imports):
        local = declarations.get(iri)
        if local:
            catalog.append(
                {
                    "requested_iri": iri,
                    "status": "resolved-local",
                    "path": local.relative_to(repo).as_posix(),
                    "bytes": local.stat().st_size,
                    "sha256": sha256(local),
                }
            )
        else:
            catalog.append(
                {
                    "requested_iri": iri,
                    "status": "unresolved-remote",
                    "path": None,
                    "bytes": None,
                    "sha256": None,
                }
            )

    result = {
        "schema_version": 1,
        "policy": "Remote imports must be content-addressed before C2/C4 and OWL 2 DL gates run.",
        "runtime": {package: version(package) for package in PACKAGES},
        "uco_gufo_profile": {
            "revision_prefix": OVERLAY_REVISION,
            "status": "unresolved-remote",
            "commit": None,
            "sha256": None,
            "path": None,
        },
        "imports": catalog,
        "ontology_files": local_files,
    }
    output = Path(__file__).with_name("dependency-lock.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
