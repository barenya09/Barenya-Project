# data.py — every input the app uses. All figures are synthetic, in ₹ crore.
COMPANY_NAME = "Barenya Pvt. Ltd."

COMPANY = {
    "name": COMPANY_NAME,
    "ticker": "NSE: BARENYA (fictional)",
    "description": ("Fictional NSE-listed mid-cap with three segments: Digital Solutions (IT services), "
                    "Industrial Automation (machinery and controls) and Consumer Electronics Components "
                    "(parts for phone and appliance makers)."),
    "quarter": "Q2 FY27 (Jul–Sep 2026)",
    "call_date": "October 2026",
}

# Six quarters of results. FCF = operating cash flow (cfo) − capex.
QUARTERLY = {
    "quarter":         ["Q1 FY26", "Q2 FY26", "Q3 FY26", "Q4 FY26", "Q1 FY27", "Q2 FY27"],
    "revenue":         [2360, 2450, 2520, 2610, 2640, 2793],
    "ebitda":          [396,  404,  408,  412,  396,  388],
    "pat":             [238,  246,  244,  241,  205,  189],
    "cfo":             [380,  330,  310,  300,  190,  85],
    "capex":           [150,  120,  130,  150,  160,  175],
    "net_debt":        [None, None, None, 610,  700,  840],
    "receivable_days": [60,   62,   63,   64,   72,   78],
}

# Segment revenue (₹ cr) and EBIT margin (%): same quarter last year, last quarter, this quarter
SEGMENTS = {
    "segment":       ["Digital Solutions", "Industrial Automation", "Consumer Electronics Components"],
    "rev_q2fy26":    [900,  1000, 550],
    "rev_q1fy27":    [1090, 1040, 510],
    "rev_q2fy27":    [1188, 1099, 506],
    "margin_q2fy26": [14.0, 15.5, 9.0],
    "margin_q1fy27": [10.5, 15.4, 4.5],
    "margin_q2fy27": [8.5,  15.1, 2.0],
}

# Why EBITDA margin fell from 16.5% to 13.9% (in basis points)
MARGIN_BRIDGE = [
    ("Q2 FY26 margin", 16.5, "absolute"),
    ("Digital deal transition costs", -1.2, "relative"),
    ("Consumer under-utilisation", -1.0, "relative"),
    ("Industrial input costs", -0.4, "relative"),
    ("Q2 FY27 margin", 13.9, "total"),
]

# What management said on earlier calls (investors WILL compare against these)
TRANSCRIPTS = [
    ("T1", "Q4 FY26 call (May 2026)", "CEO", "We are confident FY27 will be a year of margin expansion. We expect EBITDA margins to improve by 50 to 100 basis points from FY26's 16.3% as our pricing actions flow through."),
    ("T2", "Q4 FY26 call (May 2026)", "CFO", "Free cash flow remains a priority. We expect to be FCF positive in every quarter of FY27 and to deliver over ₹600 crore of free cash flow for the year."),
    ("T3", "Q4 FY26 call (May 2026)", "CEO", "Consumer has bottomed out. With two new OEM wins, we expect the segment to return to growth by Q2."),
    ("T4", "Q4 FY26 call (May 2026)", "CFO", "We will keep net debt below ₹700 crore. FY27 capex will be ₹550 to 600 crore, and revenue growth 12 to 14%."),
    ("T5", "Q4 FY26 call (May 2026)", "Head of Digital", "Digital Solutions should grow 25% plus at mid-teens EBIT margins of 14 to 16%."),
    ("T6", "Q1 FY27 call (Aug 2026)", "CFO", "The Q1 margin dip is temporary and linked to the annual wage hike. We remain comfortable with our full-year margin guidance."),
    ("T7", "Q1 FY27 call (Aug 2026)", "CFO", "Working capital was seasonally higher. We expect receivable days to normalise back to around 62 in Q2."),
    ("T8", "Q1 FY27 call (Aug 2026)", "CEO", "Digital is winning large deals. Some carry upfront transition costs, but they will be margin-accretive by H2."),
]

