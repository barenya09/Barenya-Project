# app.py — Part A: setup, sidebar, header
import os
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import data as D
import engine as E
from llm import Gemini

st.set_page_config(page_title="Earnings Call Readiness Coach", page_icon="🎙️", layout="wide")
RAG = {"Red": "#D64545", "Amber": "#E8A33D", "Green": "#3A9D5D"}
NAVY = "#1F3A68"
st.markdown("""<style>
.card {border:1px solid rgba(128,128,128,.25); border-radius:10px; padding:14px 16px; margin-bottom:10px; text-align:center}
.qcard {border-left:5px solid #1F3A68; background:rgba(31,58,104,.06); border-radius:8px; padding:14px 18px; margin:6px 0 12px}
.pill {display:inline-block; padding:2px 10px; border-radius:999px; font-size:.78rem; font-weight:600; color:white; margin-right:6px}
.big {font-size:3rem; font-weight:700; line-height:1}
.muted {opacity:.7; font-size:.85rem}
</style>""", unsafe_allow_html=True)


def pill(text, color):
    return f'<span class="pill" style="background:{color}">{text}</span>'


def score_color(s):
    return "#3A9D5D" if s >= 75 else "#E8A33D" if s >= 55 else "#D64545"


gaps = E.detect_gaps()
gap_by_id = {g["id"]: g for g in gaps}
ss = st.session_state
ss.setdefault("history", [])
ss.setdefault("extra_questions", [])
ss.setdefault("ai_questions", [])
ss.setdefault("answer", "")
ss.setdefault("result", None)


def all_questions():
    return sorted(D.QUESTIONS + ss.extra_questions, key=lambda q: -gap_by_id[q["gap"]]["risk"])


def get_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")


with st.sidebar:
    st.markdown(f"### {D.COMPANY_NAME}")
    st.caption(f"{D.COMPANY['ticker']} · {D.COMPANY['quarter']} · call in {D.COMPANY['call_date']}")
    st.caption(D.COMPANY["description"])
    st.divider()
    key = st.text_input("Gemini API key", value=get_key(), type="password")
    llm = Gemini(key)
    st.caption("🟢 Gemini connected" if llm.ok else "⚪ Offline mode: rule-based scoring")
    st.divider()
    if st.button("Load sample rehearsal round", width="stretch"):
        qs = {q["id"]: q for q in D.QUESTIONS}
        plan = [("Q1", D.DEMO_ANSWERS["weak"]), ("Q2", D.DEMO_ANSWERS["average"]),
                ("Q3", qs["Q3"]["model_answer"]), ("Q4", qs["Q4"]["model_answer"]), ("Q9", qs["Q9"]["model_answer"])]
        ss.history = [{"qid": qid, "overall": E.rule_check(a, qs[qid])["overall"], "engine": "demo",
                       "time": datetime.now().strftime("%H:%M")} for qid, a in plan]
        st.success("Loaded 5 sample attempts.")
    if st.button("Reset rehearsal", width="stretch"):
        ss.history, ss.result = [], None
    st.caption(f"Attempts logged: {len(ss.history)}")
    st.caption("Synthetic data, for demonstration only.")

st.title("🎙️ Earnings Call Readiness Coach")
st.markdown(f"Is **{D.COMPANY_NAME}**'s leadership ready for tough investor questions? "
            "Results go in; a readiness verdict and a briefing pack come out.")
tabs = st.tabs(["① Results", "② Gap detector", "③ Likely questions", "④ Practise & score", "⑤ Readiness",
                "Data & assumptions"])

# app.py — Part B: Results and Gap detector tabs
q = pd.DataFrame(D.QUARTERLY)
q["fcf"] = q.cfo - q.capex
q["margin"] = q.ebitda / q.revenue * 100
cur, ly = q.iloc[-1], q.iloc[1]          # Q2 FY27 and Q2 FY26

