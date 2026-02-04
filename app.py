import streamlit as st
import time
import random
import qrcode
from io import BytesIO
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue System",
    page_icon="⏱",
    layout="centered"
)

# ---------------- CUSTOM CSS & STYLING ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #f0f2f6, #e1e8f0);
    }
    .highlight {
        color: #0073e6;
        font-weight: bold;
        background-color: #e6f3ff;
        padding: 2px 5px;
        border-radius: 4px;
    }
    .queue-box {
        border: 2px solid #0073e6;
        padding: 20px;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
        text-align: center;
        font-size: 24px;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0073e6;
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

# ---------------- HELPER FUNCTIONS ----------------
def predict_wait(p, s, staff, arr, exp, sys, peak):
    exp_w = {"New": 1.2, "Experienced": 1.0, "Expert": 0.8}[exp]
    sys_w = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]
    peak_w = 1.25 if peak else 1.0
    base = (p * s) / max(1, staff)
    arrival_effect = arr * 2
    return round(base * exp_w * sys_w * peak_w + arrival_effect, 1)

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ================= PAGE 1 : INPUT =================
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Predictor")
    
    # Adding a Hero Image
    st.image("https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&q=80&w=800", use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.people_ahead = st.slider("👥 People Ahead", 0, 50, st.session_state.people_ahead)
        st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    with col2:
        st.session_state.service_time = st.slider("⏱ Service Time (mins)", 2, 10, st.session_state.service_time)
        st.session_state.arrival_rate = st.slider("📈 Arrival Rate", 0, 5, st.session_state.arrival_rate)

    st.markdown("### 🛠 System Variables")
    c1, c2, c3 = st.columns(3)
    with c1: st.session_state.staff_exp = st.selectbox("🎓 Staff Experience", ["New", "Experienced", "Expert"])
    with c2: st.session_state.system_status = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
    with c3: st.session_state.peak = st.checkbox("🚨 Peak Hour")

    if st.button("🔍 Calculate Wait Time", use_container_width=True):
        st.session_state.wait_time = predict_wait(
            st.session_state.people_ahead, st.session_state.service_time,
            st.session_state.staff, st.session_state.arrival_rate,
            st.session_state.staff_exp, st.session_state.system_status, st.session_state.peak
        )
        st.session_state.predicted = True

    if st.session_state.predicted:
        # REAL-TIME CALCULATION
        turn_time = datetime.now() + timedelta(minutes=st.session_state.wait_time)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h3>📊 Analysis Result</h3>
            <p>Estimated Waiting: <span class='highlight'>{st.session_state.wait_time} mins</span></p>
            <p>Expected Turn: <spa
