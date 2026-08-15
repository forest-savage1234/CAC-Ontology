#!/usr/bin/env python3
"""Tests that reviewed term groups match the asserted ontology graph."""

import json
from pathlib import Path
import unittest

from rdflib import Graph, Namespace, RDF, RDFS, URIRef

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
GUFO = Namespace("http://purl.org/nemo/gufo#")
CORE = Namespace("https://cacontology.projectvic.org/core#")


class ReviewedDispositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = Graph()
        for path in sorted((REPO / "ontology").glob("*.ttl")):
            if "-shapes" not in path.name:
                cls.graph.parse(path, format="turtle")
        groups = json.loads((HERE / "reviewed-term-groups.json").read_text(encoding="utf-8"))["groups"]
        cls.groups = {group["group_id"]: group for group in groups}

    def test_reviewed_operational_phases_are_not_gufo_classifiers(self):
        group = self.groups["PHASE-OCCURRENCE-001"]
        for iri in group["exact_iris"]:
            term = URIRef(iri)
            self.assertIn((term, RDFS.subClassOf, CORE.Phase), self.graph, iri)
            self.assertNotIn((term, RDF.type, GUFO.Phase), self.graph, iri)

    def test_event_phase_cross_parents_were_removed(self):
        for iri in (
            "https://cacontology.projectvic.org/production#ActiveProductionPhase",
            "https://cacontology.projectvic.org/production#ProductionPreparationPhase",
            "https://cacontology.projectvic.org/production#ProductionDistributionPhase",
            "https://cacontology.projectvic.org/usa-federal-law#PreTrialPhase",
            "https://cacontology.projectvic.org/usa-federal-law#TrialPhase",
            "https://cacontology.projectvic.org/usa-federal-law#SentencingPhase",
            "https://cacontology.projectvic.org/usa-federal-law#PostConvictionPhase",
        ):
            parents = set(self.graph.objects(URIRef(iri), RDFS.subClassOf))
            self.assertEqual({CORE.Phase}, parents, iri)


if __name__ == "__main__":
    unittest.main()