# The approved Q2 FY27 disclosure pack = the ONLY facts leadership may state on the call
DISCLOSURES = [
    "Q2 FY27 revenue grew 14.0% YoY to ₹2,793 crore; H1 FY27 revenue grew 13.0% to ₹5,433 crore.",
    "Q2 FY27 EBITDA was ₹388 crore; EBITDA margin 13.9%, down 260 bps YoY from 16.5%. H1 FY27 EBITDA margin was 14.4%.",
    "Margin bridge: about 120 bps from transition costs on three large Digital deals, about 100 bps from Consumer under-utilisation, about 40 bps from Industrial input costs not yet passed through.",
    "PAT was ₹189 crore, down 23% YoY from ₹246 crore, also reflecting higher depreciation (₹85 crore) and finance cost (₹38 crore).",
    "Digital Solutions revenue grew 32% to ₹1,188 crore; EBIT margin 8.5% vs 14.0%. Transition costs end by Q4 FY27; Digital margin expected at 12–13% by Q4. Mid-teens remains the medium-term ambition (no timeline). Large deals expected to be margin-accretive over contract life.",
    "Industrial Automation revenue grew 9.9% to ₹1,099 crore; EBIT margin 15.1% vs 15.5%. Renegotiating input-cost pass-through clauses with key customers.",
    "Consumer Electronics Components revenue fell 8.0% to ₹506 crore; EBIT margin 2.0%. First OEM programme began supplies in Q2 at low volumes; the second was delayed by the customer's launch postponement and is now expected to start in Q4 FY27.",
    "Operating cash flow ₹85 crore; capex ₹175 crore; free cash flow negative ₹90 crore. H1 FY27 FCF negative ₹60 crore.",
    "Receivable days rose to 78 (62 a year ago) due to milestone-based billing on large Digital contracts. Standard credit terms unchanged. About ₹180 crore of milestone billing is due in Q3.",
    "Net debt ₹840 crore (₹610 crore in March 2026), about 0.52x TTM EBITDA. Expected to peak around ₹850 crore and return below ₹700 crore by March 2027.",
    "H1 capex of ₹335 crore was front-loaded for a new automation line at the Industrial plant. FY27 capex plan trimmed to ₹500–550 crore (H2 capex ₹165–215 crore).",
    "Project Sankalp cost programme: ₹90 crore annualised savings, full run-rate from Q4 FY27.",
    "Revised FY27 outlook: revenue growth 12–14% retained; EBITDA margin revised to 14.5–15.5% (from 16.8–17.3%); FCF positive in H2 with FY27 FCF of ₹150–250 crore. Progress reported every quarter.",
    "Dividend policy (30% payout) unchanged.",
]
# Other numbers it is fine to say (derived figures, e.g. TTM EBITDA, H1 capex run-rate)
EXTRA_ALLOWED_NUMBERS = [0.52, 12.95, 14.43, 16.3, 16.8, 17.3, 1604, 4810, 670, 170, 230, 850, 60]

# ---------- Part B: commitments vs actuals, questions, assumptions ----------
# For each earlier promise: the committed range (low/high), the actual, which direction is good,
# a "scale" (how big a miss counts as maximum severity) and investor sensitivity (1–5).
GAPS = [
    dict(id="margin", topic="EBITDA margin vs guidance", commitment="FY27 EBITDA margin up 50–100 bps to 16.8–17.3%", source="T1, T6",
         actual=14.43, low=16.8, high=17.3, good="higher", unit="%", scale=2.0, sensitivity=5, owner="CFO",
         key_fact="Revised margin outlook 14.5–15.5%; 260 bps bridge (120 Digital / 100 Consumer / 40 Industrial)"),
    dict(id="fcf", topic="Free cash flow", commitment="FCF positive every quarter; FY27 FCF > ₹600 cr", source="T2",
         actual=-90, low=0, high=None, good="higher", unit="₹ cr", scale=100, sensitivity=5, owner="CFO",
         key_fact="FCF positive in H2; FY27 FCF ₹150–250 cr; ₹180 cr milestone billing due in Q3"),
    dict(id="digital", topic="Digital segment margin", commitment="Digital EBIT margin 14–16%", source="T5, T8",
         actual=8.5, low=14, high=16, good="higher", unit="%", scale=4, sensitivity=4, owner="Head of Digital",
         key_fact="Transition costs end by Q4; Digital margin 12–13% by Q4"),
    dict(id="receivables", topic="Working capital / receivables", commitment="Receivable days back to ~62 in Q2", source="T7",
         actual=78, low=None, high=62, good="lower", unit="days", scale=20, sensitivity=3, owner="CFO",
         key_fact="Milestone billing on Digital deals; credit terms unchanged; ₹180 cr due in Q3"),
    dict(id="consumer", topic="Consumer segment turnaround", commitment="Consumer back to YoY growth by Q2", source="T3",
         actual=-8.0, low=0, high=None, good="higher", unit="%", scale=10, sensitivity=3, owner="CEO",
         key_fact="First OEM programme live; second delayed to Q4 FY27 (customer launch postponed)"),
    dict(id="debt", topic="Net debt and balance sheet", commitment="Net debt below ₹700 cr", source="T4",
         actual=840, low=None, high=700, good="lower", unit="₹ cr", scale=200, sensitivity=3, owner="CFO",
         key_fact="0.52x net debt/EBITDA; peak ~₹850 cr; below ₹700 cr by Mar-27; dividend policy unchanged"),
    dict(id="capex", topic="Capex run-rate", commitment="FY27 capex ₹550–600 cr", source="T4",
         actual=670, low=None, high=600, good="lower", unit="₹ cr", scale=150, sensitivity=2, owner="CFO",
         key_fact="H1 front-loaded (₹335 cr); FY27 plan trimmed to ₹500–550 cr"),
    dict(id="revenue", topic="Revenue growth", commitment="FY27 revenue growth 12–14%", source="T4",
         actual=12.95, low=12, high=14, good="higher", unit="%", scale=4, sensitivity=3, owner="CEO",
         key_fact="H1 growth 13.0%, in line with guidance; Digital +32%, Industrial +9.9%"),
    dict(id="digital_growth", topic="Digital growth", commitment="Digital growth 25%+", source="T5",
         actual=32.0, low=25, high=None, good="higher", unit="%", scale=10, sensitivity=2, owner="Head of Digital",
         key_fact="Digital +32% YoY, ahead of the 25%+ target"),
]

