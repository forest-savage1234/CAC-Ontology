#!/usr/bin/env python3
"""Regression controls for REM-014 strict-profile decomposition."""

from __future__ import annotations

import unittest

import decompose_owl2dl_profile as decomposition
from rdflib import Graph, OWL


class Rem014DecompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = decomposition.build()

    def test_multiline_annotation_text_is_not_counted_as_a_violation(self):
        for name in ("C3", "C5"):
            configuration = self.report["configurations"][name]
            self.assertEqual(
                configuration["violation_count"],
                sum(configuration["by_category"].values()),
            )
            self.assertLessEqual(
                configuration["violation_count"],
                decomposition.REM014_BASELINE[name]["violation_count"],
            )

    def test_compatibility_delta_is_two_reserved_vocabulary_findings(self):
        c3 = self.report["configurations"]["C3"]
        c5 = self.report["configurations"]["C5"]
        self.assertEqual(2, c5["violation_count"] - c3["violation_count"])
        self.assertEqual(
            2,
            c5["by_root_cause"]["reserved-owl-vocabulary-as-domain-or-range"]
            - c3["by_root_cause"]["reserved-owl-vocabulary-as-domain-or-range"],
        )

    def test_high_confidence_cac_debt_is_prioritized(self):
        roots = [unit["root_cause"] for unit in self.report["priority_units"][:4]]
        self.assertIn("property-kind-punning", roots)
        self.assertIn("class-used-as-datatype", roots)
        self.assertNotIn(
            "single-operand-equivalence",
            self.report["configurations"]["C3"]["by_root_cause"],
        )

    def test_first_remediation_slice_reduces_only_cac_owned_findings(self):
        c3 = self.report["configurations"]["C3"]
        self.assertEqual(-21, self.report["delta_from_baseline"]["C3"])
        self.assertEqual(
            -21,
            c3["by_owner"]["cac"]
            - decomposition.REM014_BASELINE["C3"]["cac_owned_count"],
        )
        self.assertEqual(6117, c3["by_owner"]["upstream"])

    def test_no_class_is_declared_equivalent_only_to_itself(self):
        graph = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-usa-federal-law.ttl",
            format="turtle",
        )
        self.assertEqual([], sorted(str(subject) for subject, _, value in graph.triples((None, OWL.equivalentClass, None)) if subject == value))


if __name__ == "__main__":
    unittest.main()
