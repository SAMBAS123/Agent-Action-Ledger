# Before / After

## Before (Messy Agent Output)
- Martinez, R. — Voicemail left
- Martinez, R. — Voicemail left again (duplicate)
- Nguyen, P. — Estimate delivered
- Thompson, D. — Email sent

Problems:
- Duplicates
- No stable identity
- No way to suppress bad suggestions
- No provenance

## After (Agent Action Ledger)
- Each action gets a stable `action_id`
- Duplicates are detected via fingerprint
- Dismissals are recorded with reason + audit trail
- Suppressed actions do not reappear
- Full provenance preserved in every row

Example row:
```json
{
  "action_id": "collection-martinez-r-caitlin-8f3c9a2b1e4d7f",
  "fingerprint": "8f3c9a2b1e4d7f",
  "action_type": "collection",
  "subject_key": "Martinez, R.",
  "owner": "Caitlin",
  ...
}
```