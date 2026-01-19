import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Live Queue Waiting Time System",
    page_icon="⏱",
    layout="centered"
)

# ---------------- SESSION STATE INIT ----------------
defaults = {
    "page": 1,
    "people": 10,
    "service": 5,
    "staff": 2,
    "exp": "Experienced",
    "system": "Normal",
    "peak": False,
    "wait": 0,
    "predicted": False,
    "served": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- FUNCTIONS ----------------
def calculate_waiting_time(p, s, staff, exp, sys, peak):
    exp_factor = {"New": 1.2, "Experienced": 1.0, "Expert": 0.85}[exp]
    sys_factor = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]
    peak_factor = 1.25 if peak else 1.0

    base = (p * s) / max(1, staff)
    noise = np.random.uniform(-2, 2)
    wait = base * exp_factor * sys_factor * peak_factor + noise
    return max(0, round(wait, 1))

def delay_reason():
    reasons = []
    if st.session_state.people > 20:
        reasons.append("👥 High crowd")
    if st.session_state.exp == "New":
        reasons.append("🎓 New staff")
    if st.session_state.system != "Normal":
        reasons.append("🖥 System issues")
    if st.session_state.peak:
        reasons.append("🚨 Peak hour traffic")
    return reasons if reasons else ["✅ Normal flow"]

def queue_mood(wait):
    if wait < 10:
        return "😄 Happy"
    elif wait < 25:
        return "😐 Neutral"
    return "😠 Frustrated"

def smart_suggestions():
    tips = []
    if st.session_state.peak:
        tips.append("⏰ Avoid peak hours (11AM–2PM)")
    if st.session_state.system != "Normal":
        tips.append("🖥 Come later due to system delay")
    tips.append("📱 Off-peak time: 4PM–6PM")
    return tips

# ---------------- NAVIGATION ----------------
st.sidebar.title("📍 Navigation")
if st.sidebar.button("🏠 Predictor"):
    st.session_state.page = 1
if st.sidebar.button("🔄 Live Queue"):
    st.session_state.page = 2
if st.sidebar.button("🧠 Smart Suggestions"):
    st.session_state.page = 3

# ================= PAGE 1 =================
if st.session_state.page == 1:
    st.title("🚦 Queue Waiting Time Predictor")

    st.session_state.people = st.number_input("👥 People Ahead", 0, 50, st.session_state.people)
    st.session_state.service = st.number_input("⏱ Avg Service Time (minutes)", 2, 10, st.session_state.service)
    st.session_state.staff = st.number_input("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    st.session_state.exp = st.selectbox("🎓 Staff Experience", ["New", "Experienced", "Expert"])
    st.session_state.system = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
    st.session_state.peak = st.selectbox("🚨 Peak Hour", ["No", "Yes"]) == "Yes"

    if st.button("Predict Waiting Time"):
        st.session_state.wait = calculate_waiting_time(
            st.session_state.people,
            st.session_state.service,
            st.session_state.staff,
            st.session_state.exp,
            st.session_state.system,
            st.session_state.peak
        )
        st.session_state.predicted = True

    if st.session_state.predicted:
        finish = datetime.now() + timedelta(minutes=st.session_state.wait)
        st.success(f"⏱ Estimated Waiting Time: {st.session_state.wait} minutes")
        st.write(f"🕒 Expected Service Time: {finish.strftime('%I:%M %p')}")
        st.write(f"Queue Mood: {queue_mood(st.session_state.wait)}")

        st.subheader("❗ Delay Reasons")
        for r in delay_reason():
            st.write(r)

# ================= PAGE 2 =================
if st.session_state.page == 2:
    st.title("🔄 Live Queue Simulation")

    queue = st.session_state.people
    served = st.session_state.served

    progress = st.progress(0)

    for i in range(queue + 1):
        progress.progress(i / max(1, queue))
        st.write(f"🙋 People remaining: {queue - i}")
        st.write(f"✅ Served: {served + i}")

        if queue - i == 3:
            st.warning("🔔 Your turn is coming soon!")

        time.sleep(0.6)

    st.success("🎉 Your work is completed!")
    st.session_state.served += queue
    st.session_state.people = 0

# ================= PAGE 3 =================
if st.session_state.page == 3:
    st.title("🧠 Smart Suggestions & Peak Analysis")

    st.subheader("💡 Smart Tips")
    for tip in smart_suggestions():
        st.write(tip)

    st.subheader("📊 Peak Hour Heat Map")
    hours = ["9AM","10AM","11AM","12PM","1PM","2PM","3PM","4PM","5PM","6PM"]
    crowd = [5,10,25,40,45,35,20,15,10,5]

    fig, ax = plt.subplots()
    ax.plot(hours, crowd, marker='o')
    ax.set_ylabel("Crowd Level")
    ax.set_xlabel("Time")
    st.pyplot(fig)
