# Contributing to Kreyolib 🇭🇹

> _Mèsi paske ou vle ede!_ — Thank you for wanting to help!

Kreyolib is a community-driven project to give Haitian Creole a stronger place in the AI and NLP ecosystem. Whether you are a developer, a linguist, a student, or just someone who cares about the language, **you are welcome here**.

Please take a moment to read this guide. It keeps contributions consistent and keeps the project enjoyable for everyone.

---

## Table of Contents / Kontni

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Adding a Language / Feature](#adding-a-language--feature)
- [Committing and Branching](#committing-and-branching)
- [Code Review / Status Checks](#code-review--status-checks)
- [Testing](#testing)
- [Style Guide](#style-guide)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

Be respectful, inclusive, and constructive. Kreyolib welcomes people of all backgrounds and experience levels. Harassment, discrimination, or hostile behavior of any kind will not be tolerated. Disagree about architecture and approaches, but never about the person behind the profile — keep communication professional, direct, and constructive.

---

## Ways to Contribute

You do not need to be a programmer to help!

- **Collect & clean datasets** — Haitian Creole corpora, proverbs, word lists.
- **Improve NLP algorithms** — tokenizers, POS tagging, phonetic tools.
- **Build libraries & APIs** — turn algorithms into usable tools.
- **Test models & tools** — report bugs, suggest edge cases.
- **Share linguistic knowledge** — grammar, morphology, orthography.
- **Write documentation & examples** — tutorials, guides, sample usage.

Open an [issue](https://github.com/AyitiDev/kreyolib/issues) or a [pull request](https://github.com/AyitiDev/kreyolib/pulls) to get started.

> 💡 **Have an idea?** Check the [README roadmap](../README.md#roadmap--progress) to see
> where your contribution could fit best.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/<your-username>/kreyolib.git
   cd kreyolib
   ```

3. **Add the upstream remote** to stay in sync:

   ```bash
   git remote add upstream https://github.com/AyitiDev/kreyolib.git
   git pull upstream main
   ```

4. **Create a branch** for your work (see [branching](#committing-and-branching)).

---

## Development Setup

We use [`uv`](https://docs.astral.sh/uv/) for environment and dependency
management.

```bash
uv sync                      # install dependencies
uv run pytest -v             # run the test suite
```

### Install Tooling & Pre-commit

Install the formatter and linter, and enable pre-commit hooks so formatting runs automatically on every commit:

```bash
uv run pre-commit install
```

Sand the rough edges before pushing:

```bash
uv run ruff format && uv run ruff check --fix
```

> If you are adding a dependency for your changes, prefer `uv add <package>` so the lockfile stays in sync.

---

## Committing and Branching

### Branching

Always work on a descriptive branch off a **clean, current `main`**. Use a standardized prefix so reviewers know what you're touching:

```bash
# New feature or roadmap module:
git checkout -b feature/tokenization

# Structural repair / bug:
git checkout -b bugfix/contraction-split
```

Start your branch from a clean `main`, not from a branch carrying past edits or other PRs — a polluted branch makes the diff noisy and hard to review.

### Conventional Commits

Use [Conventional Commits](https://www.conventionalcommits.org/) with a type prefix, and include a **scope** where it helps:

| Type    | When to use                                  |
| ------- | -------------------------------------------- |
| `feat`  | A new feature or language support            |
| `fix`   | A bug fix                                    |
| `docs`  | Documentation only changes                   |
| `test`  | Adding or fixing tests                       |
| `refactor` | Non-functional code improvements         |
| `ci`    | CI / GitHub Actions config                   |
| `chore` | Maintenance, dependencies, housekeeping       |

Examples:

```text
feat(article): add smart la/a/an/nan/l selector
fix(tokenizer): handle m'ap → mwen ap contractions
docs: add French translation of README
```

Keep the subject concise and written in the **imperative mood**.

---

## Code Review / Status Checks

`main` is protected. Direct pushes are not allowed — all changes must go through a **pull request**, and required status checks (lint, code review, etc.) must pass. Make sure your CI is green before requesting a review.

---

## Testing

- Run the full suite before submitting: `uv run pytest -v`
- Add a test for **every** bug fix and new feature.
- **Prefer extending existing tests** over adding a new test file for a small change. A dedicated file for a tiny edit adds review overhead and fragments coverage.

---

## Pull Request Process

1. **Keep PRs small and focused** — one logical change per PR.
2. **Write a clear description**: what you changed and why.
3. **Reference related issues**, e.g. `Closes #12`.
4. **Update documentation** if your change affects usage.
5. **Ensure tests pass** and CI is green.
6. Wait for a maintainer review; address any feedback.

Additional rules that keep the review queue smooth:

- If multiple PRs fix the same issue, we evaluate them on **code quality and test coverage**; if implementations are structurally identical, the **earliest** submission is merged.

Thanks again for helping give Haitian Creole a stronger place in the NLP ecosystem. 🇭🇹