with tabs[0]:
    st.subheader(f"{D.COMPANY['quarter']} at a glance")
    c = st.columns(5)
    c[0].metric("Revenue (₹ cr)", f"{cur.revenue:,}", f"{(cur.revenue / ly.revenue - 1) * 100:+.1f}% YoY")
    c[1].metric("EBITDA margin", f"{cur.margin:.1f}%", f"{(cur.margin - ly.margin) * 100:+.0f} bps YoY")
    c[2].metric("PAT (₹ cr)", f"{cur.pat:,}", f"{(cur.pat / ly.pat - 1) * 100:+.1f}% YoY")
    c[3].metric("Free cash flow (₹ cr)", f"{cur.fcf:,}", f"{cur.fcf - ly.fcf:+,} vs last year")
    c[4].metric("Net debt (₹ cr)", f"{cur.net_debt:,.0f}", f"{cur.net_debt - 610:+,.0f} since Mar-26", delta_color="inverse")
    st.info("**What investors will see:** revenue is growing in line with guidance, but margins, cash flow and net debt "
            "have moved the wrong way, and several earlier management promises are now broken.")

    left, right = st.columns(2)
    fig = go.Figure()
    fig.add_bar(x=q.quarter, y=q.revenue, name="Revenue (₹ cr)", marker_color="#9FB3D1")
    fig.add_scatter(x=q.quarter, y=q.margin, name="EBITDA margin %", yaxis="y2", mode="lines+markers+text",
                    text=[f"{v:.1f}%" for v in q.margin], textposition="top center", line=dict(color=NAVY, width=3))
    fig.update_layout(title="Revenue up, margin down", height=340, legend=dict(orientation="h", y=-0.15),
                      yaxis2=dict(overlaying="y", side="right", range=[12, 18], dtick=1, ticksuffix="%", showgrid=False))
    left.plotly_chart(fig, width="stretch")
    fig = go.Figure(go.Bar(x=q.quarter, y=q.fcf, text=q.fcf, textposition="outside",
                           marker_color=["#D64545" if v < 0 else "#3A9D5D" for v in q.fcf]))
    fig.update_layout(title="Free cash flow (₹ cr) has turned negative", height=340, yaxis=dict(range=[-150, 280]))
    right.plotly_chart(fig, width="stretch")

    left, right = st.columns([1.35, 1])
    s = pd.DataFrame(D.SEGMENTS)
    left.markdown("**Segment performance (Q2 FY27 vs Q2 FY26)**")
    left.dataframe(pd.DataFrame({
        "Segment": s.segment, "Revenue (₹ cr)": s.rev_q2fy27,
        "YoY growth": [f"{(a / b - 1) * 100:+.1f}%" for a, b in zip(s.rev_q2fy27, s.rev_q2fy26)],
        "EBIT margin": [f"{m:.1f}%" for m in s.margin_q2fy27],
        "Δ margin": [f"{(a - b) * 100:+.0f} bps" for a, b in zip(s.margin_q2fy27, s.margin_q2fy26)]}),
        hide_index=True, width="stretch")
    left.caption("Digital: fast growth, margins diluted · Industrial: steady · Consumer: shrinking, near break-even")
    fig = go.Figure(go.Waterfall(
        x=[b[0] for b in D.MARGIN_BRIDGE], y=[b[1] for b in D.MARGIN_BRIDGE], measure=[b[2] for b in D.MARGIN_BRIDGE],
        text=[f"{b[1]:.1f}%" if b[2] != "relative" else f"{b[1] * 100:.0f} bps" for b in D.MARGIN_BRIDGE],
        textposition="outside", decreasing=dict(marker_color="#D64545"), totals=dict(marker_color=NAVY)))
    fig.update_layout(title="EBITDA margin bridge (YoY)", height=320, yaxis=dict(range=[12, 17.5]))
    right.plotly_chart(fig, width="stretch")

with tabs[1]:
    st.subheader("Where results break earlier promises")
    st.caption("Risk = gap severity (0–5) × investor sensitivity (1–5). Red ≥ 15 · Amber 7–15 · Green < 7")
    c = st.columns(3)
    c[0].metric("Promises tracked", len(gaps))
    c[1].metric("Missed", sum(g["status"] == "Missed" for g in gaps))
    c[2].metric("High-risk (red) topics", sum(g["rag"] == "Red" for g in gaps))

    def fmt(g):
        a = g["actual"]
        if g["unit"] == "₹ cr":
            return f"-₹{-a:,g} cr" if a < 0 else f"₹{a:,g} cr"
        return f"{a:g}%" if g["unit"] == "%" else f"{a:g} {g['unit']}"

    table = pd.DataFrame([{"Topic": g["topic"], "Earlier promise": g["commitment"], "Said in": g["source"],
                           "Actual": fmt(g), "Severity": g["severity"], "Sens.": g["sensitivity"],
                           "Risk": g["risk"], "RAG": g["rag"]} for g in gaps])
    st.dataframe(table.style.map(lambda v: f"background-color:{RAG[v]};color:white;font-weight:600" if v in RAG else "",
                                 subset=["RAG"]).format({"Risk": "{:.1f}", "Severity": "{:.1f}"}),
                 hide_index=True, width="stretch", height=370)
    left, right = st.columns([1.3, 1])
    rg = gaps[::-1]
    fig = go.Figure(go.Bar(y=[g["topic"] for g in rg], x=[g["risk"] for g in rg], orientation="h",
                           marker_color=[RAG[g["rag"]] for g in rg], text=[g["risk"] for g in rg], textposition="outside"))
    fig.update_layout(title="Risk score by topic (max 25)", height=330, xaxis=dict(range=[0, 30]))
    left.plotly_chart(fig, width="stretch")
    right.markdown("**What management said before**")
    for i, call, who, quote in D.TRANSCRIPTS:
        right.markdown(f"<div class='muted'><b>[{i}] {who}, {call}:</b> “{quote}”</div>", unsafe_allow_html=True)

