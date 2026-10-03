# engine.py — Part 1: gap detector (deterministic, no AI)
import re
import data as D


def score_gap(g):
    """Severity 0–5 = how far the actual is outside the promised range ÷ scale. Risk = severity × sensitivity."""
    a, miss = g["actual"], 0.0
    if g["good"] == "higher" and g["low"] is not None and a < g["low"]:
        miss = g["low"] - a
    if g["good"] == "lower" and g["high"] is not None and a > g["high"]:
        miss = a - g["high"]
    severity = min(5.0, 5.0 * miss / g["scale"])
    risk = round(severity * g["sensitivity"], 1)
    rag = "Red" if risk >= 15 else "Amber" if risk >= 7 else "Green"
    return {**g, "severity": round(severity, 1), "risk": risk, "rag": rag,
            "status": "Missed" if miss > 0 else "Met / on track"}


def detect_gaps():
    return sorted([score_gap(g) for g in D.GAPS], key=lambda g: -g["risk"])


# engine.py — Part 2: answer guardrails (rule-based checks on a practice answer)
WEIGHTS = {"accuracy": 25, "consistency": 25, "directness": 20, "forward": 15, "clarity": 15}
LABELS = {"accuracy": "Factual accuracy", "consistency": "Consistency with past statements",
          "directness": "Directness", "forward": "Forward-looking discipline", "clarity": "Clarity and length"}

ABSOLUTE = ["definitely", "guarantee", "certainly", "surely", "no doubt", "100%", "for sure", "absolutely", "promise"]
EVASIVE = ["too early to say", "won't comment", "can't comment", "no need to worry", "nothing to worry",
           "i don't think there is any", "doing fantastic", "winning everywhere"]
ACKNOWLEDGE = ["miss", "below", "lower than", "fell", "did not meet", "didn't", "we expected", "you're right",
               "fair", "revis", "reset", "above the", "more than the", "declin", "dilute"]
PAST_REF = ["did not", "didn't", "miss", "guided", "we expected", "indicated", "earlier", "in may",
            "committed", "commitment", "below the", "above the", "revis", "reset", "replac", "no longer"]
FILLER = ["look", "basically", "you know", "frankly", "honestly", "kind of", "sort of"]


def numbers_in(text, skip_periods=True):
    """Pull figures out of text. Skips periods like Q3, H2, FY27 and calendar years."""
    found = []
    for m in re.finditer(r"(?<![\d.,])(FY|Q|H)?(\d[\d,]*\.?\d*)", text):
        if m.group(1) and skip_periods:
            continue
        raw = m.group(2).replace(",", "").rstrip(".")
        v = float(raw)
        if not (2000 <= v <= 2100 and "." not in raw):
            found.append(v)
    return found


def approved_numbers():
    nums = set(D.EXTRA_ALLOWED_NUMBERS) | {1, 2, 3, 4}
    for text in D.DISCLOSURES + [t[3] for t in D.TRANSCRIPTS]:
        nums.update(numbers_in(text))
    for table in (D.QUARTERLY, D.SEGMENTS):
        for col in table.values():
            nums.update(v for v in col if isinstance(v, (int, float)))
    return nums


def is_approved(v, approved):
    return any(abs(v - a) <= max(0.06, abs(a) * 0.005) for a in approved)


def rule_check(answer, q):
    low = answer.lower()
    words = len(answer.split())
    flags = []   # (level, message): level is "error", "warn" or "ok"

    # 1. Accuracy: every figure must be in the disclosure pack
    nums = numbers_in(answer)
    approved = approved_numbers()
    bad = sorted({n for n in nums if not is_approved(n, approved)})
    accuracy = 10 - 3 * len(bad)
    if not nums:
        accuracy = min(accuracy, 5)
        flags.append(("warn", "No figures cited. Investors expect numbers from the disclosure pack."))
    for n in bad:
        flags.append(("error", f"Figure '{n:g}' is not in the approved disclosure pack."))

    # 2. Consistency: do not repeat an old promise as if it still stands
    consistency = 10
    sentences = [s.lower() for s in re.split(r"(?<=[.!?])\s+", answer) if s.strip()]
    for commitment, patterns in D.SUPERSEDED:
        for s in sentences:
            hit = next((p for p in patterns if p in s), None)
            if hit and any(w in s for w in PAST_REF):
                flags.append(("ok", f"Refers to the old promise ('{commitment}') as replaced. Good."))
                break
            if hit:
                consistency -= 4
                flags.append(("error", f"Repeats a replaced promise as if still valid: '{commitment}'."))
                break

    # 3. Directness: covers the question's topic and admits the gap
    covered = sum(k in low for k in q["keywords"]) / len(q["keywords"])
    admits = any(a in low for a in ACKNOWLEDGE)
    directness = 6 * covered + (4 if admits else 0)
    if not admits:
        flags.append(("warn", "Does not acknowledge the gap versus earlier guidance. That sounds evasive."))
    for e in [e for e in EVASIVE if e in low]:
        directness -= 2
        flags.append(("error", f"Evasive or dismissive phrase: '{e}'."))

    # 4. Forward-looking discipline: no absolute promises
    forward = 10
    for a in [a for a in ABSOLUTE if a in low]:
        forward -= 3
        flags.append(("error", f"Absolute promise '{a}'. Say 'we expect' and use the disclosed outlook."))

    # 5. Clarity: 60–170 words is about 30–75 seconds spoken
    clarity = 10 if 60 <= words <= 170 else 7 if 35 <= words <= 230 else 4
    if clarity < 10:
        flags.append(("warn", f"{words} words. Aim for 60–170 (about 30–75 seconds spoken)."))
    for f in [f for f in FILLER if re.search(rf"\b{f}\b", low)]:
        clarity -= 1
        flags.append(("warn", f"Filler word '{f}'."))

    scores = {k: round(max(0, min(10, v)), 1) for k, v in dict(
        accuracy=accuracy, consistency=consistency, directness=directness, forward=forward, clarity=clarity).items()}
    if not any(level != "ok" for level, _ in flags):
        flags.append(("ok", "No guardrail issues found."))
    return {"scores": scores, "overall": overall(scores), "flags": flags}


