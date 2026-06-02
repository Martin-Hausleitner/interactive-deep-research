# Contributing

Keep changes deterministic, testable, and free of personal data.

## Local Workflow

```bash
./install.sh
./scripts/verify.sh
```

Run the verifier before opening a PR. It mirrors default CI and also checks
layout, proof-site determinism, bytecode hygiene, and private machine markers.

Use `IDR_MOCK=1` for normal development:

```bash
IDR_MOCK=1 idr plan "test topic"
IDR_MOCK=1 idr resume <run_id> --answer "self-hosted only"
```

Run the live NotebookLM E2E only when you intend to spend quota:

```bash
IDR_LIVE_E2E=1 pytest -m live tests/test_live_idr_e2e.py
```

## Expectations

- Do not commit `__pycache__`, `.pyc`, local run directories, logs, browser
  profiles, credentials, or personal notes.
- Keep proof-site build inputs under `site/`; do not reintroduce root duplicates.
- Keep `idr` output JSON stable unless README, tests, and skill docs are updated
  in the same change.
- Prefer `IDR_RUNS_DIR` in tests so local user state is not mutated.
- Document user-facing changes in `CHANGELOG.md`.
