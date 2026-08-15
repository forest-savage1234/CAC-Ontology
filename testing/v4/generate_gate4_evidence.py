#!/usr/bin/env python3
"""Generate the local Gate 4 evidence bundle without network or GitHub mutation."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
REPORTS = HERE / "reports"
BASE = "93de063951b758dd68a27611638c177fcf910eab"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ARCH = load_module("architecture_audit", HERE / "architecture_audit.py")
SPARQL = load_module("audit_shacl_sparql", HERE / "audit_shacl_sparql.py")
LEVELS = load_module(
    "audit_shape_level_assumptions", HERE / "audit_shape_level_assumptions.py"
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def write_json(name: str, value: object) -> None:
    (REPORTS / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        [sys.executable, str(HERE / "build_dependency_lock.py")],
        cwd=REPO,
        check=True,
    )
    dependency = json.loads((HERE / "dependency-lock.json").read_text(encoding="utf-8"))

    configurations: dict[str, object] = {}
    for config in ("C3", "C5"):
        configurations[config] = {}
        for inference in ("asserted", "rdfs"):
            report = ARCH.build_report(REPO, config, inference)
            write_json(f"{config.lower()}-{inference}.json", report)
            configurations[config][inference] = {
                "status": report["status"],
                "diagnostic_findings": report["counts"]["diagnostic_findings"],
                "triples": report["counts"]["triples"],
            }

    tests = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(HERE),
            "-p",
            "test_*.py",
            "-v",
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    test_output = tests.stdout + tests.stderr
    (REPORTS / "unittest.txt").write_text(test_output, encoding="utf-8")
    match = re.search(r"Ran (\d+) tests", test_output)

    sparql = SPARQL.audit(REPO / "ontology")
    write_json("shacl-sparql-syntax.json", sparql)
    level_inventory = LEVELS.inventory(REPO / "ontology")
    write_json("shape-level-assumptions.json", level_inventory)

    baseline = json.loads(
        (HERE / "baselines" / "c1-v3.1-asserted.json").read_text(encoding="utf-8")
    )
    ledger = json.loads((HERE / "term-disposition-summary.json").read_text(encoding="utf-8"))
    imports = dependency["imports"]

    commits = git("rev-list", "--reverse", f"{BASE}..HEAD").splitlines()
    unsigned = [
        commit
        for commit in commits
        if "Signed-off-by:" not in git("show", "-s", "--format=%B", commit)
    ]
    changed_paths = git("diff", "--name-only", f"{BASE}..HEAD").splitlines()

    docker = shutil.which("docker")
    docker_server = False
    if docker:
        docker_check = subprocess.run(
            [docker, "version", "--format", "{{json .Server}}"],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        docker_server = docker_check.returncode == 0 and docker_check.stdout.strip() not in {
            "",
            "null",
        }

    summary = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "base_commit": BASE,
            "candidate_commit": git("rev-parse", "HEAD"),
            "candidate_tree": git("rev-parse", "HEAD^{tree}"),
            "branch": git("branch", "--show-current"),
            "tracked_dirty": bool(git("status", "--porcelain", "--untracked-files=no")),
            "commits": len(commits),
            "unsigned_commits": unsigned,
            "changed_paths": len(changed_paths),
            "detection_shapes_changed": "ontology/cacontology-detection-shapes.ttl" in changed_paths,
        },
        "configurations": {
            "C1": {
                "status": "observed-baseline",
                "diagnostic_findings": baseline["counts"]["diagnostic_findings"],
                "source_commit": BASE,
            },
            "C2": {
                "status": "blocked",
                "blocker": "Pinned UCO gUFO Profile bytes at 4b98b9881aa29ed80f39b589d15725fa696c921a are unavailable locally; official Git and browser retrieval failed.",
            },
            "C3": configurations["C3"],
            "C4": {
                "status": "blocked",
                "blocker": "Same unavailable pinned UCO gUFO Profile bytes as C2.",
            },
            "C5": configurations["C5"],
        },
        "tests": {
            "return_code": tests.returncode,
            "tests_run": int(match.group(1)) if match else None,
            "status": "pass" if tests.returncode == 0 else "fail",
        },
        "shacl_sparql": {
            "queries": sparql["queries"],
            "proposal_failures": sparql["proposal_failures"],
            "pr48_detection_failures": sparql["pr48_detection_failures"],
        },
        "term_dispositions": ledger,
        "dependencies": {
            "imports": len(imports),
            "resolved_local": sum(i["status"] == "resolved-local" for i in imports),
            "unresolved_remote": sum(i["status"] == "unresolved-remote" for i in imports),
            "uco_gufo_profile": dependency["uco_gufo_profile"],
        },
        "owl_2_dl": {
            "status": "blocked",
            "java": shutil.which("java"),
            "robot": shutil.which("robot"),
            "docker_client": docker,
            "docker_server_available": docker_server,
            "claim": "No HermiT/ROBOT OWL 2 DL consistency or unsatisfiable-class result is claimed.",
        },
        "gate4_recommendation": {
            "status": "hold",
            "reason": "Applicable local diagnostics pass, but deterministic imports, C4 overlay execution, and normative OWL 2 DL reasoning remain release blockers.",
            "github_mutation_authorized": False,
        },
        "sensitive_data": "Synthetic fixtures only; no real investigative, victim, or adopter data is present.",
    }
    write_json("gate4-summary.json", summary)
    return 0 if tests.returncode == 0 else tests.returncode


if __name__ == "__main__":
    raise SystemExit(main())
