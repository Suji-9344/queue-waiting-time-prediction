import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Management System",
    page_icon="⏱",
    layout="wide"
)

# ---------------- CSS DESIGN ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #3b82f6, #f97316);
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.header {
    background: linear-gradient(90deg, #1e3a8a, #2563eb);
    padding: 20px;
    border-radius: 20px;
    color: white;
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}

/* Highlight card */
.alert-card {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    padding: 18px;
    border-radius: 18px;
}

/* Queue */
.queue-box {
    background: #e0f2fe;
    border-radius: 20px;
    padding: 15px;
    text-align: center;
    font-size: 24px;
    border: 3px dashed #2563eb;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #1e40af);
    color: white;
    border-radius: 15px;
    font-size: 16px;
    padding: 10px 20px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='header'>🚦 SMART QUEUE MANAGEMENT SYSTEM</div>", unsafe_allow_html=True)

# ---------------- TOP NAV ----------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["🔮 Predictor", "🔄 Live Queue", "🚨 Alerts", "♿ Priority"]
)

# ================= TAB 1 : PREDICTOR =================
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("⏱ Wait Time Estimator")

        people = st.slider("👥 People Ahead", 0, 50, 12)
        staff = st.slider("👨‍💼 Staff", 1, 5, 3)
        service = st.slider("⏳ Service Time (mins)", 2, 10, 6)
        arrival = st.slider("📈 Arrival Rate", 0, 5, 2)

        if st.button("🔍 Predict"):
            wait = round((people * service) / staff + arrival * 2, 1)
            st.success(f"Estimated Wait: {wait} mins")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 AI Prediction Result")

        st.write("🕒 **Now Serving:** A-23")
        st.write("⏳ **Approx Wait:** 5 minutes")
        st.progress(0.6)
        st.info("🟡 Queue Mood: Medium Crowd")
        st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2 : LIVE QUEUE =================
with tab2:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔄 Live Queue Tracker")

        queue_container = st.empty()
        progress = st.progress(0)

        if st.button("▶️ Start Live Queue"):
            total = 12
            for i in range(total + 1):
                remaining = total - i
                progress.progress(i / total)
                queue_container.markdown(
                    f"<div class='queue-box'>{'👤 ' * remaining}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.5)

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📍 Your Status")
        st.write("Your Position: **4 / 12**")
        st.write("Expected Time: **5 mins**")
        st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 3 : ALERTS =================
with tab3:
    st.markdown("<div class='alert-card'>", unsafe_allow_html=True)
    st.subheader("🚨 Crowd Surge Alert")
    st.error("Heavy crowd expected in next 10 minutes")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔔 Smart Notifications")
    st.warning("Your turn in 3 minutes")
    st.info("Please be ready at counter")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 4 : PRIORITY =================
with tab4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("♿ Priority Queue System")

    st.write("✅ Senior citizens")
    st.write("✅ Pregnant women")
    st.write("✅ Emergency cases")

    st.success("Priority users get reduced waiting time")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div style="text-align:center;color:white;margin-top:30px;">
Ethical AI | Smart Alerts | Digital Queue | Decision Support
</div>
""", unsafe_allow_html=True)
