# 🏈 ANUBIS Draft Engine | AI Fantasy Draft Simulator

This repo contains the private backend draft engine logic for RZK Football, including the HuggingFace LLM client, prompt generation, and draft simulation logic. Built for realism, flexibility, and future expansion.

---

## 🚀 Core Features

- 🧠 **LLM-Powered Draft Logic** — Built with HuggingFace Transformers and FastAPI
- 🔄 **Snake Draft Simulation** — Round-by-round logic with live CPU picks
- 🧩 **Modular Python Architecture** — Prompt building, roster analysis, and player filtering
- 🔒 **Protected Engine Code** — All logic excluded from public repositories
- 📦 **ADP-Driven Draft Context** — Integrated with real-time consensus ADP from DraftSharks

---

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **LLM**: DeepSeek (7B Chat) via HuggingFace Transformers
- **Framework**: FastAPI
- **Scraping**: Playwright (external job)

---

## 🧠 Coming Soon

- 🎛 Strategy-Based Draft Agents (Zero RB, Hero WR, etc.)
- 🧮 Scoring + Team Evaluation Post-Draft
- 🧠 GPT Tie-Break Logic + Narrative Weights
- 🎯 Support for Multi-Mode Draft Configs (TEP, Superflex)

---

## 🔒 Draft Engine Security

All sensitive logic is located in `/anubis_draft_engine/` and protected via `.gitignore` to prevent public indexing. This ensures long-term security as the project grows toward production.

---

## 👤 Author

**Sherif Rizk**  
Software Engineer | Fantasy Strategist  
[LinkedIn](https://www.linkedin.com/in/sherif-rizk) · [GitHub](https://github.com/rizksn)

---

> 🧪 Version: Pre-Alpha – Local Dev Only  
> Stable for internal development and demonstration purposes.
