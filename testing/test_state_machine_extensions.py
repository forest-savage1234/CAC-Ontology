#!/usr/bin/env python3
"""Unit tests for CaseLinker state machine extension classes."""

import os
import sys
import unittest

os.chdir(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.getcwd(), "sdk", "python"))

from pyshacl import validate
import rdflib

from cacontology import (
    AccountReplacementEvent,
    AffordanceMisuse,
    ChannelMigrationEvent,
    CoercionCycle,
)

REPO = os.getcwd()


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


class TestCoercionCycle(unittest.TestCase):
  shapes = os.path.join(REPO, "ontology", "cacontology-sextortion-shapes.ttl")

  def test_valid_instance_passes_shacl(self):
    cycle = CoercionCycle(
      id="urn:uuid:test-coercion-cycle-valid",
      sustained_by="urn:uuid:test-artifact-001",
      cycles_between=[
        "urn:uuid:test-extortion-phase",
        "urn:uuid:test-image-phase",
      ],
      coercion_cycle_demand_type="imagery_quota",
      termination_condition="unknown",
    )
    self.assertTrue(shacl_validate(cycle.to_graph(), self.shapes))
    self.assertIn("@type", cycle.to_jsonld())
    self.assertEqual(cycle.to_jsonld()["@type"], "cac-sextortion:CoercionCycle")

  def test_missing_sustained_by_fails_shacl(self):
    g = rdflib.Graph()
    g.parse(
      data="""
      @prefix cac-sextortion: <https://cacontology.projectvic.org/sextortion#> .
      <urn:uuid:test-coercion-cycle-invalid> a cac-sextortion:CoercionCycle ;
        cac-sextortion:coercionCycleDemandType "imagery_quota" ;
        cac-sextortion:cyclesBetween <urn:uuid:phase-a>, <urn:uuid:phase-b> .
      """,
      format="turtle",
    )
    self.assertFalse(shacl_validate(g, self.shapes))


class TestChannelMigrationEvent(unittest.TestCase):
  shapes = os.path.join(REPO, "ontology", "cacontology-platforms-shapes.ttl")

  def test_valid_instance_passes_shacl(self):
    event = ChannelMigrationEvent(
      id="urn:uuid:test-channel-migration-valid",
      from_platform="urn:uuid:platform-instagram",
      to_platform="urn:uuid:platform-messenger",
      migration_rationale="capability_upgrade",
      occurs_between=["urn:uuid:phase-trust", "urn:uuid:phase-image"],
    )
    self.assertTrue(shacl_validate(event.to_graph(), self.shapes))
    self.assertEqual(
      event.to_jsonld()["cac-platforms:migrationRationale"], "capability_upgrade"
    )

  def test_invalid_rationale_fails_shacl(self):
    g = rdflib.Graph()
    g.parse(
      data="""
      @prefix cac-platforms: <https://cacontology.projectvic.org/platforms#> .
      <urn:uuid:test-channel-migration-invalid> a cac-platforms:ChannelMigrationEvent ;
        cac-platforms:fromPlatform <urn:uuid:platform-a> ;
        cac-platforms:toPlatform <urn:uuid:platform-b> ;
        cac-platforms:migrationRationale "invalid_value" ;
        cac-platforms:occursBetween <urn:uuid:phase-a>, <urn:uuid:phase-b> .
      """,
      format="turtle",
    )
    self.assertFalse(shacl_validate(g, self.shapes))


class TestAffordanceMisuse(unittest.TestCase):
  shapes = os.path.join(REPO, "ontology", "cacontology-platforms-shapes.ttl")

  def test_valid_instance_passes_shacl(self):
    misuse = AffordanceMisuse(
      id="urn:uuid:test-affordance-misuse-valid",
      affordance_class="urn:uuid:affordance-ephemerality",
      enables_transition_from="urn:uuid:phase-trust",
      enables_transition_to="urn:uuid:phase-image",
      misuse_description="Disappearing messages normalized image sharing before extortion.",
      platform="urn:uuid:platform-snapchat",
    )
    self.assertTrue(shacl_validate(misuse.to_graph(), self.shapes))
    self.assertIn("cac-platforms:misuseDescription", misuse.to_jsonld())

  def test_missing_description_fails_shacl(self):
    g = rdflib.Graph()
    g.parse(
      data="""
      @prefix cac-platforms: <https://cacontology.projectvic.org/platforms#> .
      <urn:uuid:test-affordance-misuse-invalid> a cac-platforms:AffordanceMisuse ;
        cac-platforms:affordanceClass <urn:uuid:affordance-anonymity> ;
        cac-platforms:enablesTransitionFrom <urn:uuid:phase-a> ;
        cac-platforms:enablesTransitionTo <urn:uuid:phase-b> .
      """,
      format="turtle",
    )
    self.assertFalse(shacl_validate(g, self.shapes))


class TestAccountReplacementEvent(unittest.TestCase):
  shapes = os.path.join(REPO, "ontology", "cacontology-grooming-shapes.ttl")

  def test_valid_instance_passes_shacl(self):
    event = AccountReplacementEvent(
      id="urn:uuid:test-account-replacement-valid",
      triggered_by="platform_ban",
      resumes_at="urn:uuid:phase-initial-contact",
      original_account_id="urn:uuid:account-banned",
      replacement_account_id="urn:uuid:account-new",
    )
    self.assertTrue(shacl_validate(event.to_graph(), self.shapes))
    self.assertEqual(event.to_jsonld()["cac-grooming:triggeredBy"], "platform_ban")

  def test_invalid_trigger_fails_shacl(self):
    g = rdflib.Graph()
    g.parse(
      data="""
      @prefix cac-grooming: <https://cacontology.projectvic.org/grooming#> .
      <urn:uuid:test-account-replacement-invalid> a cac-grooming:AccountReplacementEvent ;
        cac-grooming:triggeredBy "account_hack" ;
        cac-grooming:resumesAt <urn:uuid:phase-initial-contact> .
      """,
      format="turtle",
    )
    self.assertFalse(shacl_validate(g, self.shapes))


if __name__ == "__main__":
  unittest.main()
