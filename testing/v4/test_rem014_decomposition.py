#!/usr/bin/env python3
"""Regression controls for REM-014 strict-profile decomposition."""

from __future__ import annotations

import unittest

import decompose_owl2dl_profile as decomposition
from rdflib import Graph, OWL, RDF, URIRef


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

    def test_completed_high_confidence_roots_leave_the_priority_queue(self):
        roots = self.report["configurations"]["C3"]["by_root_cause"]
        self.assertNotIn(
            "single-operand-equivalence",
            roots,
        )
        self.assertEqual(2, roots.get("property-kind-punning", 0))
        self.assertNotIn("class-used-as-datatype", roots)

    def test_remediation_reduces_only_cac_owned_findings(self):
        c3 = self.report["configurations"]["C3"]
        self.assertLessEqual(self.report["delta_from_baseline"]["C3"], -21)
        self.assertEqual(
            self.report["delta_from_baseline"]["C3"],
            c3["by_owner"]["cac"]
            - decomposition.REM014_BASELINE["C3"]["cac_owned_count"],
        )
        self.assertEqual(
            decomposition.REM014_BASELINE["C3"]["upstream_owned_count"],
            c3["by_owner"]["upstream"],
        )
        self.assertEqual(
            decomposition.REM014_BASELINE["C3"]["shared_or_unattributed_count"],
            c3["by_owner"]["shared-or-unattributed"],
        )

    def test_object_property_targets_have_explicit_class_declarations(self):
        educational = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-educational-exploitation.ttl",
            format="turtle",
        )
        taskforce = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-taskforce.ttl",
            format="turtle",
        )
        targets = {
            educational: (
                "https://cacontology.projectvic.org/educational#PhysicalContactPattern",
                "https://cacontology.projectvic.org/educational#VictimDisclosureToStaff",
                "https://cacontology.projectvic.org/educational#PrincipalNotification",
                "https://cacontology.projectvic.org/educational#PoliceNotification",
                "https://cacontology.projectvic.org/educational#AgeDeception",
                "https://cacontology.projectvic.org/educational#MultipleAccountDeception",
            ),
            taskforce: (
                "https://cacontology.projectvic.org/taskforce#TaskForceTraining",
            ),
        }
        for graph, iris in targets.items():
            for iri in iris:
                self.assertIn((URIRef(iri), RDF.type, OWL.Class), graph)

    def test_no_class_is_declared_equivalent_only_to_itself(self):
        graph = Graph().parse(
            decomposition.REPO / "ontology" / "cacontology-usa-federal-law.ttl",
            format="turtle",
        )
        self.assertEqual([], sorted(str(subject) for subject, _, value in graph.triples((None, OWL.equivalentClass, None)) if subject == value))


if __name__ == "__main__":
    unittest.main()
