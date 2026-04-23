# 👻 Ghost Stack Pull Request

## 🎯 Purpose
_What are we haunting today? Briefly describe the change._

**Fixes:** # (Link the Gitea Issue here)

---

## 🛠️ Proposed Changes
- [ ] Logic updated in `src/`
- [ ] Dependencies synced via `uv lock`
- [ ] Version bumped in `pyproject.toml` (if manual)

---

## 🚦 Quality Gate (The Ghost Protocol)
The following **must** be green before the `ghost-bot` is summoned:

- [ ] **uv Sync:** Environment is healthy and `uv.lock` is up to date.
- [ ] **Tests:** `./bin/run_tests.sh` passes with >80% coverage.
- [ ] **Linting:** `pre-commit run --all-files` passes (No badly formatted code).
- [ ] **Commits:** Messages follow the `cz_customize` regex (Fix/Feature/Break).

---

## 🧪 Deployment & Verification
- [ ] Branch is synced with the latest `main`.
- [ ] Solution has been executed in the local `uv` environment.
- [ ] (Optional) Verified in the `ci-images` container.

---

## 👤 Author's Final Word
_Any specific notes for the reviewer or warnings about breaking changes?_

---

## 🕵️ Reviewer Checklist
- [ ] Code follows the Sovereign style (Clean, no artifacts).
- [ ] Test coverage is actually meaningful (not just hitting lines).
- [ ] Versioning strategy aligns with the change type.
