import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Live Queue Waiting Time Predictor",
    page_icon="🚦",
    layout="centered"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.card {
    background:white;
    padding:18px;
    border-radius:12px;
    box-shadow:2px 2px 10px rgba(0,0,0,0.15);
    margin-bottom:15px;
}
.alert {
    background:#fff3cd;
    padding:10px;
    border-radius:8px;
    font-weight:bold;
}
.done {
    background:#d1e7dd;
    padding:12px;
    border-radius:8px;
    font-weight:bold;
}
.green {color:#2e7d32;}
.orange {color:#ff8f00;}
.red {color:#c62828;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DEFAULTS ----------------
defaults = {
    "page": 1,
    "queue": 20,
    "position": 6,
    "staff": 2,
    "service_time": 4,
    "arrival_rate": 1,
    "experience": "Average",
    "system": "Normal",
    "peak": False,
    "served": 0,
    "running": False,
    "completed": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- FUNCTIONS ----------------
def exp_factor(exp):
    return {"New": 0.8, "Average": 1.0, "Expert": 1.3}[exp]

def sys_factor(sys):
    return {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]

def predict_wait(queue):
    if queue <= 0:
        return 0
    base = (queue * st.session_state.service_time) / st.session_state.staff
    return round(
        base *
        exp_factor(st.session_state.experience) *
        sys_factor(st.session_state.system) *
        (1.3 if st.session_state.peak else 1.0),
        2
    )

def mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd", "green"
    elif wait <= 30:
        return "🟡 Medium Crowd", "orange"
    else:
        return "🔴 Heavy Crowd", "red"

# ---------------- PAGE 1 : INPUT ----------------
if st.session_state.page == 1:
    st.title("🚦 Smart Live Queue Waiting Time Predictor")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.session_state.queue = st.slider("👥 Total People in Queue", 1, 50, st.session_state.queue)
        st.session_state.position = st.slider(
            "🙋 Your Position in Queue",
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
        st.session_state.completed = False
        st.session_state.served = 0
        st.session_state.page = 2
        st.rerun()

# ---------------- PAGE 2 : LIVE QUEUE ----------------
elif st.session_state.page == 2:

    st.title("📊 Live Queue Status")

    box = st.empty()
    bar = st.progress(0)

    step = 0
    total = st.session_state.position + 1

    while st.session_state.running and st.session_state.position > 0:

        served_now = max(1, int(st.session_state.staff * exp_factor(st.session_state.experience)))
        st.session_state.queue = max(0, st.session_state.queue - served_now)
        st.session_state.position = max(0, st.session_state.position - served_now)
        st.session_state.served += served_now

        wait_time = predict_wait(st.session_state.position)
        mood_txt, color = mood(wait_time)

        now = datetime.now()
        finish_time = now + timedelta(minutes=wait_time)

        alert_msg = ""
        if st.session_state.position == 1:
            alert_msg = "⏰ Your turn is coming soon. Please be ready."

        box.markdown(f"""
        <div class="card">
        <h3>⏳ Waiting Time: {wait_time} minutes</h3>
        <h4 class="{color}">{mood_txt}</h4>

        👥 People in queue: <b>{st.session_state.queue}</b><br>
        🙋 Your position: <b>{st.session_state.position}</b><br>
        ✅ People served: <b>{st.session_state.served}</b><br><br>

        🕒 Current Time: <b>{now.strftime('%I:%M %p')}</b><br>
        ⏰ Expected Service Time: <b>{finish_time.strftime('%I:%M %p')}</b><br><br>

        {f'<div class="alert">{alert_msg}</div>' if alert_msg else ''}
        </div>
        """, unsafe_allow_html=True)

        step += 1
        bar.progress(min(100, int((step / total) * 100)))
        time.sleep(1.5)

    # ---- COMPLETED ----
    st.session_state.running = False
    st.session_state.completed = True

    box.markdown("""
    <div class="card done">
    ✅ <b>Your work is completed</b><br>
    Thank you for waiting.
    </div>
    """, unsafe_allow_html=True)

    bar.progress(100)

    if st.button("💡 Smart Suggestions"):
        st.session_state.page = 3
        st.rerun()

# ---------------- PAGE 3 : SMART SUGGESTIONS ----------------
elif st.session_state.page == 3:
    st.title("💡 Smart Suggestions & Best Time")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.write("### ❗ Delay Reasons")
        if st.session_state.queue > 20:
            st.write("👥 High number of people")
        if st.session_state.experience == "New":
            st.write("🎓 New or less experienced staff")
        if st.session_state.system != "Normal":
            st.write("🖥 System performance issue")
        if st.session_state.peak:
            st.write("🚨 Peak hour traffic")
        if st.session_state.arrival_rate > 1:
            st.write("📈 High arrival rate")

        st.markdown('</div>', unsafe_allow_html=True)

    best_time = "2:30 PM – 4:00 PM" if st.session_state.peak else "Any non-peak hour (Morning / Afternoon)"

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"""
        🕒 **Best Time to Visit:** {best_time}

        👨‍💼 **Suggestion:** Add one staff during peak hours  
        ⚡ **Suggestion:** Reduce service time using digital processing
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