# Old promises that the revised outlook replaces. If an answer repeats one AS IF STILL VALID, flag it.
SUPERSEDED = [
    ("Margin expansion of 50–100 bps / 16.8–17.3% margin", ["margin expansion", "50 to 100 basis points", "50–100 bps", "50-100 bps", "17%", "17.3", "16.8"]),
    ("FCF positive every quarter / FY27 FCF over ₹600 crore", ["positive every quarter", "positive in every quarter", "600 crore", "₹600"]),
    ("Consumer back to growth by Q2", ["bottomed out", "growth by q2"]),
    ("Margin dip is temporary / comfortable with full-year margin guidance", ["dip is temporary", "comfortable with our full-year", "maintain our margin guidance"]),
    ("Net debt will stay below ₹700 crore this year", ["stay below 700", "remain below 700", "never exceed"]),
    ("Capex of ₹550–600 crore", ["550 to 600", "550–600", "550-600"]),
]

QUESTIONS = [
    dict(id="Q1", gap="margin", persona="Sell-side analyst (domestic brokerage)",
         question="In May you guided to 50–100 bps of EBITDA margin expansion for FY27, and in August you said you were still comfortable with it. H1 margin is 14.4%, more than 200 bps below even the low end. Is the guidance withdrawn, and why should we trust the new number?",
         why="Compares results with two earlier statements (T1, T6). A credibility question.",
         keywords=["margin", "guidance", "bps", "revis"],
         model_answer="You're right. H1 margin of 14.4% is well below the 50–100 bps expansion we guided to in May, and today we are revising our FY27 EBITDA margin outlook to 14.5–15.5%. Three factors explain the 260 bps year-on-year decline in Q2: about 120 bps from transition costs on three large Digital deals, about 100 bps from under-utilisation in Consumer, and about 40 bps from Industrial input costs not yet passed through. The Digital transition costs end by Q4, and Project Sankalp should deliver ₹90 crore of annualised savings at full run-rate from Q4. We would rather reset now to a number we can deliver than defend the old one.",
         follow_up="If transition costs end in Q4, why isn't the revised range higher? What are you assuming for Consumer?"),
    dict(id="Q2", gap="margin", persona="Institutional investor (long-only fund)",
         question="Can you break down the 260 bps year-on-year margin decline? How much is one-off and how much is structural?",
         why="Investors need to know if margin pressure carries into next year's valuation.",
         keywords=["bps", "one-off", "structural", "transition", "consumer", "input"],
         model_answer="Of the 260 bps decline, about 120 bps comes from upfront transition costs on three large Digital deals. That is time-bound and ends by Q4, after which we expect Digital margins of 12–13%. About 100 bps is Consumer under-utilisation, which should reverse as the second OEM programme starts supplies in Q4. The 40 bps from Industrial input costs is the most structural piece, and we are renegotiating pass-through clauses with key customers. So most of the decline is temporary, but we are not assuming a full recovery this year, which is why the revised outlook is 14.5–15.5%.",
         follow_up="What happens to the 40 bps if customers refuse the new pass-through terms?"),
    dict(id="Q3", gap="fcf", persona="Credit analyst (bond investor)",
         question="You committed to positive free cash flow in every quarter of FY27. Q2 FCF is negative ₹90 crore and H1 is negative ₹60 crore. What went wrong, and when does cash turn?",
         why="A broken cash promise (T2) hits credibility and the credit view.",
         keywords=["cash", "fcf", "working capital", "billing", "h2"],
         model_answer="We did not meet our commitment of positive free cash flow every quarter. Q2 FCF was negative ₹90 crore. The main driver is working capital: our large Digital contracts are billed on milestones, so receivable days rose to 78, and about ₹180 crore of milestone billing falls due in Q3. Capex was also front-loaded at ₹335 crore in H1, and we have trimmed the full-year capex plan to ₹500–550 crore. We now expect FCF to turn positive in H2, with FY27 FCF of ₹150–250 crore, and net debt to return below ₹700 crore by March 2027.",
         follow_up="What happens to your FCF outlook if the ₹180 crore milestone billing slips into Q4?"),
    dict(id="Q4", gap="receivables", persona="Sell-side analyst (foreign brokerage)",
         question="Receivable days went from 62 to 78, even though you told us in Q1 they would normalise in Q2. Are you financing customers to buy revenue growth?",
         why="Hints at aggressive revenue recognition; contradicts T7.",
         keywords=["receivable", "days", "billing", "credit"],
         model_answer="That's a fair challenge. Receivable days rose from 62 to 78, more than the normalisation we indicated in Q1. This is not extended credit: our standard customer credit terms are unchanged. The increase comes from milestone-based billing on our large Digital contracts, where work is delivered ahead of the billing milestone. About ₹180 crore of milestone billing is due in Q3, which should bring receivables down meaningfully.",
         follow_up="Can you show unbilled revenue separately from trade receivables?"),
    dict(id="Q5", gap="digital", persona="Institutional investor (long-only fund)",
         question="Digital grew 32% but its EBIT margin almost halved to 8.5%. Are you buying large deals at the expense of profitability?",
         why="Growth vs profitability; contradicts the mid-teens margin promise (T5).",
         keywords=["digital", "margin", "deal", "transition"],
         model_answer="Digital revenue grew 32%, ahead of our 25%-plus target, but EBIT margin fell to 8.5% from 14.0%. That is mainly upfront transition costs on three large multi-year deals, which we absorb in the early quarters. These costs end by Q4, and we expect Digital margins to recover to 12–13% by then. Mid-teens remains our medium-term ambition, but we won't put a date on it today. These deals are expected to be margin-accretive over the life of the contracts.",
         follow_up="How many more large deals in the pipeline carry similar transition costs?"),
    dict(id="Q6", gap="consumer", persona="Sell-side analyst (domestic brokerage)",
         question="You said Consumer had bottomed out and would return to growth by Q2. It's down 8%. What happened to the two OEM wins?",
         why="Direct reversal of T3.",
         keywords=["consumer", "oem", "growth", "delay"],
         model_answer="We expected Consumer to return to growth by Q2, and it didn't: revenue was down 8%. Of the two OEM wins we discussed, the first began supplies this quarter at low volumes. The second was delayed because the customer postponed its product launch, and we now expect supplies to start in Q4 FY27. Under-utilisation in the meantime cost us about 100 bps of group margin this quarter.",
         follow_up="Is Consumer still a core business, or are you considering strategic options?"),
    dict(id="Q7", gap="debt", persona="Credit analyst (bond investor)",
         question="Net debt is ₹840 crore against your ₹700 crore ceiling. Is the balance sheet at risk, and is the dividend safe?",
         why="Breaks the T4 promise; dividend matters to income investors.",
         keywords=["net debt", "leverage", "dividend", "700"],
         model_answer="Net debt rose to ₹840 crore, above the ₹700 crore level we indicated, mainly because of the working-capital build and front-loaded capex. Leverage remains comfortable at about 0.52x net debt to trailing EBITDA. We expect net debt to peak around ₹850 crore and return below ₹700 crore by March 2027 as milestone billing converts to cash. Our dividend policy of a 30% payout is unchanged.",
         follow_up="What is the covenant headroom on your term loans?"),
    dict(id="Q8", gap="margin", persona="Activist-leaning shareholder",
         question="This is the second quarter in a row where management has called an issue temporary. Why should investors believe your revised guidance?",
         why="Attacks the pattern of misses (T6, T7, T8).",
         keywords=["guidance", "credib", "revised", "believe", "deliver"],
         model_answer="That's a fair concern, and it's why we are resetting guidance today rather than defending it. We were too optimistic about how quickly Digital transition costs and the Consumer OEM ramp would play out. The revised outlook, 14.5–15.5% EBITDA margin and ₹150–250 crore of FCF for FY27, is based on contracts already signed and cost actions already under way, including ₹90 crore of annualised savings from Project Sankalp. We will report progress against each of these every quarter.",
         follow_up="Will management pay be linked to delivering the revised outlook?"),
    dict(id="Q9", gap="revenue", persona="Sell-side analyst (foreign brokerage)",
         question="Revenue is tracking guidance, but how much of that growth is low-margin large deals? Are you sacrificing quality of revenue?",
         why="Even good news gets challenged; a chance to lead with strengths.",
         keywords=["revenue", "growth", "quality", "deal"],
         model_answer="H1 revenue grew 13.0%, within our 12–14% guidance, and Industrial grew 9.9% with margins broadly stable at 15.1%. In Digital, the three large deals do dilute margins in the early quarters because of transition costs, but they are multi-year contracts expected to be margin-accretive over their life. Once transition costs end in Q4, we expect Digital margins of 12–13%. So we are not chasing volume at any price; we are absorbing cost upfront on revenue that is contracted.",
         follow_up="What share of H2 revenue is already contracted?"),
    dict(id="Q10", gap="capex", persona="Institutional investor (long-only fund)",
         question="You've spent ₹335 crore of capex in H1 against a full-year guide of ₹550–600 crore. Will capex overshoot and make the cash position worse?",
         why="Links capex discipline to the cash miss.",
         keywords=["capex", "h2", "plan", "cash"],
         model_answer="H1 capex was ₹335 crore because spending on a new automation line at our Industrial plant was front-loaded. We have reviewed the H2 programme and trimmed FY27 capex to ₹500–550 crore, below the earlier plan, so H2 capex will be ₹165–215 crore. That supports our expectation of positive free cash flow in H2.",
         follow_up="Does trimming capex delay any growth projects?"),
]

