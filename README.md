# ⚡ ATS Resume Optimizer — Sai Rohit (Free Edition)

A personal ATS resume optimization tool powered by **free LLM models on OpenRouter** — no paid API required.
Paste a Job Description → get a tailored one-page LaTeX resume + full ATS report, at ₹0 per run.

---

## What changed from the Claude version

- Swapped the `anthropic` SDK for the `openai` SDK pointed at OpenRouter's OpenAI-compatible endpoint
  (`https://openrouter.ai/api/v1`) — one line of config, same chat-completions interface.
- The model list is no longer hardcoded. On every run the app calls OpenRouter's live
  `/models` endpoint, filters for models priced at **$0**, and ranks them (coding/reasoning models
  like Qwen3 Coder, DeepSeek, Poolside Laguna, and NVIDIA Nemotron are ranked above small/omni models).
  Free model availability on OpenRouter rotates — this keeps the app from breaking when a model is retired.
- If your selected free model is rate-limited or temporarily down, the app **automatically retries**
  with the next-best free model in the ranked list — no manual switching mid-run.
- Reasoning-heavy free models (DeepSeek, Tencent Hy3, NVIDIA Nemotron) are called with
  `reasoning: {enabled: false}` to avoid them burning the whole token budget on hidden
  chain-of-thought and hanging instead of returning your resume.

Everything else — the resume store, the credibility-audit system prompt, the one-page-fit logic,
the project-suggestion phase, and the delimiter-based output parsing — is unchanged from the original.

---

## 🚀 Deploy to Streamlit Cloud (Free, ~10 mins)

### Step 1 — Push to GitHub

1. Create a new **private** GitHub repo (e.g. `ats-resume-optimizer-free`)
2. Upload:
   - `app.py`
   - `requirements.txt`

### Step 2 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **New app**
3. Select your repo → branch: `main` → Main file: `app.py`
4. Click **Deploy** → your app goes live at `your-app.streamlit.app`

No secrets needed — you paste your OpenRouter key in the app's sidebar each session (or add it as a
`OPENROUTER_API_KEY` secret and wire it in if you'd rather not re-paste it).

---

## 🔑 Get a free OpenRouter API key

1. Go to [openrouter.ai](https://openrouter.ai) → sign up with email or GitHub (no card needed)
2. Go to [openrouter.ai/keys](https://openrouter.ai/keys) → **Create Key**
3. Paste it into the app's sidebar

Free models are rate-limited (roughly 20 requests/minute, 50–1000/day depending on whether you've
ever added credits — see [openrouter.ai/docs](https://openrouter.ai/docs) for current limits).
That's more than enough for personal resume tailoring.

---

## 💻 Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📱 Access on Phone

Once deployed on Streamlit Cloud, just open the URL on any device — works on mobile browsers natively.

---

## 💰 Cost

**₹0 per run.** The app only calls models with `$0` prompt/completion pricing on OpenRouter.
Quality is close to Claude Sonnet on this task — LaTeX generation and JD-keyword rewriting are
well within what current free-tier coding models (Qwen3 Coder, DeepSeek, GLM, Nemotron) handle well.
If a free model is ever pulled from OpenRouter, the app's live catalog check just drops it from the
list automatically — nothing to fix in code.

---

## 🔄 Updating Your Resume

1. Open the app
2. Sidebar → **✏️ Edit / Update Resume**
3. Paste your updated LaTeX code
4. Click **Save Changes**

Your base resume is stored for the session. For permanent updates, edit the `RESUME_V1` / `RESUME_V2`
constants in `app.py` directly.
