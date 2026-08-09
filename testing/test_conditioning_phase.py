#!/usr/bin/env python3
"""Unit tests for ConditioningPhase offense-trajectory modeling."""

import os
import unittest

os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from pyshacl import validate
import rdflib

REPO = os.getcwd()

CAC_CORE = rdflib.Namespace("https://cacontology.projectvic.org/core#")
CAC_GROOMING = rdflib.Namespace("https://cacontology.projectvic.org/grooming#")
CAC_SEXTORTION = rdflib.Namespace("https://cacontology.projectvic.org/sextortion#")

GROOMING_SHAPES = os.path.join(REPO, "ontology", "cacontology-grooming-shapes.ttl")
CONDITIONING_EXAMPLE = os.path.join(
    REPO,
    "examples_knowledge_graphs",
    "conditioning-phase-offense-trajectory-example.ttl",
)


def shacl_validate(data_graph: rdflib.Graph, shapes_path: str) -> bool:
    shapes_graph = rdflib.Graph()
    shapes_graph.parse(shapes_path, format="turtle")
    conforms, _, _ = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="none",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
    )
    return conforms


class TestConditioningPhaseShacl(unittest.TestCase):
    def test_valid_dual_typed_passes_grooming_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix cac-core: <https://cacontology.projectvic.org/core#> .
            @prefix cac-grooming: <https://cacontology.projectvic.org/grooming#> .
            <urn:uuid:test-conditioning-valid> a cac-grooming:ConditioningPhase ,
                    cac-core:Phase ;
                rdfs:label "Test Conditioning" ;
                cac-core:conditioningMode "deception" .
            """,
            format="turtle",
        )
        self.assertTrue(shacl_validate(g, GROOMING_SHAPES))

    def test_missing_cac_core_phase_dual_type_fails_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix cac-core: <https://cacontology.projectvic.org/core#> .
            @prefix cac-grooming: <https://cacontology.projectvic.org/grooming#> .
            <urn:uuid:test-conditioning-missing-phase> a cac-grooming:ConditioningPhase ;
                rdfs:label "Missing dual type" ;
                cac-core:conditioningMode "trust_rapport" .
            """,
            format="turtle",
        )
        self.assertFalse(shacl_validate(g, GROOMING_SHAPES))

    def test_invalid_conditioning_mode_fails_shacl(self):
        g = rdflib.Graph()
        g.parse(
            data="""
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix cac-core: <https://cacontology.projectvic.org/core#> .
            @prefix cac-grooming: <https://cacontology.projectvic.org/grooming#> .
            <urn:uuid:test-conditioning-bad-mode> a cac-grooming:ConditioningPhase ,
                    cac-core:Phase ;
                rdfs:label "Bad mode" ;
                cac-core:conditioningMode "not_a_real_mode" .
            """,
            format="turtle",
        )
        self.assertFalse(shacl_validate(g, GROOMING_SHAPES))

    def test_offense_trajectory_example_passes_shacl(self):
        g = rdflib.Graph()
        g.parse(CONDITIONING_EXAMPLE, format="turtle")
        self.assertTrue(shacl_validate(g, GROOMING_SHAPES))


class TestTrustBuildingDeprecation(unittest.TestCase):
    def test_trust_building_subclasses_conditioning_phase(self):
        g = rdflib.Graph()
        g.parse(os.path.join(REPO, "ontology", "cacontology-grooming.ttl"), format="turtle")
        g.parse(os.path.join(REPO, "ontology", "cacontology-core-spine.ttl"), format="turtle")
        g.parse(os.path.join(REPO, "ontology", "cacontology-sextortion.ttl"), format="turtle")

        grooming_tb = CAC_GROOMING.TrustBuildingPhase
        sextortion_tb = CAC_SEXTORTION.TrustBuildingPhase
        conditioning = CAC_CORE.ConditioningPhase

        self.assertIn(
            (grooming_tb, rdflib.RDFS.subClassOf, CAC_GROOMING.ConditioningPhase),
            g,
        )
        self.assertIn(
            (sextortion_tb, rdflib.RDFS.subClassOf, conditioning),
            g,
        )
        self.assertTrue(
            any(
                o == rdflib.Literal(True)
                for o in g.objects(grooming_tb, rdflib.OWL.deprecated)
            )
        )
        self.assertTrue(
            any(
                o == rdflib.Literal(True)
                for o in g.objects(sextortion_tb, rdflib.OWL.deprecated)
            )
        )


if __name__ == "__main__":
    unittest.main()