DEMO_ANSWERS = {
    "weak": "Look, we remain very confident in our business. The margin dip is temporary and we will definitely get back to 17% margins by year end, no doubt about it. Our digital business is doing fantastic and we are winning everywhere. I don't think there is any need to worry.",
    "average": "Margins were lower this quarter mainly because of transition costs on some large Digital deals and weakness in Consumer. These are temporary and we expect margins to improve in the second half as these costs roll off. We are taking cost actions and we remain confident in the long-term margin profile of the business.",
}

ASSUMPTIONS = [
    f"{COMPANY_NAME} is fictional. All figures are synthetic, in ₹ crore, built to match the case: revenue up, margins down, cash weaker, segments mixed.",
    "The call being prepared is the Q2 FY27 call (Jul–Sep 2026 quarter) in October 2026. Earlier promises come from the Q4 FY26 call (May 2026) and Q1 FY27 call (Aug 2026).",
    "The Q2 disclosure pack is the board-approved source of truth. Any figure said on the call that is not in it is flagged as unverified.",
    "FCF = operating cash flow − capex. Net debt/EBITDA uses trailing-12-month EBITDA (₹1,604 crore). Net debt rose ₹230 crore in H1: −₹60 crore FCF plus a ~₹170 crore final dividend.",
    "Gap severity (0–5) = how far the actual is outside the promised range ÷ a metric-specific scale (e.g. 2 percentage points for margin, ₹100 crore for FCF), capped at 5.",
    "Investor sensitivity (1–5) is a judgement: margins and cash weighted highest, capex lowest.",
    "Risk = severity × sensitivity (0–25). Red ≥ 15, Amber 7–15, Green < 7.",
    "Answer score (0–100) = Accuracy 25% + Consistency 25% + Directness 20% + Forward-looking discipline 15% + Clarity 15%.",
    "Gemini judges answer quality; fixed rules (unverified numbers, repeated old promises, absolute promises, evasive phrases) cap the AI's score where they apply.",
    "Readiness index = risk-weighted average of each topic's best rehearsal score. Ready ≥ 75, Nearly ready 55–75, Not ready < 55. Unrehearsed topics count as 0.",
]
