import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Live Queue Waiting Time Predictor",
    page_icon="🚦",
    layout="centered"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    margin-bottom: 15px;
}
.green {color:#2e7d32;}
.orange {color:#ff8f00;}
.red {color:#c62828;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DEFAULTS ----------------
defaults = {
    "queue": 15,
    "position": 5,
    "staff": 2,
    "service_time": 4,
    "arrival_rate": 1,
    "experience": "Average",
    "system": "Normal",
    "peak": False,
    "served": 0,
    "running": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- FUNCTIONS ----------------
def experience_factor(exp):
    return {"New": 0.8, "Average": 1.0, "Expert": 1.3}[exp]

def system_factor(sys):
    return {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]

def predict_wait(queue):
    base = (queue * st.session_state.service_time) / st.session_state.staff
    return round(
        base *
        experience_factor(st.session_state.experience) *
        system_factor(st.session_state.system) *
        (1.3 if st.session_state.peak else 1.0),
        2
    )

def queue_mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd", "green"
    elif wait <= 30:
        return "🟡 Medium Crowd", "orange"
    else:
        return "🔴 Heavy Crowd", "red"

# ---------------- INPUT PAGE ----------------
st.title("🚦 Live Queue Waiting Time Predictor")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.session_state.queue = st.slider("👥 Total People in Queue", 1, 50, st.session_state.queue)
    st.session_state.position = st.slider(
        "🙋 Your Position in Queue (Naa ethanavathu aala nikkuren)",
        1, st.session_state.queue, st.session_state.position
    )
    st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    st.session_state.service_time = st.slider("⏱ Service Time (minutes)", 1, 10, st.session_state.service_time)
    st.session_state.arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 3, st.session_state.arrival_rate)
    st.session_state.experience = st.selectbox("🎓 Staff Experience", ["New", "Average", "Expert"])
    st.session_state.system = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
    st.session_state.peak = st.checkbox("🚨 Peak Hour")

    st.markdown('</div>', unsafe_allow_html=True)

if st.button("▶️ Start Live Queue"):
    st.session_state.running = True
    st.session_state.served = 0

# ---------------- LIVE QUEUE ----------------
if st.session_state.running:

    box = st.empty()
    progress = st.progress(0)

    for i in range(30):

        served_now = int(st.session_state.staff * experience_factor(st.session_state.experience))
        arrived_now = st.session_state.arrival_rate

        st.session_state.queue = max(0, st.session_state.queue - served_now + arrived_now)
        st.session_state.position = max(0, st.session_state.position - served_now)
        st.session_state.served += served_now

        wait_time = predict_wait(st.session_state.position)
        mood, color = queue_mood(wait_time)

        delay_reasons = []
        if st.session_state.queue > 25:
            delay_reasons.append("👥 High crowd")
        if st.session_state.experience == "New":
            delay_reasons.append("🎓 New staff")
        if st.session_state.system != "Normal":
            delay_reasons.append("🖥 System issue")
        if st.session_state.peak:
            delay_reasons.append("🚨 Peak hour")
        if st.session_state.arrival_rate > 1:
            delay_reasons.append("📈 High arrival rate")

        box.markdown(f"""
        <div class="card">
        <h3>⏳ Live Waiting Time: {wait_time} mins</h3>
        <h4 class="{color}">{mood}</h4>

        👥 Queue la innum irukkura aal: <b>{st.session_state.queue}</b><br>
        🙋 Neenga nikkura position: <b>{st.session_state.position}</b><br>
        ✅ Serve pannina aal: <b>{st.session_state.served}</b><br><br>

        🗣 <b>Tamil Explanation:</b><br>
        "Neenga queue la {st.session_state.position}-avathu aala nikkuringa.
        Innum {st.session_state.position} per service mudiyanum.
        Approximate-ah {wait_time} nimisham wait pannanum."

        <br><br>
        ❗ <b>Delay Reasons:</b><br>
        {"<br>".join(delay_reasons) if delay_reasons else "No major delay"}
        </div>
        """, unsafe_allow_html=True)

        progress.progress((i + 1) * 3)
        time.sleep(1)

    st.success("✅ Live queue simulation completed")
    st.session_state.running = False
