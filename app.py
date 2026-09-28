import streamlit as st
from agent import recall_incidents, analyze_incident, save_incident_resolution, hindsight, BANK_ID

st.set_page_config(page_title="Incident Response Agent", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.mono { font-family: 'JetBrains Mono', monospace; }
.stApp { background: radial-gradient(circle at 15% 0%, #0d1b2a 0%, #05070a 45%, #05070a 100%); }
.main .block-container {padding-top: 1.5rem; max-width: 1200px;}
.hero { display:flex; align-items:center; justify-content:space-between; padding: 22px 28px; border-radius: 16px; margin-bottom: 22px; background: linear-gradient(135deg, rgba(0,255,180,0.06), rgba(0,120,255,0.05)); border: 1px solid rgba(0,255,180,0.18); box-shadow: 0 0 40px rgba(0,255,180,0.05), inset 0 0 60px rgba(0,255,180,0.02); }
.hero-title { font-size: 1.85rem; font-weight: 800; color: #eafff5; letter-spacing: 0.5px; margin:0; }
.hero-title span { color: #00ffb3; text-shadow: 0 0 18px rgba(0,255,179,0.5); }
.hero-sub { color:#7d94a3; font-size:0.92rem; margin-top:4px; }
.pulse-dot { height:9px; width:9px; border-radius:50%; display:inline-block; margin-right:8px; box-shadow: 0 0 10px currentColor; animation: pulse 1.6s infinite; }
.dot-ok { background:#00ffb3; color:#00ffb3; }
.dot-fail { background:#ff4d6d; color:#ff4d6d; }
@keyframes pulse { 0%{opacity:1;} 50%{opacity:0.35;} 100%{opacity:1;} }
.status-pill { font-family:'JetBrains Mono', monospace; font-size:0.78rem; font-weight:600; padding:7px 16px; border-radius:999px; letter-spacing:0.5px; background: rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08); }
.stat-row {display:flex; gap:14px; margin-bottom:22px;}
.stat-card { flex:1; background: rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:16px 20px; }
.stat-label { font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:#5d7285; text-transform:uppercase; letter-spacing:1px; }
.stat-value { font-family:'JetBrains Mono', monospace; font-size:1.6rem; font-weight:700; color:#eafff5; margin-top:2px; }
.section-label { font-family:'JetBrains Mono', monospace; font-size:0.78rem; font-weight:700; color:#00ffb3; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px; display:flex; align-items:center; gap:8px; }
.section-label::before { content:''; width:18px; height:2px; background:#00ffb3; box-shadow: 0 0 8px #00ffb3; }
.badge-wrap { margin: 6px 0 20px 0; }
.badge-reuse { display:inline-flex; align-items:center; gap:10px; background: linear-gradient(135deg, rgba(0,255,179,0.14), rgba(0,255,179,0.04)); border: 1px solid rgba(0,255,179,0.45); color:#baffe8; padding:12px 24px; border-radius:12px; font-size:1.05rem; font-weight:700; box-shadow: 0 0 30px rgba(0,255,179,0.12); font-family:'JetBrains Mono', monospace; }
.badge-new { display:inline-flex; align-items:center; gap:10px; background: linear-gradient(135deg, rgba(255,176,0,0.14), rgba(255,176,0,0.04)); border: 1px solid rgba(255,176,0,0.45); color:#ffe0a3; padding:12px 24px; border-radius:12px; font-size:1.05rem; font-weight:700; box-shadow: 0 0 30px rgba(255,176,0,0.12); font-family:'JetBrains Mono', monospace; }
.solution-card { background: rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.09); border-left: 3px solid #00ffb3; border-radius:12px; padding:22px 24px; margin-bottom:20px; }
.field-label { font-family:'JetBrains Mono', monospace; font-size:0.7rem; font-weight:700; color:#5d7285; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:5px; }
.field-value { color:#dbe7ee; line-height:1.6; font-size:0.97rem; margin-bottom:18px; }
.reason-note { color:#5d7285; font-size:0.85rem; font-style:italic; border-top:1px solid rgba(255,255,255,0.07); padding-top:12px; margin-top:4px; }
.memory-count { color:#7d94a3; font-family:'JetBrains Mono', monospace; font-size:0.85rem; margin-bottom:12px; }
.memory-empty { background: rgba(255,255,255,0.02); border:1px dashed rgba(255,255,255,0.15); border-radius:10px; padding:18px 20px; color:#5d7285; font-family:'JetBrains Mono', monospace; font-size:0.88rem; text-align:center; }
.warn-box { background: linear-gradient(135deg, rgba(255,176,0,0.1), rgba(255,176,0,0.02)); border:1px solid rgba(255,176,0,0.35); border-radius:10px; padding:14px 18px; color:#ffe0a3; margin-bottom:14px; font-size:0.9rem; }
.reuse-note { background: linear-gradient(135deg, rgba(0,255,179,0.08), rgba(0,255,179,0.02)); border:1px solid rgba(0,255,179,0.3); border-radius:10px; padding:14px 18px; color:#a8d4f0; font-size:0.9rem; }
.stButton>button { border-radius:10px !important; font-weight:600 !important; }
.stButton>button[kind="primary"] { background: linear-gradient(135deg, #00ffb3, #00b386) !important; color:#04140e !important; border:none !important; box-shadow: 0 0 24px rgba(0,255,179,0.25) !important; }
section[data-testid="stSidebar"] { background: rgba(5,10,14,0.6); border-right:1px solid rgba(255,255,255,0.06); }
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
if "current_alert" not in st.session_state:
    st.session_state.current_alert = ""
if "saved" not in st.session_state:
    st.session_state.saved = False

try:
    hindsight.recall(bank_id=BANK_ID, query="ping")
    hs_ok = True
except Exception:
    hs_ok = False

st.markdown(f"""
<div class="hero">
<div>
<div class="hero-title">🛡️ <span>INCIDENT RESPONSE</span> AGENT</div>
<div class="hero-sub">Memory-driven triage · Hindsight recall · Human-verified learning loop</div>
</div>
<div>
<span class="status-pill"><span class="pulse-dot {'dot-ok' if hs_ok else 'dot-fail'}"></span>{'HINDSIGHT ONLINE' if hs_ok else 'HINDSIGHT OFFLINE'}</span>
</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
mode_display = st.session_state.result["analysis"]["mode"] if st.session_state.result else "—"
mem_display = len(st.session_state.result["memories"]) if st.session_state.result else "—"
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-label">Memory Bank</div><div class="stat-value">{BANK_ID}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="stat-card"><div class="stat-label">Last Decision</div><div class="stat-value">{mode_display}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-label">Memories Recalled</div><div class="stat-value">{mem_display}</div></div>', unsafe_allow_html=True)

st.write("")

with st.sidebar:
    st.markdown('<div class="section-label">📚 MEMORY BANK</div>', unsafe_allow_html=True)
    if st.button("🔄 Refresh stored incidents", use_container_width=True):
        try:
            with st.spinner("Querying Hindsight..."):
                browse = hindsight.recall(bank_id=BANK_ID, query="incident")
                st.session_state.browse_results = browse.results[:20]
        except Exception as e:
            st.error(f"Couldn't load memory: {e}")
    if "browse_results" in st.session_state:
        st.caption(f"{len(st.session_state.browse_results)} memories · showing top 20")
        for m in st.session_state.browse_results:
            with st.expander(m.text[:60] + "..."):
                st.caption(m.text)
    else:
        st.caption("Click refresh to load stored incidents.")

st.markdown('<div class="section-label">🔍 NEW ALERT</div>', unsafe_allow_html=True)

examples = {
    "🆕 Novel · USB device": "Employee laptop reported unauthorized USB device connected",
    "🔁 Repeat · SSH brute-force": "Hundreds of failed SSH login attempts from one external IP",
    "🔁 Repeat · DB timeout": "Database connection timeouts on the payments API",
}
ex_cols = st.columns(len(examples))
for i, (label, text) in enumerate(examples.items()):
    if ex_cols[i].button(label, use_container_width=True):
        st.session_state.current_alert = text

alert = st.text_area("Alert input", value=st.session_state.current_alert, height=90,
                      placeholder="Paste or type the incoming alert / symptom...", label_visibility="collapsed")

if st.button("▶  ANALYZE ALERT", type="primary", use_container_width=True):
    if not alert.strip():
        st.warning("Enter an alert first.")
    else:
        try:
            with st.spinner("🔎 Querying Hindsight memory..."):
                memories = recall_incidents(alert)
            with st.spinner("🧠 Running LLM analysis..."):
                analysis = analyze_incident(alert, memories)
            st.session_state.result = {"alert": alert, "memories": memories, "analysis": analysis}
            st.session_state.current_alert = alert
            st.session_state.saved = False
            st.rerun()
        except Exception as e:
            st.error(f"Something went wrong: {e}")

if st.session_state.result:
    r = st.session_state.result
    analysis = r["analysis"]
    memories = r["memories"]
    mode = analysis.get("mode", "NEW")
    is_reuse = mode == "REUSE"

    st.write("")
    badge_class = "badge-reuse" if is_reuse else "badge-new"
    badge_text = "✅  REUSED FROM MEMORY" if is_reuse else "🆕  NEW — NO MATCH FOUND"
    st.markdown(f'<div class="badge-wrap"><div class="{badge_class}">{badge_text}</div></div>', unsafe_allow_html=True)

    st.markdown(f"""
<div class="solution-card">
<div class="field-label">Root Cause</div>
<div class="field-value">{analysis.get("root_cause","")}</div>
<div class="field-label">Recommended Solution</div>
<div class="field-value">{analysis.get("solution","")}</div>
<div class="reason-note">💭 {analysis.get("reason","")}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="section-label">📋 MEMORIES RECALLED</div>', unsafe_allow_html=True)
    if memories:
        st.markdown(f'<div class="memory-count">{len(memories)} memories retrieved from bank "{BANK_ID}"</div>', unsafe_allow_html=True)
        for i, mem in enumerate(memories, start=1):
            with st.expander(f"◦ Memory {i:02d}"):
                st.markdown(f'<div class="mono" style="font-size:0.88rem; color:#c8d6de;">{mem}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="memory-empty">— NO RELATED MEMORIES FOUND —<br>This incident is entirely new to the agent.</div>', unsafe_allow_html=True)

    st.write("")

    if is_reuse:
        st.markdown('<div class="reuse-note">✅ This solution was already verified previously — nothing new to save.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warn-box">⚠️ This is a newly generated solution — review it carefully before it becomes permanent knowledge in the memory bank.</div>', unsafe_allow_html=True)
        approved = st.checkbox("I have reviewed and verified this solution works")

        if st.session_state.saved:
            st.success("✅ Saved to memory. Try a similar alert now to see it get reused.")
        else:
            if st.button("💾  SAVE RESOLUTION TO MEMORY", disabled=not approved, use_container_width=True):
                try:
                    save_incident_resolution(
                        alert=r["alert"],
                        root_cause=analysis.get("root_cause", ""),
                        solution=analysis.get("solution", ""),
                        source="LLM generated and user verified",
                    )
                    st.session_state.saved = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Couldn't save: {e}")