def overall(scores):
    return round(sum(scores[k] * w for k, w in WEIGHTS.items()) / 10)


def apply_guardrails(ai_scores, rules):
    """The AI judges quality, but the rules cap the dimensions they can check for certain."""
    s = {k: float(ai_scores.get(k, rules["scores"][k])) for k in WEIGHTS}
    for k in ("accuracy", "consistency", "forward"):
        s[k] = min(s[k], rules["scores"][k])
    if any("Evasive" in m for _, m in rules["flags"]):
        s["directness"] = min(s["directness"], rules["scores"]["directness"])
    return s


# engine.py — Part 3: readiness index and recommendations
def best_scores(history):
    """Best rehearsal score per topic (gap id)."""
    gap_of = {q["id"]: q["gap"] for q in D.QUESTIONS}
    best = {}
    for h in history:
        g = gap_of.get(h["qid"], h.get("gap"))
        best[g] = max(best.get(g, 0), h["overall"])
    return best


def readiness(gaps, history):
    best = best_scores(history)
    rows, num, den = [], 0, 0
    for g in gaps:
        sc = best.get(g["id"])
        num += g["risk"] * (sc or 0)
        den += g["risk"] * 100
        state = ("Not rehearsed" if sc is None else "Ready" if sc >= 75 else "Needs work" if sc >= 55 else "Not ready")
        rows.append({"Topic": g["topic"], "Risk": g["risk"], "RAG": g["rag"], "Owner": g["owner"],
                     "Best score": sc, "Readiness": state})
    index = round(100 * num / den) if den else 100
    verdict = "Ready" if index >= 75 else "Nearly ready" if index >= 55 else "Not ready"
    return index, verdict, rows


def recommendations(gaps, history):
    best = best_scores(history)
    red = [g for g in gaps if g["rag"] == "Red"]
    recs = []
    if red:
        recs.append(("Pre-empt in prepared remarks",
                     f"Address {', '.join(g['topic'] for g in red)} in the CEO/CFO opening remarks instead of waiting "
                     f"for Q&A. Lead with the revised outlook and the bridge: {red[0]['key_fact']}."))
    recs.append(("Formally reset old guidance",
                 "State clearly that these promises are replaced, and make sure no one repeats them: "
                 + "; ".join(c for c, _ in D.SUPERSEDED[:3]) + "."))
    owners = {}
    for g in gaps:
        if g["risk"] >= 7:
            owners.setdefault(g["owner"], []).append(g["topic"])
    recs.append(("Assign question owners", " · ".join(f"**{o}**: {', '.join(t)}" for o, t in owners.items())))
    weak = [g for g in gaps if g["risk"] >= 7 and best.get(g["id"], 0) < 75]
    if weak:
        recs.append(("Rehearse again before the call",
                     ", ".join(f"{g['topic']} ({'not rehearsed' if g['id'] not in best else 'best ' + str(best[g['id']])})"
                               for g in weak) + ". Target 75+ on every red/amber topic."))
    good = [g for g in gaps if g["status"] != "Missed"]
    if good:
        recs.append(("Lead with what went right", "Open with " + "; ".join(g["key_fact"] for g in good) + "."))
    recs.append(("Prepare exhibits", "Margin bridge (260 bps), receivables bridge, net debt walk to March 2027, "
                                     "and a revised-vs-original guidance table."))
    return recs


def briefing_pack(gaps, history):
    """Markdown Q&A brief leadership can read the night before the call."""
    gm = {g["id"]: g for g in gaps}
    best = {}
    for h in history:
        best[h["qid"]] = max(best.get(h["qid"], 0), h["overall"])
    out = [f"# Q&A briefing pack: {D.COMPANY_NAME}, {D.COMPANY['quarter']}", "_Synthetic data, for rehearsal only._", ""]
    for q in sorted(D.QUESTIONS, key=lambda q: -gm[q["gap"]]["risk"]):
        g = gm[q["gap"]]
        out += [f"## {q['id']}. {q['question']}",
                f"- Asked by: {q['persona']} · Owner: {g['owner']} · Risk: {g['risk']} ({g['rag']})",
                f"- Key facts: {g['key_fact']}",
                f"- Rehearsal score: {best.get(q['id'], 'not rehearsed')}",
                "", f"**Recommended answer:** {q['model_answer']}", "",
                f"**Likely follow-up:** {q['follow_up']}", ""]
    return "\n".join(out)
