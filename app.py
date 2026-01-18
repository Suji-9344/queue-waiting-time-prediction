import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Real-Time Queue Waiting Time Predictor",
    page_icon="🚦",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #e3f2fd, #ffffff);
}
.card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 2px 2px 12px rgba(0,0,0,0.15);
    margin-bottom: 15px;
}
.green {color:#2e7d32;}
.orange {color:#ff8f00;}
.red {color:#c62828;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE DEFAULTS ----------------
defaults = {
    "page": 1,
    "people": 20,
    "staff": 3,
    "service_time": 5,
    "arrival_rate": 2,
    "staff_exp": "Average",
    "system_status": "Normal",
    "peak": False,
    "wait_time": 0,
    "served": 0,
    "running": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- FUNCTIONS ----------------
def exp_factor(exp):
    return {"New": 0.8, "Average": 1.0, "Expert": 1.3}[exp]

def system_factor(sys):
    return {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]

def predict_wait(queue):
    base = (queue * st.session_state.service_time) / st.session_state.staff
    return round(base * exp_factor(st.session_state.staff_exp) *
                 system_factor(st.session_state.system_status) *
                 (1.3 if st.session_state.peak else 1.0), 2)

def queue_mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd", "green"
    elif wait <= 30:
        return "🟡 Medium Crowd", "orange"
    else:
        return "🔴 Heavy Crowd", "red"

# ---------------- PAGE 1 : INPUT ----------------
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Waiting Time Predictor")
    st.write("Real-time, user-friendly and intelligent queue prediction system")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.session_state.people = st.slider("👥 People in Queue", 0, 100, st.session_state.people)
        st.session_state.staff = st.slider("👨‍💼 Staff Available", 1, 10, st.session_state.staff)
        st.session_state.service_time = st.slider("⏱ Service Time (minutes)", 1, 10, st.session_state.service_time)
        st.session_state.arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 5, st.session_state.arrival_rate)

        st.session_state.staff_exp = st.selectbox(
            "🎓 Staff Experience", ["New", "Average", "Expert"]
        )

        st.session_state.system_status = st.selectbox(
            "🖥 System Status", ["Normal", "Slow", "Down"]
        )

        st.session_state.peak = st.checkbox("🚨 Peak Hour")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Predict & Start Live Queue"):
        st.session_state.wait_time = predict_wait(st.session_state.people)
        st.session_state.page = 2
        st.session_state.running = True
        st.rerun()

# ---------------- PAGE 2 : LIVE QUEUE ----------------
elif st.session_state.page == 2:
    st.title("📊 Live Queue Status")

    mood, color = queue_mood(st.session_state.wait_time)

    box = st.empty()
    bar = st.progress(0)

    for i in range(25):
        if not st.session_state.running:
            break

        served_now = int(st.session_state.staff * exp_factor(st.session_state.staff_exp))
        arrived_now = st.session_state.arrival_rate

        st.session_state.people = max(0, st.session_state.people - served_now + arrived_now)
        st.session_state.served += served_now
        st.session_state.wait_time = predict_wait(st.session_state.people)

        mood, color = queue_mood(st.session_state.wait_time)

        bar.progress((i + 1) * 4)

        box.markdown(f"""
        <div class="card">
            <h3>⏳ Waiting Time: {st.session_state.wait_time} mins</h3>
            <h4 class="{color}">{mood}</h4>
            👥 Remaining Queue: <b>{st.session_state.people}</b><br>
            ✅ People Served: <b>{st.session_state.served}</b><br>
            🕒 Expected Service Time: 
            {(datetime.now()+timedelta(minutes=st.session_state.wait_time)).strftime('%I:%M %p')}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 Smart Suggestions"):
            st.session_state.page = 3
            st.rerun()
    with col2:
        if st.button("🏠 Back to Home"):
            st.session_state.page = 1
            st.session_state.running = False
            st.rerun()

# ---------------- PAGE 3 : SMART INSIGHTS ----------------
elif st.session_state.page == 3:
    st.title("💡 Smart Insights & Decisions")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.write("### ❗ Delay Reasons")
        if st.session_state.system_status != "Normal":
            st.write("🖥 System performance issues")
        if st.session_state.staff_exp == "New":
            st.write("🎓 New staff handling customers")
        if st.session_state.people > 30:
            st.write("👥 High crowd volume")
        if st.session_state.arrival_rate > 2:
            st.write("📈 High arrival rate")

        st.markdown('</div>', unsafe_allow_html=True)

    improved_staff = st.session_state.staff + 1
    improved_time = predict_wait(st.session_state.people)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"""
        👨‍💼 **Add 1 Staff**
        - Old Waiting Time: {st.session_state.wait_time} mins  
        - New Waiting Time: {improved_time} mins
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    best_time = "2:30 PM – 4:00 PM" if st.session_state.peak else "Non-peak hours"
    st.info(f"🕒 Best Time to Visit: {best_time}")

    if st.button("🔄 What-If Simulation"):
        st.session_state.page = 4
        st.rerun()

# ---------------- PAGE 4 : WHAT-IF ----------------
elif st.session_state.page == 4:
    st.title("🔄 What-If Simulation")

    sim_staff = st.slider("👨‍💼 Staff Count", 1, 10, st.session_state.staff)
    sim_service = st.slider("⏱ Service Time", 1, 10, st.session_state.service_time)

    sim_wait = (st.session_state.people * sim_service) / sim_staff

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"""
        📊 **Simulation Result**
        - Staff: {sim_staff}
        - Service Time: {sim_service} mins
        - New Waiting Time: {round(sim_wait,2)} mins
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
