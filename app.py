import streamlit as st
import time
import random
from datetime import datetime, timedelta

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
    background-color: #f4f9ff;
    font-family: Arial, sans-serif;
}
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
    arrival_effect = arr * 2
    return round(base * exp_w * sys_w * peak_w + arrival_effect, 1)

def queue_mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd"
    elif wait <= 30:
        return "🟡 Medium Crowd"
    else:
        return "🔴 Heavy Crowd"

# ================= PAGE 1 : INPUT =================
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Predictor & Live Tracker")

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
        st.session_state.position = st.session_state.people_ahead
        st.session_state.served = 0
        st.session_state.predicted = True
        st.session_state.simulation_started = False

    if st.session_state.predicted:
        end_time = datetime.now() + timedelta(minutes=st.session_state.wait_time)
        st.success(f"⏳ **Estimated Waiting Time:** {st.session_state.wait_time} minutes")
        st.info(f"🕒 **Expected Turn Time:** {end_time.strftime('%I:%M %p')}")
        st.write(f"**Queue Mood:** {queue_mood(st.session_state.wait_time)}")

        if st.button("➡️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 : LIVE QUEUE =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Simulation")

    st.write(f"🙋 **Current Position:** {st.session_state.position}")
    st.write(f"✅ **People Served:** {st.session_state.served}")

    progress_bar = st.progress(0)
    queue_container = st.empty()

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

            progress_bar.progress((i + 1) / total)

            people_icons = "👤 " * remaining
            queue_container.markdown(
                f"<div class='queue-box'>{people_icons}</div>",
                unsafe_allow_html=True
            )

            if remaining > 15:
                st.warning("⚠️ **High waiting detected – some users may leave**")
            else:
                st.info("✅ **Queue moving smoothly**")

            if remaining == 3:
                st.warning("🔔 **Your turn is coming next!**")

            time.sleep(1)

        st.success("🎉 **Service Completed Successfully!**")

    # ✅ WORKING QR CODE
    st.subheader("📱 Scan for Live Queue Status")
    qr_data = f"Live Queue | Position: {st.session_state.position} | Wait: {st.session_state.wait_time} mins"
    st.qr_code(qr_data)

    if st.button("➡️ Smart Recommendations"):
        st.session_state.page = 3
        st.rerun()

# ================= PAGE 3 : SMART RECOMMENDATIONS =================
elif st.session_state.page == 3:
    st.title("💡 Smart AI Recommendations")

    st.markdown("### 🔥 **INTELLIGENT QUEUE ACTIONS**")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/942/942748.png",
        width=90
    )
    st.markdown("**🟢 Dynamic Counter Scaling**  \nAutomatically open new counters when queue exceeds threshold.")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
        width=90
    )
    st.markdown("**⏰ Optimal Visit Prediction**  \nAI suggests low-crowd time slots to users.")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/595/595067.png",
        width=90
    )
    st.markdown("**🚦 Join / Avoid Guidance**  \nReal-time decision support before entering queue.")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",
        width=90
    )
    st.markdown("**👴 Priority Queue Allocation**  \nElderly & emergency users handled faster.")

    if st.button("➡️ Download Report"):
        st.session_state.page = 4
        st.rerun()

# ================= PAGE 4 : REPORT =================
elif st.session_state.page == 4:
    st.title("📄 Queue Report")

    report = f"""
SMART QUEUE MANAGEMENT REPORT
----------------------------

People Ahead: {st.session_state.people_ahead}
Staff Count: {st.session_state.staff}
Service Time: {st.session_state.service_time} mins
Arrival Rate: {st.session_state.arrival_rate} people/min

Predicted Waiting Time: {st.session_state.wait_time} minutes

AI FEATURES:
- One-time live simulation
- Digital queue twin
- QR-based live tracking
- Smart AI recommendations

STATUS: Queue completed successfully
"""

    st.download_button("📥 Download Report", report, file_name="queue_report.txt")

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
