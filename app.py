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
body {
    background-color: #0d1b2a;
    color: white;
    font-family: Arial, sans-serif;
}
h1, h2, h3 {
    font-weight: bold;
    color: #00ffcc;
}
.queue-box {
    border: 2px solid #00ffcc;
    padding: 15px;
    border-radius: 10px;
    background-color: #1b263b;
    font-weight: bold;
    text-align: center;
}
.container-box {
    background-color: #1b263b;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-weight: bold;
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
    return round(base * exp_w * sys_w * peak_w + arr * 2, 1)

# ---------------- QR CODE (WORKING) ----------------
def generate_qr_image(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# ================= PAGE 1 : HOME =================
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Predictor")

    st.session_state.people_ahead = st.slider("👥 People Ahead", 0, 50, st.session_state.people_ahead)
    st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    st.session_state.service_time = st.slider("⏱ Service Time (mins)", 2, 10, st.session_state.service_time)
    st.session_state.arrival_rate = st.slider("📈 Arrival Rate", 0, 5, st.session_state.arrival_rate)

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
        st.session_state.predicted = True

    if st.session_state.predicted:
        now = datetime.now()
        expected = now + timedelta(minutes=st.session_state.wait_time)

        st.markdown(f"<div class='container-box'>⏳ Waiting Time: {st.session_state.wait_time} mins</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='container-box'>🕒 Expected Turn: {expected.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)

        if st.button("➡️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 : LIVE QUEUE =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue")

    st.markdown(f"<div class='container-box'>Your Position: {st.session_state.position}</div>", unsafe_allow_html=True)
    progress = st.progress(0)
    box = st.empty()

    total = st.session_state.position

    if st.button("▶️ Start Simulation"):
        for i in range(total + 1):
            remaining = total - i
            st.session_state.position = remaining
            progress.progress(i / max(1, total))

            box.markdown(
                f"<div class='queue-box'>{'👤 ' * remaining}</div>",
                unsafe_allow_html=True
            )
            time.sleep(1)

        st.success("🎉 Service Completed!")

    # -------- LIVE QR CODE --------
    expected_turn = (datetime.now() + timedelta(minutes=st.session_state.wait_time)).strftime('%I:%M %p')

    qr_data = f"""
SMART QUEUE STATUS
Position: {st.session_state.position}
Waiting Time: {st.session_state.wait_time} mins
Expected Turn: {expected_turn}
"""

    qr_img = generate_qr_image(qr_data)
    st.image(qr_img, caption="📱 Scan for Live Queue Status")

    if st.button("➡️ Download Report"):
        st.session_state.page = 3
        st.rerun()

# ================= PAGE 3 : REPORT =================
elif st.session_state.page == 3:
    st.title("📄 Queue Report")

    expected_turn = (datetime.now() + timedelta(minutes=st.session_state.wait_time)).strftime('%I:%M %p')

    report = f"""
SMART QUEUE REPORT

People Ahead: {st.session_state.people_ahead}
Staff Count: {st.session_state.staff}
Service Time: {st.session_state.service_time} mins
Arrival Rate: {st.session_state.arrival_rate}

Waiting Time: {st.session_state.wait_time} mins
Expected Turn Time: {expected_turn}

STATUS: Queue completed successfully
"""

    st.download_button("📥 Download Report", report, file_name="queue_report.txt")

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