# app.py — Part C: Likely questions and Practise tabs
with tabs[2]:
    st.subheader("The questions investors are most likely to ask")
    st.caption("Ranked by the risk of the broken promise behind each question.")
    for qq in all_questions():
        g = gap_by_id[qq["gap"]]
        with st.expander(f"{qq['id']} · [{g['rag']}] {qq['question'][:110]}…"):
            st.markdown(pill(f"{g['rag']} risk {g['risk']}", RAG[g["rag"]]) + pill("Owner: " + g["owner"], NAVY),
                        unsafe_allow_html=True)
            st.markdown(f"**Asked by:** {qq['persona']}\n\n> {qq['question']}\n\n**Why they'll ask:** {qq['why']}\n\n"
                        f"**Facts to anchor on:** {g['key_fact']}")
    st.divider()
    if st.button("✨ Generate 5 new questions with Gemini", disabled=not llm.ok):
        with st.spinner("Thinking like a sell-side analyst…"):
            ss.ai_questions = llm.new_questions(gaps) or []
        if not ss.ai_questions:
            st.error(f"Gemini call failed: {llm.error}")
    for i, aq in enumerate(ss.ai_questions):
        st.markdown(f"**{aq.get('persona', 'Analyst')}** · {aq.get('question', '')}  \n_{aq.get('why', '')}_")
        if st.button("Add to practice list", key=f"add{i}"):
            text = (aq.get("topic", "") + " " + aq.get("question", "")).lower()
            gid = next((gid for words, gid in [(("cash", "fcf"), "fcf"), (("receivable", "working capital"), "receivables"),
                        (("consumer", "oem"), "consumer"), (("debt", "dividend"), "debt"), (("capex",), "capex"),
                        (("digital",), "digital")] if any(w in text for w in words)), "margin")
            ss.extra_questions.append(dict(id=f"AI{len(ss.extra_questions) + 1}", gap=gid, persona=aq.get("persona", "Analyst"),
                                           question=aq.get("question", ""), why=aq.get("why", ""),
                                           keywords=[gid, "guidance"], model_answer="", follow_up=""))
            st.success("Added. Pick it in the Practise tab.")

with tabs[3]:
    st.subheader("Practise an answer and get scored")
    options = all_questions()
    qid = st.selectbox("Pick a question (highest risk first)", [x["id"] for x in options],
                       format_func=lambda i: next(f"{i} · [{gap_by_id[x['gap']]['rag']}] {x['question'][:90]}…"
                                                  for x in options if x["id"] == i))
    qq = next(x for x in options if x["id"] == qid)
    g = gap_by_id[qq["gap"]]
    st.markdown(f'<div class="qcard"><div class="muted">🎤 {qq["persona"]} asks:</div>'
                f'<div style="font-size:1.12rem;margin-top:4px">“{qq["question"]}”</div></div>', unsafe_allow_html=True)
    st.caption(f"Owner: {g['owner']} · Promise at risk: {g['commitment']} · Facts to use: {g['key_fact']}")

    b = st.columns([1.5, 1.5, 0.8, 2.2])
    if b[0].button("Demo: weak answer"):
        ss.answer = D.DEMO_ANSWERS["weak"]
    if b[1].button("Demo: average answer"):
        ss.answer = D.DEMO_ANSWERS["average"]
    if b[2].button("Clear"):
        ss.answer = ""
    answer = st.text_area("Your answer (as you would say it on the call)", key="answer", height=150)

    if st.button("🎯 Score my answer", type="primary", disabled=not answer.strip()):
        rules = E.rule_check(answer, qq)
        ai = None
        if llm.ok:
            with st.spinner("Gemini is checking the answer against the disclosure pack…"):
                ai = llm.score_answer(qq, g, answer)
        if ai and "scores" in ai:
            scores, engine = E.apply_guardrails(ai["scores"], rules), f"Gemini ({llm.model}) + guardrails"
        else:
            scores, engine = rules["scores"], "Rule-based guardrails (offline)"
            if llm.ok:
                st.warning(f"Gemini unavailable, used rules only. {llm.error}")
        total = E.overall(scores)
        ss.result = dict(qid=qid, scores=scores, overall=total, rules=rules, ai=ai, engine=engine)
        ss.history.append(dict(qid=qid, gap=qq["gap"], overall=total, engine=engine, time=datetime.now().strftime("%H:%M")))

    res = ss.result
    if res and res["qid"] == qid:
        st.divider()
        left, right = st.columns([1, 2])
        col = score_color(res["overall"])
        verdict = "Call-ready" if res["overall"] >= 75 else "Needs work" if res["overall"] >= 55 else "Not ready"
        left.markdown(f'<div class="card"><div class="muted">Answer score</div><div class="big" style="color:{col}">'
                      f'{res["overall"]}</div><div class="muted">out of 100</div>{pill(verdict, col)}</div>',
                      unsafe_allow_html=True)
        left.caption(f"Scored by: {res['engine']}")
        for k, label in E.LABELS.items():
            right.markdown(f"{label} ({E.WEIGHTS[k]}%): **{res['scores'][k]:.1f}/10**")
            right.progress(min(1.0, res["scores"][k] / 10))

        left, right = st.columns(2)
        left.markdown("**🛡️ Disclosure guardrails** (rule-based, always on)")
        for level, msg in res["rules"]["flags"]:
            left.markdown({"error": "🔴 ", "warn": "🟠 ", "ok": "🟢 "}[level] + msg)
        ai = res["ai"] or {}
        right.markdown("**🤖 Coach feedback (Gemini)**")
        if not ai:
            right.caption("Connect Gemini for qualitative feedback. The guardrails still apply.")
        for s_ in ai.get("strengths", [])[:3]:
            right.markdown(f"✅ {s_}")
        for s_ in ai.get("issues", [])[:4]:
            right.markdown(f"⚠️ {s_}")

        better = ai.get("improved_answer") or qq.get("model_answer")
        if better:
            st.markdown("**✍️ Stronger answer (uses only disclosed facts)**")
            st.success(better)
        follow = ai.get("follow_up") or qq.get("follow_up")
        if follow:
            st.markdown(f"**🔁 Expect this follow-up:** _{follow}_")
            if st.button("Practise this follow-up next"):
                ss.extra_questions.append(dict(id=f"FU{len(ss.extra_questions) + 1}", gap=qq["gap"],
                                               persona=qq["persona"] + " (follow-up)", question=follow,
                                               why=f"Follow-up to {qid}.", keywords=qq["keywords"],
                                               model_answer="", follow_up=""))
                st.success("Added to the practice list.")

