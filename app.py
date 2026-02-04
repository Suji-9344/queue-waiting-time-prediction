import streamlit as st
import time
from datetime import datetime, timedelta
import urllib.parse

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue System",
    page_icon="⏱",
    layout="centered"
)

# ---------------- STRONG HIGH-CONTRAST CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0b132b;
    color: #ffffff;
    font-family: Arial, sans-serif;
}

h1 {
    color: #00f5ff;
    font-weight: 900;
    text-align: center;
}

h2, h3 {
    color: #22ff88;
    font-weight: 800;
}

label, p, span, div {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.stSlider > label {
    font-size: 18px;
    color: #ffffff !important;
}

.stSelectbox > label, .stCheckbox > label {
    font-size: 18px;
    color: #ffffff !important;
}

.stButton > button {
    background-color: #00f5ff;
    color: #000000;
    font-size: 18px;
    font-weight: 900;
    border-radius: 12px;
    padding: 10px 20px;
}

.stButton > button:hover {
    background-color: #22ff88;
    color: #000;
}

.card {
    background-color: #1c2541;
    border: 2px solid #00f5ff;
    border-radius: 12px;
    padding: 15px;
    margin-top: 15px;
    font-size: 18px;
}

.queue-box {
    background-color: #3a86ff;
    color: #ffffff;
    font-size: 22px;
    font-weight: 900;
    text-align: center;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
defaults = {
    "page": 1,
    "people_ahead": 10,
    "staff": 2,
    "service_time": 5,
    "wait_time": 0,
    "expected_time": "",
    "position": 0,
    "predicted": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- WAIT TIME FUNCTION ----------------
def predict_wait(people, service_time, staff):
    return round((people * service_time) / max(1, staff), 1)

# ================= PAGE 1 : HOME =================
if st.session_state.page == 1:
    st.markdown("<h1>🚦 SMART QUEUE MANAGEMENT SYSTEM</h1>", unsafe_allow_html=True)

    st.session_state.people_ahead = st.slider(
        "👥 Number of People Ahead", 0, 50, st.session_state.people_ahead
    )
    st.session_state.staff = st.slider(
        "👨‍💼 Number of Staff", 1, 5, st.session_state.staff
    )
    st.session_state.service_time = st.slider(
        "⏱ Average Service Time (minutes)", 2, 10, st.session_state.service_time
    )

    if st.button("🔍 Predict Waiting Time"):
        # -------- WAIT TIME --------
        st.session_state.wait_time = predict_wait(
            st.session_state.people_ahead,
            st.session_state.service_time,
            st.session_state.staff
        )

        # ✅ EXPECTED TURN TIME (CORRECT CODE)
        current_time = datetime.now()
        expected_turn_time = current_time + timedelta(
            minutes=st.session_state.wait_time
        )
        st.session_state.expected_time = expected_turn_time.strftime("%I:%M %p")

        st.session_state.position = st.session_state.people_ahead
        st.session_state.predicted = True

    if st.session_state.predicted:
        st.markdown(f"""
        <div class="card">
        ⏳ <b>Predicted Waiting Time:</b> {st.session_state.wait_time} minutes<br><br>
        🕒 <b>Expected Turn Time:</b> {st.session_state.expected_time}
        </div>
        """, unsafe_allow_html=True)

        if st.button("▶️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 : LIVE QUEUE =================
elif st.session_state.page == 2:
    st.markdown("<h2>🔄 LIVE QUEUE STATUS</h2>", unsafe_allow_html=True)

    progress = st.progress(0)
    display = st.empty()
    total = st.session_state.position

    for i in range(total + 1):
        remaining = total - i
        st.session_state.position = remaining
        progress.progress(i / max(1, total))

        display.markdown(
            f"<div class='queue-box'>👤 Remaining People: {remaining}</div>",
            unsafe_allow_html=True
        )
        time.sleep(1)

    st.success("🎉 Service Completed Successfully!")

    # ---------------- QR CODE ----------------
    qr_text = f"""
Queue Status
People Remaining: {st.session_state.position}
Waiting Time: {st.session_state.wait_time} minutes
Expected Turn Time: {st.session_state.expected_time}
"""
    encoded = urllib.parse.quote(qr_text)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={encoded}"

    st.markdown("### 📱 Scan QR Code for Queue Details")
    st.image(qr_url)

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
