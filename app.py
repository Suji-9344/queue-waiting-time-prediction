import streamlit as st
import time
import random
from datetime import datetime, timedelta
import urllib.parse

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue System",
    page_icon="🚦",
    layout="centered"
)

# ---------------- DARK UI CSS ----------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #0f2027, #203a43, #2c5364);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

h1, h2, h3, h4 {
    color: #00eaff;
    font-weight: 800;
}

label, p, span {
    color: #ffffff !important;
    font-weight: 600;
}

.stButton > button {
    background: linear-gradient(90deg, #00eaff, #00ffa6);
    color: #000;
    font-weight: 800;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.05);
}

.queue-box {
    background: rgba(0, 234, 255, 0.15);
    border: 2px solid #00eaff;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
}

.card {
    background: rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #00eaff;
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
    "expected_time": "",
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

# ================= PAGE 1 =================
if st.session_state.page == 1:
    st.markdown("<h1 style='text-align:center;'>🚦 SMART QUEUE PREDICTOR & LIVE TRACKER</h1>", unsafe_allow_html=True)

    st.session_state.people_ahead = st.slider("👥 People Ahead", 0, 50, st.session_state.people_ahead)
    st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    st.session_state.service_time = st.slider("⏱ Service Time (mins)", 2, 10, st.session_state.service_time)
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

        now = datetime.now()
        expected = now + timedelta(minutes=st.session_state.wait_time)
        st.session_state.expected_time = expected.strftime("%I:%M %p")

        st.session_state.position = st.session_state.people_ahead
        st.session_state.served = 0
        st.session_state.predicted = True

    if st.session_state.predicted:
        st.markdown(f"""
        <div class="card">
        ⏳ <b>Waiting Time:</b> {st.session_state.wait_time} minutes<br>
        🕒 <b>Expected Turn Time:</b> {st.session_state.expected_time}
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 =================
elif st.session_state.page == 2:
    st.title("🔄 LIVE QUEUE STATUS")

    progress = st.progress(0)
    box = st.empty()

    total = st.session_state.position

    for i in range(total + 1):
        remaining = total - i
        st.session_state.position = remaining
        st.session_state.served = i

        progress.progress(i / max(1, total))
        box.markdown(f"<div class='queue-box'>👤 Remaining in Queue: {remaining}</div>", unsafe_allow_html=True)

        time.sleep(1)

    st.success("🎉 Your service is completed!")

    # -------- WORKING QR CODE --------
    qr_data = f"Queue Position: {st.session_state.position}, Waiting Time: {st.session_state.wait_time} mins, Expected Time: {st.session_state.expected_time}"
    encoded = urllib.parse.quote(qr_data)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={encoded}"

    st.markdown("### 📱 Scan QR for Live Queue Status")
    st.image(qr_url)

    if st.button("➡️ Smart Suggestions"):
        st.session_state.page = 3
        st.rerun()

# ================= PAGE 3 =================
elif st.session_state.page == 3:
    st.title("💡 SMART SUGGESTIONS")

    st.markdown("""
    <div class="card">
    ✅ Open extra counters when queue > 15<br>
    🕓 Best visit time: 4 PM – 6 PM<br>
    🚦 Avoid queue if people > 20<br>
    ⭐ Priority queue for seniors & emergencies
    </div>
    """, unsafe_allow_html=True)

    if st.button("➡️ Download Report"):
        st.session_state.page = 4
        st.rerun()

# ================= PAGE 4 =================
elif st.session_state.page == 4:
    st.title("📄 QUEUE REPORT")

    report = f"""
SMART QUEUE MANAGEMENT REPORT

People Ahead: {st.session_state.people_ahead}
Staff Count: {st.session_state.staff}
Service Time: {st.session_state.service_time} mins
Arrival Rate: {st.session_state.arrival_rate}

Predicted Waiting Time: {st.session_state.wait_time} mins
Expected Turn Time: {st.session_state.expected_time}

STATUS: COMPLETED SUCCESSFULLY
"""

    st.download_button("📥 Download Report", report, file_name="queue_report.txt")

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
