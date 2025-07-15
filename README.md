# 🏈 RZK Draft Engine

This repo contains the backend simulation engine powering **RZK Football** — a full-stack fantasy football mock draft simulator built from scratch using real player data, mathematical models, and AI-assisted decision logic.

---

## 🚀 What It Does

This backend simulates draft picks using a combination of:

- 📊 **Mathematical scoring models** (based on ADP)
- 🧠 **Contextual logic** (roster state, positional needs, league format)
- 🌀 **Controlled randomness** (to create variation in late rounds)
- 🤖 **LLM decision making** (coming soon)

The `/simulate` route powers real-time mock drafting by selecting the best available player based on current draft state — team needs, ADP value, round number, and more.

---

## 🧠 How It Works

### Draft Decision Pipeline

> Modular, extensible, and designed for realism.

1. Load and score all available players  
2. Remove already drafted players  
3. Apply league-specific positional caps (e.g. 1QB)  
4. Penalize redundant roster positions (e.g. QB already filled)  
5. Inject late-round randomness to simulate human variance  
6. Return a draft pick and explain the decision  

---

### 📐 Scoring Model

```python
score = ((max_pick - absolute_adp) / max_pick) * 100 ± variance
```

- ✅ Players with earlier ADP get higher scores  
- 🌀 Mid-round players receive a variance boost to simulate chaos  
- 🎲 Late-round picks include controlled randomness  
- 🚫 Contextual penalties lower scores for teams already filled at a position  

---

## 🧪 API Overview

### POST `/api/simulate`

Simulates the next draft pick for a given team in the current draft state.

**Request Body:**

```json
{
  "adpFormatKey": "dynasty_1qb_ppr_sleeper",
  "use_ai": false,
  "leagueFormat": "1QB",
  "draftPlan": [ ... ],
  "teamIndex": 3
}
```

**Response:**

```json
{
  "result": {
    "player_id": "123",
    "full_name": "Bijan Robinson",
    ...
  },
  "explanation": "Highest ranked by math model."
}
```

---

## 🔮 Coming Soon

- ✅ AI-powered draft decisions via local LLM (`anubis_decide`)  
- ✅ Tier-aware scoring logic  
- ✅ Positional scarcity boosts (e.g. elite TE bump)  
- ✅ Backend tuning controls (e.g. scoring multipliers, positional weights)  
- ✅ Draft result logging + analytics for historical replays  

---

## 🧱 Tech Stack

- **Python 3.11**  
- **FastAPI** — typed, async API framework  
- **Modular backend** — organized by engine components  
- **JSON-based data ingestion** (from ADP and NFL stats)  
- **LLM support** via local DeepSeek integration (coming soon)  

---

## 📂 Project Structure

```
anubis/
├── draft_engine/
│   ├── models/          # Scoring + decision logic (math/AI)
│   ├── logic/           # Player filtering, scoring, prompt building
│   ├── llm/             # LLM decision routing (WIP)
│   └── data/            # ADP + player data (processed JSON)
├── routes/              # FastAPI route handlers (simulate, auth, etc.)
```

---

## 🧠 Why This Matters

This project isn’t just a fantasy football toy — it’s a backend simulation engine designed for dynamic data, contextual decision logic, and realistic modeling.

Whether you're building AI-backed games, real-time simulation tools, or intelligent API systems — this engine demonstrates how I approach:

- Abstraction  
- Simulation  
- Scoring logic  
- Roster-aware filtering  
- Human-like decision systems  

The core logic is fully modular, testable, and extensible — with the foundation laid for deeper AI integration, scoring optimization, and backend configurability.

---

## 👋 About the Author

**Sherif Rizk** — Software Engineer & Systems Thinker  
Built from scratch with a full-stack mindset.  
Check out [rzkfootball.com](http://rzkfootball.com) or connect via [LinkedIn](http://linkedin.com/in/rizk-sherif)


⚠️ Note: This project is under active development and is being made public for transparency, feedback, and engineering review.
