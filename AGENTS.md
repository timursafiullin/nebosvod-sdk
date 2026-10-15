# Nebosvod SDK — agent guide

This is the PUBLIC SDK repository (Apache-2.0). Everything here may be read by anyone.

## Rules

- Never add internal architecture, roadmap, ADRs, `.agents/` content, proprietary engine code, license keys or
  references to private repositories beyond their public names.
- `schemas/` is generated from the private Nebosvod repository by CI; never edit it by hand.
- Python 3.12+, typed (mypy strict), ruff for lint and format; no dependencies beyond those declared in
  `pyproject.toml`; additions need maintainer approval.
- Physical quantities in SI units; reference frame and time scale explicit in types.
- A module never receives simulated truth; do not design APIs that would require it.
- Tests are deterministic (fixed seeds, no network, no wall clock).
- Everything in English.
- Code style: Allman braces and 4-space indentation for C++ (`.clang-format`), ruff for Python (`ruff.toml`),
  prettier for JavaScript/TypeScript (`.prettierrc.json`); run the formatter before every commit.
- Commit messages, PR descriptions and tags never contain links to AI sessions, chats, transcripts or any
  internal URL. The only allowed AI trailer is `Co-Authored-By:`.

## Layout

See `README.md`. Each folder has a README describing its content and rules.

## Workflow

Changes come as small pull requests with tests. Maintainers coordinate SDK work from the private repository;
external contributors follow `CONTRIBUTING.md`.
