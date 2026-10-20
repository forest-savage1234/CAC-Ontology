"""Regression checks for the domain participation targets in issue #58.

These focused tests use the shipped local class hierarchy with RDFS
inference and the participation shape's complete blank-node closure. They do
not download owl:imports or stand in for the repository-wide validation run.
"""
from pathlib import Path
import unittest

from pyshacl import validate
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL


ROOT = Path(__file__).resolve().parents[1]
CORE = Namespace("https://cacontology.projectvic.org/core#")
FORENSICS = Namespace("https://cacontology.projectvic.org/forensics#")
FEDERAL = Namespace("https://cacontology.projectvic.org/usa-federal-law#")
IMPACT = Namespace("https://cacontology.projectvic.org/victim-impact#")
SH = Namespace("http://www.w3.org/ns/shacl#")
EX = Namespace("urn:example:participation:")


class EventParticipationScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ontology = Graph()
        for filename in (
            "cacontology-core-spine.ttl",
            "cacontology-forensics.ttl",
            "cacontology-usa-federal-law.ttl",
            "cacontology-victim-impact.ttl",
        ):
            cls.ontology.parse(ROOT / "ontology" / filename, format="turtle")
        cls.hierarchy = Graph()
        for triple in cls.ontology.triples((None, RDFS.subClassOf, None)):
            cls.hierarchy.add(triple)
        cls.shapes = {}
        for filename, shape in (
            ("cacontology-forensics-shapes.ttl", FORENSICS.ForensicEventParticipationShape),
            ("cacontology-usa-federal-law-shapes.ttl", FEDERAL.EventParticipationValidationShape),
        ):
            graph = Graph().parse(ROOT / "ontology" / filename, format="turtle")
            cls.shapes[shape] = graph.cbd(shape)

    def conforms(self, shape, event_type, participant=None):
        data = Graph()
        data.add((EX.event, RDF.type, event_type))
        if participant is not None:
            data.add((EX.event, participant, EX.actor))
        conforms, _, report = validate(
            data_graph=data,
            shacl_graph=self.shapes[shape],
            ont_graph=self.hierarchy,
            inference="rdfs",
            do_owl_imports=False,
        )
        return conforms, report

    def domain_event_classes(self, namespace):
        return {
            term for term in self.ontology.subjects(RDF.type, OWL.Class)
            if str(term).startswith(str(namespace))
            and CORE.Event in self.ontology.transitive_objects(term, RDFS.subClassOf)
            and CORE.Phase not in self.ontology.transitive_objects(term, RDFS.subClassOf)
        }

    def test_unrelated_events_do_not_require_domain_participants(self):
        # SupportEvent is the actual spine parent of victim-support activity.
        for shape in self.shapes:
            for event_type in (CORE.Event, CORE.SupportEvent, CORE.InvestigativeAction,
                               IMPACT.VictimSupport):
                with self.subTest(shape=shape, event_type=event_type):
                    conforms, report = self.conforms(shape, event_type)
                    self.assertTrue(conforms, report)

    def test_forensic_events_still_require_participation(self):
        for event_type in self.domain_event_classes(FORENSICS):
            with self.subTest(event_type=event_type):
                conforms, report = self.conforms(FORENSICS.ForensicEventParticipationShape, event_type)
                self.assertFalse(conforms, report)

    def test_federal_events_still_require_participation(self):
        for event_type in self.domain_event_classes(FEDERAL):
            with self.subTest(event_type=event_type):
                conforms, report = self.conforms(FEDERAL.EventParticipationValidationShape, event_type)
                self.assertFalse(conforms, report)

    def test_each_forensic_participant_path_satisfies_the_rule(self):
        for prop in (FORENSICS.examinedBy, FORENSICS.performedBy,
                     FORENSICS.witnessedBy, FORENSICS.authorizedBy):
            with self.subTest(prop=prop):
                conforms, report = self.conforms(
                    FORENSICS.ForensicEventParticipationShape,
                    FORENSICS.ForensicAcquisitionAction, prop,
                )
                self.assertTrue(conforms, report)

    def test_each_federal_participant_path_satisfies_the_rule(self):
        for prop in (FEDERAL.prosecutedBy, FEDERAL.investigatedBy,
                     FEDERAL.defendedBy, FEDERAL.victimizedBy):
            with self.subTest(prop=prop):
                conforms, report = self.conforms(
                    FEDERAL.EventParticipationValidationShape,
                    FEDERAL.ChildPornographyPossession, prop,
                )
                self.assertTrue(conforms, report)

    def test_forensic_event_does_not_require_federal_participation(self):
        conforms, report = self.conforms(
            FEDERAL.EventParticipationValidationShape, FORENSICS.ForensicAcquisitionAction,
        )
        self.assertTrue(conforms, report)

    def test_federal_event_does_not_require_forensic_participation(self):
        conforms, report = self.conforms(
            FORENSICS.ForensicEventParticipationShape, FEDERAL.ChildPornographyPossession,
        )
        self.assertTrue(conforms, report)

    def test_wrong_domain_participant_does_not_satisfy_the_rule(self):
        for shape, event_type, prop in (
            (FORENSICS.ForensicEventParticipationShape,
             FORENSICS.ForensicAcquisitionAction, FEDERAL.prosecutedBy),
            (FEDERAL.EventParticipationValidationShape,
             FEDERAL.ChildPornographyPossession, FORENSICS.examinedBy),
        ):
            with self.subTest(shape=shape):
                conforms, report = self.conforms(shape, event_type, prop)
                self.assertFalse(conforms, report)

    def test_phase_inheriting_a_targeted_process_keeps_existing_requirement(self):
        conforms, report = self.conforms(
            FEDERAL.EventParticipationValidationShape, FEDERAL.TrialPhase,
        )
        self.assertFalse(conforms, report)


if __name__ == "__main__":
    unittest.main()
