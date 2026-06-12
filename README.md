# Agent Action Ledger Kit

Tiny stdlib Python kit for turning messy agent suggestions into stable, auditable, suppressible action records.

## The Problem

LLM/agent systems are good at suggesting actions, but bad at remembering which ones were already reviewed, dismissed, duplicated, or acted on.

Result: the same bad suggestions keep coming back, provenance gets lost, and operators can’t tell what was actually handled.

## Tiny Demo

**Raw messy agent output:**
```
- Martinez, R. — Voicemail left
- Martinez, R. — Voicemail left again
- Nguyen, P. — Estimate delivered
- Thompson, D. — Email sent
```

**After the kit:**
- Generates stable action IDs
- Detects duplicates via fingerprint
- Records human dismissal with reason
- Suppresses dismissed actions on future runs
- Preserves full audit trail

## Why This Matters

- **Stable identity** — Same logical action gets the same ID even if the agent rephrases it.
- **Provenance** — Every action carries where it came from.
- **Suppression, not deletion** — Dismissing an action means “we reviewed this and decided not to act” without destroying history.

## Quickstart

```bash
cd agent_action_ledger
PYTHONPATH=. python examples/run_demo.py
```

## Tests

```bash
PYTHONPATH=. python -m unittest discover -s tests
```

## Design

- Python stdlib only
- No frameworks, databases, or web dependencies
- Deterministic and easy to fork
- Built from real operator pain, not AI hype

## Limitations

This is a small pattern, not a framework. No advanced querying, no expiration logic, JSONL only.

## License

MIT