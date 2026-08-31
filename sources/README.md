# Sources

This directory is the provenance boundary for original and imported Rising Sea planning material.

## Rule

Source artifacts may inform canonical specs, but source presence does not make a document current or authoritative.

Every imported source should eventually be recorded in `sources/registry.jsonl` with:

- stable source ID;
- original path or URI;
- SHA-256 when bytes are available;
- source kind;
- import/discovery date;
- semantic objects it supports;
- disposition such as `CURRENT_SOURCE`, `HISTORICAL_SOURCE`, `SUPERSEDED_SOURCE`, `DUPLICATE_SOURCE`, or `EXTERNAL_REFERENCE`.

Never silently rewrite an imported source to make it fit the current design. Compile current meaning into `specs/` and retain the provenance link.