# app.py — Part D: Readiness and Data tabs
with tabs[4]:
    st.subheader("Is leadership ready for the call?")
    index, verdict, rows = E.readiness(gaps, ss.history)
    col = score_color(index)
    left, right = st.columns([1, 2.2])
    left.markdown(f'<div class="card"><div class="muted">Readiness index</div><div class="big" style="color:{col}">'
                  f'{index}</div><div class="muted">risk-weighted, out of 100</div>{pill(verdict, col)}</div>',
                  unsafe_allow_html=True)
    left.caption(f"Based on {len(ss.history)} rehearsal attempt(s). Unrehearsed topics count as 0.")
    if not ss.history:
        left.info("No rehearsals yet. Practise in tab ④ or click **Load sample rehearsal round** in the sidebar.")
    r = pd.DataFrame(rows)
    r["Risk"] = r["Risk"].map(lambda v: f"{v:.1f}")
    r["Best score"] = r["Best score"].map(lambda v: "–" if pd.isna(v) else f"{v:.0f}")
    state_color = {"Ready": "#3A9D5D", "Needs work": "#E8A33D", "Not ready": "#D64545", "Not rehearsed": "#888"}
    right.dataframe(r.style.map(lambda v: f"background-color:{RAG[v]};color:white" if v in RAG else "", subset=["RAG"])
                    .map(lambda v: f"color:{state_color.get(v, '')};font-weight:600", subset=["Readiness"]),
                    hide_index=True, width="stretch", height=360)

    st.markdown("### 📋 Recommendation to leadership")
    for i, (title, body) in enumerate(E.recommendations(gaps, ss.history), 1):
        st.markdown(f"**{i}. {title}.** {body}")
    st.download_button("⬇️ Download Q&A briefing pack (.md)", E.briefing_pack(gaps, ss.history),
                       file_name="qa_briefing_pack.md")

with tabs[5]:
    st.subheader("Inputs and assumptions")
    for a in D.ASSUMPTIONS:
        st.markdown(f"- {a}")
    left, right = st.columns(2)
    left.markdown("**Approved Q2 FY27 disclosure pack (source of truth)**")
    for d in D.DISCLOSURES:
        left.markdown(f"- {d}")
    right.markdown("**Earlier promises (previous call transcripts)**")
    for i, call, who, quote in D.TRANSCRIPTS:
        right.markdown(f"- **[{i}] {who}, {call}:** “{quote}”")
    st.markdown("**Quarterly financials (₹ crore)**")
    st.dataframe(q.round(1), hide_index=True, width="stretch")
    st.markdown("**Segments**")
    st.dataframe(pd.DataFrame(D.SEGMENTS), hide_index=True, width="stretch")
