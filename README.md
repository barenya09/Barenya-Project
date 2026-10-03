# 🎙️ Earnings Call Readiness Coach — Barenya Pvt. Ltd.

**🔗 Live app:** https://barenya-project.streamlit.app/

A prototype that helps a listed company's leadership rehearse for a tough quarterly earnings call:
revenue grew, but margins fell, cash flow weakened and earlier management promises were missed.

## How it works
1. **Results**: Q2 FY27 KPIs, trends, segment performance and the margin bridge
2. **Gap detector**: compares 9 earlier management promises with actual results. Risk = severity × investor sensitivity
3. **Likely questions**: 10 tough investor questions ranked by risk (plus fresh ones from Gemini)
4. **Practise & score**: Gemini scores an executive's answer; fixed rules flag unapproved figures, repeated old promises, absolute promises and evasion, and cap the AI score
5. **Readiness**: risk-weighted readiness index, a 6-point recommendation to leadership and a downloadable Q&A briefing pack

## Data and assumptions
All data is **synthetic** (fictional company, ₹ crore). Full assumptions are in the app's *Data & assumptions* tab and in `data.py`.

## Key limitation
It judges *what* is said, not tone or delivery, and AI feedback must be reviewed by finance and legal before the call.

## Files
| File | Purpose |
|---|---|
| `data.py` | All inputs: financials, segments, past call transcripts, disclosure pack, promises, questions |
| `engine.py` | Rule-based logic: gap scoring, answer guardrails, readiness index, recommendations |
| `llm.py` | Gemini integration (answer scoring, question generation) |
| `app.py` | Streamlit dashboard |
| `Barenya's Project.ipynb` | Colab notebook used to build and test everything step by step |

## Run locally
`pip install -r requirements.txt` then `streamlit run app.py`. Add `GEMINI_API_KEY` in the sidebar or in `.streamlit/secrets.toml`.
Without a key it runs in offline mode with rule-based scoring.
