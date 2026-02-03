import streamlit as st
import time
import random
from datetime import datetime, timedelta
import pyqrcode
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
body {
    background-color: #0d1b2a;
    color: #ffffff;
    font-family: 'Arial', sans-serif;
}
h1, h2, h3, h4, h5, h6, .stButton button {
    font-weight: bold;
}
.queue-box {
    border: 2px solid #00ffcc;
    padding: 15px;
    border-radius: 12px;
    background-color: #1b263b;
    margin-bottom: 10px;
    color: #ffffff;
    font-weight: bold;
    text-align: center;
}
.progress-bar > div {
    background-color: #00ffcc !important;
}
.header-img {
    width: 100%;
    border-radius: 12px;
    margin-bottom: 20px;
}
.container-box {
    background-color: #1b263b;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 20px;
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

# ---------------- ML-LIKE WAIT TIME PREDICTION ----------------
def predict_wait(p, s, staff, arr, exp, sys, peak):
    exp_w = {"New": 1.2, "Experienced": 1.0, "Expert": 0.8}[exp]
    sys_w = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]
    peak_w = 1.25 if peak else 1.0
    base = (p * s) / max(1, staff)
    arrival_effect = arr * 2
    return round(base * exp_w * sys_w * peak_w + arrival_effect, 1)

# ---------------- QUEUE MOOD ----------------
def queue_mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd"
    elif wait <= 30:
        return "🟡 Medium Crowd"
    else:
        return "🔴 Heavy Crowd"

# ---------------- STAFF EFFICIENCY ----------------
def staff_efficiency(staff_count, service_time):
    efficiency = min(100, (staff_count * 10) / service_time * 10)
    return round(efficiency, 1)

# ---------------- GENERATE QR ----------------
def generate_qr(data):
    qr = pyqrcode.create(data)
    buffer = BytesIO()
    qr.png(buffer, scale=5, module_color=[0, 255, 204, 255], background=[27,38,59,255])
    buffer.seek(0)
    return buffer

# ================= PAGE 1 : HOME =================
if st.session_state.page == 1:
    st.markdown("<h1 style='color:#00ffcc;text-align:center;'>🚦 Smart Queue Predictor & Live Tracker</h1>", unsafe_allow_html=True)

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
        current_time = datetime.now()
        expected_turn_time = current_time + timedelta(minutes=st.session_state.wait_time)
        st.markdown(f"<div class='container-box'>⏳ <b>Estimated Waiting Time:</b> {st.session_state.wait_time} minutes</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='container-box'>🕒 <b>Expected Turn Time:</b> {expected_turn_time.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='container-box'>Queue Mood: {queue_mood(st.session_state.wait_time)}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='container-box'>Staff Efficiency: {staff_efficiency(st.session_state.staff, st.session_state.service_time)}%</div>", unsafe_allow_html=True)
        
        if st.button("➡️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 : LIVE QUEUE =================
elif st.session_state.page == 2:
    st.markdown("<h1 style='color:#00ffcc;text-align:center;'>🔄 Live Queue Simulation</h1>", unsafe_allow_html=True)

    st.markdown(f"<div class='container-box'>🙋 Your Current Position: {st.session_state.position}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='container-box'>✅ People Served: {st.session_state.served}</div>", unsafe_allow_html=True)
    progress_bar = st.progress(0)
    queue_container = st.empty()

    if st.button("▶️ Start Simulation"):
        total = st.session_state.position
        for i in range(total + 1):
            remaining = total - i
            st.session_state.position = remaining
            st.session_state.served += 1

            progress_bar.progress(i / max(1, total))

            people_icons = "👤 " * remaining
            queue_container.markdown(f"<div class='queue-box'>{people_icons}</div>", unsafe_allow_html=True)

            if remaining > 12:
                st.warning(f"⚠️ {random.randint(1,3)} people may leave due to long wait")
            else:
                st.info("✅ Good time to join queue now")

            if i > 0 and (remaining - (total - i - 1)) >= 2:
                st.error("🚨 Crowd surge detected! Monitor staff allocation")

            if remaining > 20:
                st.info("🤖 AI triggered: Add extra staff to counters")

            if remaining == 3:
                st.warning("🔔 Your turn is coming soon!")
                st.info("🔊 Voice Alert: Your turn is coming in few minutes")

            time.sleep(1)

        st.success("🎉 Your service is completed!")

    st.subheader("📱 QR Code for Live Queue Status")
    qr_data = f"Position:{st.session_state.position}, Waiting:{st.session_state.wait_time} mins"
    qr_img = generate_qr(qr_data)
    st.image(qr_img)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Back to Home"):
        st.session_state.page = 1
        st.rerun()
    if col2.button("➡️ Smart Suggestions"):
        st.session_state.page = 3
        st.rerun()

# ================= PAGE 3 : SMART SUGGESTIONS =================
elif st.session_state.page == 3:
    st.markdown("<h1 style='color:#00ffcc;text-align:center;'>💡 Smart Suggestions</h1>", unsafe_allow_html=True)

    st.markdown("""
<div class='container-box'>
1. 🟢 Dynamic Counter Opening: Add staff if queue > 15<br>
2. 🕒 Best Time to Visit: 4:00 PM – 6:00 PM<br>
3. ⚠️ Join or Avoid Queue Advice: Join when queue < 12, avoid otherwise<br>
4. 🔧 Staff Reallocation: Move staff to busy counters<br>
5. ⭐ Priority Queue Recommendation: For seniors and emergencies<br>
6. 📊 Live Crowd Percentage: Monitor real-time queue status
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Back to Live Queue"):
        st.session_state.page = 2
        st.rerun()
    if col2.button("➡️ Download Report"):
        st.session_state.page = 4
        st.rerun()

# ================= PAGE 4 : REPORT =================
elif st.session_state.page == 4:
    st.markdown("<h1 style='color:#00ffcc;text-align:center;'>📄 Queue Report</h1>", unsafe_allow_html=True)

    expected_turn_time = datetime.now() + timedelta(minutes=st.session_state.wait_time)
    report = f"""
SMART QUEUE MANAGEMENT REPORT
----------------------------

People Ahead: {st.session_state.people_ahead}
Staff Count: {st.session_state.staff}
Service Time: {st.session_state.service_time} mins
Arrival Rate: {st.session_state.arrival_rate} people/min
Staff Experience: {st.session_state.staff_exp}
System Status: {st.session_state.system_status}

Predicted Waiting Time: {st.session_state.wait_time} minutes
Expected Turn Time: {expected_turn_time.strftime('%I:%M %p')}

SMART SUGGESTIONS APPLIED:
- Dynamic counter opening
- Best time to visit
- Join or avoid queue advice
- Staff reallocation
- Priority queue recommendation
- Live crowd monitoring

LIVE QUEUE FEATURES APPLIED:
- Digital twin live queue
- Live join/leave prediction
- Crowd surge detection
- Auto staff trigger
- Explainable AI message

STATUS: Queue completed successfully
"""
    st.download_button("📥 Download Report", report, file_name="queue_report.txt", key="download_report")

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
