import streamlit as st
import time
import random
from datetime import datetime, timedelta
from urllib.parse import quote

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue System",
    page_icon="⏱",
    layout="centered"
)

# ---------------- COLORFUL BACKGROUND & UI ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
    font-family: 'Arial', sans-serif;
    color: white;
}

h1, h2, h3 {
    color: #ffffff;
    font-weight: 900;
}

.queue-box {
    border: 2px solid #00f5ff;
    padding: 15px;
    border-radius: 12px;
    background-color: #1f2a44;
    margin-bottom: 10px;
    text-align: center;
    font-size: 20px;
}

.stButton > button {
    background-color: #00f5ff;
    color: black;
    font-weight: 900;
    border-radius: 12px;
    padding: 8px 20px;
}

.stButton > button:hover {
    background-color: #22ff88;
}

.stSlider label, .stSelectbox label, .stCheckbox label {
    font-weight: 700;
    color: white;
}

.card {
    background-color: #1f2a44;
    padding: 15px;
    border-radius: 12px;
    border: 2px solid #22ff88;
    margin-bottom: 15px;
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
    "predicted": False
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
    arrival_effect = arr * 2
    return round(base * exp_w * sys_w * peak_w + arrival_effect, 1)

def queue_mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd"
    elif wait <= 30:
        return "🟡 Medium Crowd"
    else:
        return "🔴 Heavy Crowd"

# ================= PAGE 1 =================
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Predictor & Live Tracker")

    st.session_state.people_ahead = st.slider("👥 People Ahead of You", 0, 50, st.session_state.people_ahead)
    st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    st.session_state.service_time = st.slider("⏱ Average Service Time (mins)", 2, 10, st.session_state.service_time)
    st.session_state.arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 5, st.session_state.arrival_rate)

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

    if st.session_state.predicted:
        end_time = datetime.now() + timedelta(minutes=st.session_state.wait_time)

        st.markdown(f"""
        <div class="card">
        ⏳ <b>Estimated Waiting Time:</b> {st.session_state.wait_time} minutes<br><br>
        🕒 <b>Expected Turn Time:</b> {end_time.strftime('%I:%M %p')}<br><br>
        🚦 <b>Queue Mood:</b> {queue_mood(st.session_state.wait_time)}
        </div>
        """, unsafe_allow_html=True)

        if st.button("➡️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Simulation")

    progress_bar = st.progress(0)
    queue_container = st.empty()

    if st.button("▶️ Start Simulation"):
        total = st.session_state.position
        for i in range(total + 1):
            remaining = total - i
            st.session_state.position = remaining
            st.session_state.served += 1

            progress_bar.progress(i / max(1, total))
            queue_container.markdown(
                f"<div class='queue-box'>{'👤 ' * remaining}</div>",
                unsafe_allow_html=True
            )

            if remaining == 3:
                st.warning("🔔 Your turn is coming soon!")

            time.sleep(1)

        st.success("🎉 Service Completed Successfully!")

    # ---------------- WORKING QR CODE ----------------
    qr_data = f"""
Queue Status
Remaining: {st.session_state.position}
Waiting Time: {st.session_state.wait_time} minutes
"""
    qr_encoded = quote(qr_data)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={qr_encoded}"

    st.subheader("📱 Scan QR for Live Queue Status")
    st.image(qr_url)

    if st.button("➡️ Smart Suggestions"):
        st.session_state.page = 3
        st.rerun()

# ================= PAGE 3 =================
elif st.session_state.page == 3:
    st.title("💡 Smart Suggestions")
    st.write("🟢 Add staff if queue > 15")
    st.write("🕒 Best time: 4 PM – 6 PM")
    st.write("⚠️ Avoid peak hours")
    st.write("⭐ Priority queue for seniors")

    if st.button("➡️ Download Report"):
        st.session_state.page = 4
        st.rerun()

# ================= PAGE 4 =================
elif st.session_state.page == 4:
    st.title("📄 Queue Report")

    report = f"""
SMART QUEUE MANAGEMENT REPORT

People Ahead: {st.session_state.people_ahead}
Staff Count: {st.session_state.staff}
Service Time: {st.session_state.service_time}
Arrival Rate: {st.session_state.arrival_rate}

Predicted Waiting Time: {st.session_state.wait_time} minutes
Status: Queue Completed
"""

    st.download_button("📥 Download Report", report, file_name="queue_report.txt")

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
