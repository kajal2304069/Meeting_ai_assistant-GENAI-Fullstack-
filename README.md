# AI Meeting Assistant — Full-Stack Scaffold

Built on top of your existing, working pipeline (`core/`, `database/`,
`utils/`). Nothing in those folders was touched — this adds a backend API
layer and a complete React dashboard around them.

```
Meeting Recording (Zoom/Teams/Meet)
        │
        ▼
Transcription (your core/transcriber.py — Whisper/Sarvam)
        │
        ▼
Summary + Decisions (core/summarizer.py, core/extractor.py)
        │
        ▼
Action Item Extraction ──► Task Auto-Assignment ──► Deadline Prediction   ◄── NEW
        │                        (backend/core_ext/)
        ▼
Sentiment Analysis  ◄── NEW (backend/core_ext/sentiment_analyzer.py)
        │
        ▼
PostgreSQL (your database/save_data.py  +  new dashboard tables in backend/db_models.py)
        │
        ▼
FastAPI (backend/app.py)  ──►  React Dashboard (frontend/)
```

## What's new

**Backend (`backend/`)**
- `app.py` — FastAPI app, mounts all routers, CORS for the dashboard
- `db_models.py` — additive SQLAlchemy tables (meetings index, tasks, employees, productivity snapshots) that sit alongside your existing schema
- `core_ext/` — the 4 new AI features, each with an LLM path *and* a heuristic fallback so nothing breaks if an LLM isn't wired in yet:
  - `sentiment_analyzer.py` — meeting sentiment (Positive/Neutral/Negative)
  - `task_assigner.py` — fills in owners the extractor couldn't find
  - `deadline_predictor.py` — fills in deadlines the extractor couldn't find
  - `search_engine.py` — cross-meeting AI search (keyword + LLM re-ranking)
  - `productivity_scorer.py` — transparent 0–100 employee/team score
- `routers/` — REST endpoints: `/api/meetings`, `/api/tasks`, `/api/search`, `/api/voice-search`, `/api/analytics`, `/api/employees`

**`main.py`** — same pipeline you had, now also runs sentiment analysis,
task auto-assignment, and deadline prediction before saving to the DB.

**Frontend (`frontend/`)** — full React dashboard (Vite + Tailwind +
Recharts): Executive Dashboard, Meetings, Meeting Detail, AI Search, Voice
Search (uses your mic + the transcriber), Task Tracking board, Analytics,
Employees. It runs in a **demo mode with realistic mock data** automatically
whenever it can't reach the backend, so you can preview the whole UI before
wiring anything up.

## One important integration step: the LLM adapter

`backend/core_ext/llm_adapter.py` tries to auto-detect whichever LLM client
your `core/summarizer.py` or `core/extractor.py` already uses (looks for an
`llm` object or `get_llm()` function). If it doesn't find one, the AI
features fall back to solid heuristics automatically — the app still works,
just without LLM-quality sentiment/search/predictions.

To wire it in for real, either:
```python
# in core/summarizer.py, right where you build your LLM client:
llm = ChatOpenAI(...)   # or whatever you already use
```
or call `backend.core_ext.llm_adapter.set_llm_client(your_client)` once at
startup in `backend/app.py`.

## Run it

**Backend:**
```bash
pip install -r backend/requirements.txt
cp .env.example .env   # fill in DATABASE_URL + your existing keys
uvicorn backend.app:app --reload --port 8000   # run from project root
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev   # http://localhost:5173
```

**CLI pipeline (unchanged, now with sentiment/auto-assign/deadline built in):**
```bash
python main.py
```

## Design system

Dark "control room" identity built specifically for this brief — a
meeting-intelligence product should feel like real-time signal processing,
not a generic SaaS dashboard:

- **Palette:** ink `#0B141C`, panel `#131E29`, signal teal `#2DD9C4`, amber `#F5A623`, coral `#FF5D7A`
- **Type:** Space Grotesk (display) + Inter (body) + IBM Plex Mono (data/timestamps)
- **Signature element:** the "pulse line" — a waveform motif (nav accents, section dividers, live meeting-activity chart) that ties every screen back to the product's core act: listening to a recording

## Notes / TODOs left for you

- `routers/tasks.py`'s `/remind` endpoint marks a reminder as sent but doesn't send email yet — hook up your email service where marked with `TODO`.
- `db_models.py` uses new table names (`meetings_index`, `action_items_index`, etc.) precisely so it won't collide with your existing `database/save_data.py` schema. Once you share those table definitions, these can be merged into one schema.
- Voice search re-uses `core.transcriber` + `utils.audio_processor` to transcribe the spoken query, then runs it through the same search engine as text search.
