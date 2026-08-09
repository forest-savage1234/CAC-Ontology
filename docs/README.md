# CAC Ontology documentation

This documentation describes **CAC Ontology v3.1.0**. The semantic spine was introduced in v3.0.0, and CASE/UCO imports are pinned to 1.5.0.

## Start here

- [User guide](user_doc.md) — loading, authoring, and validation guidance
- [Architecture](architecture.md) — semantic spine, bridges, and module relationships
- [Design](design.md) — modeling principles and shipped-versus-planned distinctions
- [Interoperability](interoperability.md) — CASE, UCO, and gUFO alignment
- [Namespaces and prefixes](namespaces-and-prefixes.md) — canonical IRI guidance
- [Module catalog](CAC-Ontology-List) — file-by-file ontology and shapes inventory
- [Glossary](glossary.md) — project terminology
- [Product requirements](PRD.md) — requirements and targets, not an implementation report

The repository currently ships 50 ontology/alignment Turtle modules, 47 SHACL shape files, 61 Turtle example graphs, 32 SPARQL query files, and six JSON-LD contexts. These counts are descriptive of v3.1.0 in this checkout.

## Status conventions

- **Shipped** means the referenced artifact exists in the repository.
- **Requirement** or **target** describes desired behavior and is not proof that it has been implemented or benchmarked.
- **Planned** means no complete shipped implementation is claimed.
- **Historical** preserves release context and must not be read as current guidance.

The [v3.0 semantic-spine proposal](major_release-planning/CAC-Ontology-v3.0.0-Semantic-Spine-Refactoring-Proposal.md) is historical. Use the current architecture and ontology files for v3.1.0 behavior.

For repository-specific AI-agent procedure, see [agent.md](../agent.md).
