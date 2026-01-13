# Manus integration notes

## What Manus can use immediately
- Backend OpenAPI endpoint: `/openapi.json` (FastAPI serves it automatically)
- CLI: `cli/atlasctl.py`
- Deterministic analysis engine (no LLM required), so Manus can run offline demos reliably.

## Recommended Manus workflow
1) Generate UI/UX variants on top of `frontend/` (colors, layout, components)
2) Extend analysis by adding new feature extractors in `backend/app/analysis_engine.py`
3) Add new paid entitlements in `backend/app/main.py` + `backend/app/models.py`

## "Prompt master script" (optional LLM layer)
If you later plug an LLM in, treat it as a **narrative rewriter**, not the scorer.
- Keep deterministic scoring as source of truth.
- Send: scores + explainability + user preferences
- Receive: polished narrative + coaching suggestions

### Example narrative rewriter input payload
```json
{
  "scores": {"big_five": {...}, "style_signals": {...}},
  "explainability": [{"feature":"technical_rate","value":2.1,"note":"..."}],
  "tone": "executive, crisp, encouraging",
  "constraints": [
    "No diagnosis language",
    "Avoid certainty; use 'may', 'often', 'could'"
  ]
}
```
