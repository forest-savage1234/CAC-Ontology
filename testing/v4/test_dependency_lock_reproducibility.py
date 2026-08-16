#!/usr/bin/env python3
"""Cross-platform reproducibility controls for first-party dependency hashes."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import build_dependency_lock as dependency_lock


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


class DependencyLockReproducibilityTests(unittest.TestCase):
    def test_local_ontology_hashes_use_canonical_lf_bytes(self):
        lock = json.loads((HERE / "dependency-lock.json").read_text(encoding="utf-8"))
        self.assertIn("CRLF-to-LF", lock["first_party_text_hash_policy"])
        for record in lock["ontology_files"]:
            path = REPO / record["path"]
            canonical = path.read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual("utf-8-lf", record["canonicalization"])
            self.assertEqual(len(canonical), record["bytes"])
            self.assertEqual(hashlib.sha256(canonical).hexdigest(), record["sha256"])

    def test_git_equivalent_line_endings_produce_the_same_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf.ttl"
            crlf = root / "crlf.ttl"
            lf.write_bytes(b"@prefix ex: <urn:example:> .\nex:s ex:p ex:o .\n")
            crlf.write_bytes(b"@prefix ex: <urn:example:> .\r\nex:s ex:p ex:o .\r\n")
            lf_record = dependency_lock.file_record(
                root, lf, status="resolved-local", source="test", license_id="test", canonical_text=True
            )
            crlf_record = dependency_lock.file_record(
                root, crlf, status="resolved-local", source="test", license_id="test", canonical_text=True
            )
            self.assertEqual(lf_record["bytes"], crlf_record["bytes"])
            self.assertEqual(lf_record["sha256"], crlf_record["sha256"])


if __name__ == "__main__":
    unittest.main()
