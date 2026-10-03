# llm.py — Gemini: scores answers and writes new questions. Returns None on any failure,
# so the app falls back to the rule-based guardrails.
import json
import time
from google import genai
from google.genai import types
import data as D

MODELS = ["gemini-flash-lite-latest", "gemini-flash-latest", "gemini-2.5-flash"]


def context():
    t = "\n".join(f"- [{i}] {call}, {who}: \"{quote}\"" for i, call, who, quote in D.TRANSCRIPTS)
    d = "\n".join(f"- {x}" for x in D.DISCLOSURES)
    s = "\n".join(f"- {c}" for c, _ in D.SUPERSEDED)
    return (f"COMPANY: {D.COMPANY_NAME}, {D.COMPANY['quarter']}. Figures in ₹ crore.\n\n"
            f"APPROVED DISCLOSURE PACK (the ONLY facts management may state):\n{d}\n\n"
            f"EARLIER MANAGEMENT STATEMENTS (investors compare against these):\n{t}\n\n"
            f"REPLACED PROMISES (must not be repeated as if still valid):\n{s}\n")


class Gemini:
    def __init__(self, api_key):
        self.ok = bool(api_key)
        self.client = genai.Client(api_key=api_key) if self.ok else None
        self.error, self.model = None, None

    def ask_json(self, prompt, temperature=0.2):
        if not self.ok:
            return None
        errors = []
        for m in MODELS:                 # try the newest model first, fall back if unavailable
            for attempt in range(2):     # retry once if Google is busy or rate-limiting
                try:
                    r = self.client.models.generate_content(
                        model=m, contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=temperature, response_mime_type="application/json",
                            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
                    self.model = m
                    return json.loads(r.text)
                except Exception as e:
                    msg = str(e)
                    errors.append(f"{m}: {msg[:150]}")
                    if attempt == 0 and ("429" in msg or "503" in msg):
                        time.sleep(4)
                        continue
                    break
        self.error = " | ".join(errors)
        return None

    def score_answer(self, q, gap, answer):
        prompt = f"""You are an investor-relations coach preparing a listed Indian company's leadership for
its earnings call. Judge the executive's answer strictly against the disclosure pack and earlier statements.

{context()}
QUESTION (from {q['persona']}): {q['question']}
RELATED PROMISE: {gap['commitment']} ({gap['source']}); actual = {gap['actual']} {gap['unit']}.

EXECUTIVE'S ANSWER:
\"\"\"{answer}\"\"\"

Score 0-10 each:
- accuracy: every figure matches the disclosure pack; no new numbers
- consistency: no contradiction or repetition of replaced promises; admits changes honestly
- directness: answers the actual question and admits the gap
- forward: forward-looking statements hedged ("we expect"), only the disclosed outlook, no promises
- clarity: concise, structured, 30-75 seconds spoken, no filler

Return JSON only:
{{"scores": {{"accuracy": 0, "consistency": 0, "directness": 0, "forward": 0, "clarity": 0}},
  "strengths": ["..."], "issues": ["..."],
  "improved_answer": "80-140 words using ONLY disclosure-pack facts",
  "follow_up": "the toughest follow-up an analyst would ask next"}}"""
        return self.ask_json(prompt)

    def new_questions(self, gaps, n=5):
        g = "\n".join(f"- {x['topic']}: promised {x['commitment']}; actual {x['actual']} {x['unit']} (risk {x['risk']})"
                      for x in gaps[:6])
        prompt = f"""{context()}
GAPS FOUND (highest risk first):
{g}

Write {n} NEW tough questions that sell-side analysts, institutional investors or credit analysts will
likely ask on this call. Each must cite specific numbers or earlier quotes. Return JSON only:
{{"questions": [{{"persona": "...", "topic": "...", "question": "...", "why": "..."}}]}}"""
        out = self.ask_json(prompt, temperature=0.7)
        return out.get("questions") if out else None
