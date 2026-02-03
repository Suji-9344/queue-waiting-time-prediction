import streamlit as st
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Management System",
    page_icon="⏱",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #2563eb, #f97316);
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
.header {
    background: linear-gradient(90deg, #1e3a8a, #2563eb);
    padding: 18px;
    border-radius: 20px;
    color: #fde68a;
    text-align: center;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 25px;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    font-size: 16px;
    font-weight: 700;
    color: #1e3a8a;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.95);
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 8px 18px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}

/* Alert Card */
.alert {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    padding: 18px;
    border-radius: 18px;
    font-weight: 700;
}

/* Notification Card */
.notify {
    background: linear-gradient(135deg, #ede9fe, #ddd6fe);
    padding: 18px;
    border-radius: 18px;
    font-weight: 700;
}

/* Queue */
.queue-box {
    border: 3px dashed #2563eb;
    padding: 15px;
    border-radius: 20px;
    background: #eff6ff;
    font-size: 22px;
    text-align: center;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb, #1e40af);
    color: white;
    border-radius: 15px;
    font-size: 16px;
    padding: 10px 22px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    "<div class='header'>🚦 SMART QUEUE MANAGEMENT SYSTEM</div>",
    unsafe_allow_html=True
)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs(
    ["Predictor", "Live Queue", "Suggestions", "Priority & Alerts"]
)

# ================= TAB 1 =================
with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("⏱ Wait Time Estimator")

        st.write("**People Ahead:** 12")
        st.write("**Staff Count:** 3")
        st.write("**Service Time:** 6 mins")
        st.write("**Arrival Rate:** 2 / min")

        st.success("Estimated Wait Time: **18 mins**")
        st.info("Queue Mood: 🟡 Medium Crowd")

        st.button("▶ Start Live Queue")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Live Queue Tracker")

        st.markdown("### **NOW SERVING A-23**")
        st.write("Approx Wait: **5 mins**")
        st.progress(0.6)

        st.markdown("<div class='queue-box'>👤 👤 👤 👤 👤 👤 👤</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 2 =================
with tab2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🔄 Live Queue Simulation")

    queue_area = st.empty()
    progress = st.progress(0)

    if st.button("▶ Start Simulation"):
        total = 12
        for i in range(total + 1):
            remain = total - i
            progress.progress(i / total)
            queue_area.markdown(
                f"<div class='queue-box'>{'👤 ' * remain}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.4)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 3 =================
with tab3:
    st.markdown("<div class='alert'>", unsafe_allow_html=True)
    st.subheader("🚨 Crowd Surge Alert!")
    st.write("⚠ Heavy crowd incoming. Surge expected soon.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='notify'>", unsafe_allow_html=True)
    st.subheader("🔔 Smart Notifications")
    st.write("🔔 Your turn in **3 minutes**")
    st.write("📢 Get ready for service!")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= TAB 4 =================
with tab4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("♿ Priority Queue System")

    st.write("✔ Senior citizens")
    st.write("✔ Pregnant women")
    st.write("✔ Emergency cases")

    st.success("Fast-track service enabled for priority users")
    st.markdown("</div>", unsafe_allow_html=True)

# ================= IMAGE SECTION =================
st.markdown("## 🎨 UI Design Preview")
st.image("dashboard_ui.png", use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div style="text-align:center;color:white;margin-top:30px;font-weight:600;">
Ethical AI | Smart Alerts | Digital Queue | Decision Support
</div>
""", unsafe_allow_html=True)
