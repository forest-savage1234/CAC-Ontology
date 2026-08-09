# Duplicate Detection Report (Local Repo Scan)

- **Source URL**: `https://www.missingkids.org/cybertiplinedata`
- **caseId**: `ncmec-cybertipline-data`
- **Scan date (UTC)**: 2026-07-19T05:03:58Z
- **Method**: local repo scan of `analytics_demonstration/collected_sources/` and `examples_knowledge_graphs/` for exact URL match (in lieu of a triplestore SPARQL duplicate check). Near-duplicate title/keyword scan for CyberTipline / NCMEC aggregate data pages.

## Findings

| Check | Result |
|---|---|
| Exact URL in `collected_sources/*/manifest.yaml` | **none** |
| Exact URL in `collected_sources/*/source.txt` | **none** |
| Exact URL in `examples_knowledge_graphs/*.ttl` | **none** |
| caseId directory already present | **none** prior to this collection |
| Near-duplicate title "CyberTipline Data" / "2025 CyberTipline Report" as primary source | **none** |

### Related (non-duplicate) mentions

Repo contains other graphs that **reference** NCMEC/CyberTip concepts (e.g. investigation lifecycle examples, Utah cases, partnerships). Those are different sources/cases and do not constitute a prior collection of this public statistics page.

## Entity resolution (near-duplicate)

- **Status**: not executed beyond keyword/URL scan
- **Reason**: single-document Path A; no vector index / Graph DB ER stack configured for volunteer workflow

## Decision

- **Action**: **PROCEED** with collection
- **Reason**: No exact or near-duplicate primary source collection detected for this URL/page

## Content hashes (for future deduplication)

| Artifact | Size (bytes) | SHA-256 |
|---|---:|---|
| `source.html` (raw) | 725977 | `db3cf9214fb28679b5f709ec54a36aff3aa0fa0bd431ae6fff3bb52d75e9e9c4` |
| `source.txt` (clean prose) | 22420 | `4b4e83f0c20e47b3289292441149cf98bbc4d6af622712015a09a2c73b8c95e6` |
| `normalized.txt` (keypoints) | 8746 | `f0d8b0431066a09a0b5b444f618bf874083ad088c861ade132b23ea891a9a617` |
