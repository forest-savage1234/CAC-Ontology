# Namespaces and prefixes

This reference describes CAC Ontology v3.1.0. Prefixes are conveniences; IRIs carry the semantics.

## CAC namespaces

| Suggested prefix | Namespace | Use |
|---|---|---|
| `cac:` or `cacontology:` | `https://cacontology.projectvic.org#` | Core CAC vocabulary |
| `cac-core:` | `https://cacontology.projectvic.org/core#` | Semantic spine introduced in v3.0.0 |
| `cac-grooming:` | `https://cacontology.projectvic.org/grooming#` | Grooming module |
| `cac-sextortion:` | `https://cacontology.projectvic.org/sextortion#` | Sextortion module |
| `cac-platforms:` | `https://cacontology.projectvic.org/platforms#` | Platforms module |
| `cac-temporal:` | `https://cacontology.projectvic.org/temporal#` | Temporal module |

Most domain modules follow `https://cacontology.projectvic.org/{module}#`, but consumers must verify the declarations in each Turtle file. Filenames, local prefix choices, and namespace path segments are not guaranteed to be identical.

## External namespaces

Common unversioned term namespaces include:

```turtle
@prefix case-investigation: <https://ontology.caseontology.org/case/investigation/> .
@prefix uco-core: <https://ontology.unifiedcyberontology.org/uco/core/> .
@prefix uco-action: <https://ontology.unifiedcyberontology.org/uco/action/> .
@prefix uco-identity: <https://ontology.unifiedcyberontology.org/uco/identity/> .
@prefix uco-observable: <https://ontology.unifiedcyberontology.org/uco/observable/> .
@prefix gufo: <http://purl.org/nemo/gufo#> .
```

CAC v3.1.0 pins CASE/UCO imports to **1.5.0 version IRIs** and gUFO
imports to its **1.0.0 version IRI**, even though term prefixes use the stable
namespaces above. Examples of versioned imports include:

```turtle
<https://ontology.caseontology.org/case/case/1.5.0>
<https://ontology.caseontology.org/case/investigation/1.5.0>
<https://ontology.unifiedcyberontology.org/uco/core/1.5.0>
<http://purl.org/nemo/gufo#/1.0.0>
```

## Rules for examples and applications

- Declare every prefix used in a standalone graph or query.
- Prefer `cac-core:` only for the spine; do not also call it `cacontology-core:` in new documentation.
- Use repository-relative file paths without a leading slash.
- Do not treat a version IRI as the namespace for individual terms.
- Do not invent JSON-LD context paths. Only use contexts that exist under `contexts/`.
