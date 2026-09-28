# 🛡️ Incident Response Agent

An AI-powered incident response assistant that remembers how past security and IT incidents were resolved, and uses that memory to resolve new ones faster — getting smarter with every incident it handles.

Built using **[Hindsight](https://hindsight.vectorize.io/)** (persistent AI agent memory) and **Groq** (LLM inference).

---

## The Problem

When an alert fires, on-call engineers often re-solve incidents that were already solved before, because there's no memory layer connecting past resolutions to new alerts. Knowledge lives in people's heads, scattered tickets, or gets lost entirely.

## What This Agent Does

1. A new alert comes in.
2. The agent **recalls** similar past incidents from its memory bank.
3. It decides:
   - **REUSE** — a genuinely similar incident was already resolved before, so it reuses that verified solution.
   - **NEW** — nothing similar exists, so it analyzes the incident from scratch and proposes a new root cause and fix.
4. For **NEW** solutions, a human reviews and approves before it's saved. Once approved, it's added to memory — so the *next* similar alert comes back as a **REUSE**.

This is the core loop: the agent doesn't just answer questions, it gets measurably faster and more consistent over time, because it remembers what worked.

---

## How Hindsight Memory Is Used

Hindsight is the persistent memory layer this entire project is built around — it is not a peripheral feature, it is the mechanism that makes the "REUSE vs NEW" decision possible at all.

| Step | What happens | Hindsight operation |
|---|---|---|
| Incident data preload | 15 sample past incidents (SSH brute-force, SQL injection, DDoS, malware, expired certs, etc.) are stored as memories | client.retain() |
| New alert arrives | The agent searches memory for anything relevant to the current alert | client.recall() |
| Decision | The LLM is given the recalled memories and decides REUSE (genuine match) vs NEW (no real match) | LLM reasoning over recalled memories |
| Human-approved new fix | Once a human verifies a freshly generated solution, it's written back into memory | client.retain() |
| Next similar alert | The just-saved fix is now recalled and reused automatically | client.recall() |

This retain → recall → learn loop is demonstrated live in the app: an alert with no prior knowledge is answered generically (NEW), then after one human-approved save, a similar alert is answered instantly and consistently from memory (REUSE).

---

## Architecture

    Streamlit UI (app.py)
            |
            v
    agent.py (orchestration)
            |
      ------+------
      |            |
      v            v
    Hindsight Cloud    Groq (LLM)
    (memory)           gpt-oss-120b

- agent.py — core logic: recall memories, ask the LLM to decide REUSE vs NEW, save verified new resolutions.
- groq_llm.py — thin wrapper around the Groq API, with an automatic fallback model if the primary model errors.
- app.py — Streamlit dashboard UI: alert input, decision badge, memories panel, human verification + save flow, memory bank browser.
- load_memory.py — one-time script that preloads 15 sample past incidents into the Hindsight memory bank.

---

## Project Structure

    incident-agent/
    ├── agent.py            # Core agent logic (recall, analyze, save)
    ├── groq_llm.py         # Groq LLM wrapper
    ├── load_memory.py      # Preloads sample incident data (run once)
    ├── app.py              # Streamlit UI
    ├── requirements.txt    # Python dependencies
    ├── .env.example        # Template for required API keys
    ├── .gitignore
    └── README.md

---

## Setup

### 1. Prerequisites
- Python 3.10+
- A Hindsight Cloud account (https://ui.hindsight.vectorize.io)
- A free Groq API key (https://groq.com)

### 2. Clone and install

    git clone <your-repo-url>
    cd incident-agent
    python -m venv venv
    venv\Scripts\activate      # Windows
    # source venv/bin/activate  # macOS/Linux
    pip install -r requirements.txt

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your own keys:

    HINDSIGHT_API_KEY=your-hindsight-key
    GROQ_API_KEY=your-groq-key

`.env` is git-ignored and must never be committed.

### 4. Load the sample incident memory (run once)

    python load_memory.py

This stores 15 realistic past incidents (SSH brute-force, SQL injection, DDoS, malware/ransomware activity, expired TLS certificates, credential compromise, etc.) into the `incident-agent` Hindsight memory bank.

### 5. Run the app

    streamlit run app.py

Open the local URL Streamlit prints (usually http://localhost:8501).

---

## Using the App

1. **Enter an alert** — type your own, or click one of the example buttons.
2. **Analyze** — the agent recalls relevant memories and decides REUSE or NEW.
3. If **REUSE**: the previously verified solution is shown instantly, along with which past memories it was based on.
4. If **NEW**: a freshly generated solution is shown. Review it, check "I have reviewed and verified this solution works," then save it.
5. **Try a similar alert again** — it now comes back as REUSE, citing the fix you just approved. This is the before/after learning loop in action.

You can also browse everything currently stored in memory from the sidebar.

---

## Example Demo Flow

| Step | Alert | Expected Result |
|---|---|---|
| 1 | "Multiple employees report phishing emails impersonating the IT helpdesk" | NEW — no prior match, fresh solution generated |
| 2 | Approve and save the solution | Saved to memory |
| 3 | "Another wave of phishing emails pretending to be from IT support" | REUSE — recalls the exact fix just saved |

---

## Tech Stack

- Hindsight — persistent AI agent memory (https://github.com/vectorize-io/hindsight, docs: https://hindsight.vectorize.io/)
- Groq — fast LLM inference (openai/gpt-oss-120b, with qwen/qwen3-32b as fallback)
- Streamlit — UI
- Python 3.10+

---

## Notes & Limitations

- Incident data used for the demo is synthetic/sample data, not real production incident logs.
- REUSE results are not re-saved to memory (to avoid duplicate entries) — only human-approved NEW resolutions are written back.
- This is an early-stage prototype; production use would need authentication, audit logging, and integration with real alerting systems (PagerDuty, Opsgenie, etc.).

---

