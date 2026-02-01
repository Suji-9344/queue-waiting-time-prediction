import streamlit as st
import time
import random
from datetime import datetime, timedelta
import qrcode
from PIL import Image
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue System",
    page_icon="⏱",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.queue-box {
    border: 2px solid #0073e6;
    padding: 15px;
    border-radius: 10px;
    background-color: #ffffff;
    margin-bottom: 10px;
    text-align: center;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
defaults = {
    "page": 1,
    "people_ahead": 10,
    "staff": 2,
    "service_time": 5,
    "arrival_rate": 1,
    "staff_exp": "Experienced",
    "system_status": "Normal",
    "peak": False,
    "wait_time": 0,
    "position": 0,
    "served": 0,
    "predicted": False,
    "simulation_started": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- WAIT TIME PREDICTION ----------------
def predict_wait(p, s, staff, arr, exp, sys, peak):
    exp_w = {"New": 1.2, "Experienced": 1.0, "Expert": 0.8}[exp]
    sys_w = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]
    peak_w = 1.25 if peak else 1.0
    base = (p * s) / max(1, staff)
    return round(base * exp_w * sys_w * peak_w + arr * 2, 1)

# ================= PAGE 1 =================
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Predictor")

    st.session_state.people_ahead = st.slider("👥 People Ahead", 0, 50, 10)
    st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, 2)
    st.session_state.service_time = st.slider("⏱ Service Time (mins)", 2, 10, 5)
    st.session_state.arrival_rate = st.slider("📈 Arrival Rate", 0, 5, 1)

    st.session_state.staff_exp = st.selectbox("🎓 Staff Experience", ["New", "Experienced", "Expert"])
    st.session_state.system_status = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
    st.session_state.peak = st.checkbox("🚨 Peak Hour")

    if st.button("🔍 Predict Waiting Time"):
        st.session_state.wait_time = predict_wait(
            st.session_state.people_ahead,
            st.session_state.service_time,
            st.session_state.staff,
            st.session_state.arrival_rate,
            st.session_state.staff_exp,
            st.session_state.system_status,
            st.session_state.peak
        )
        st.session_state.position = st.session_state.people_ahead
        st.session_state.served = 0
        st.session_state.predicted = True
        st.session_state.simulation_started = False

    if st.session_state.predicted:
        end_time = datetime.now() + timedelta(minutes=st.session_state.wait_time)
        st.success(f"⏳ Waiting Time: {st.session_state.wait_time} mins")
        st.info(f"🕒 Expected Turn: {end_time.strftime('%I:%M %p')}")

        if st.button("➡️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Simulation")

    st.write(f"🙋 Position: {st.session_state.position}")
    st.write(f"✅ Served: {st.session_state.served}")

    progress = st.progress(0)
    box = st.empty()

    if not st.session_state.simulation_started:
        if st.button("▶️ Start Simulation (One Time)"):
            st.session_state.simulation_started = True
            st.rerun()

    if st.session_state.simulation_started:
        total = st.session_state.position

        for i in range(total):
            remaining = total - i - 1
            st.session_state.position = remaining
            st.session_state.served += 1

            progress.progress((i + 1) / total)
            box.markdown(
                f"<div class='queue-box'>{'👤 ' * remaining}</div>",
                unsafe_allow_html=True
            )

            if remaining == 3:
                st.warning("🔔 Your turn is next!")
