import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Live Queue System",
    page_icon="⏱",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
defaults = {
    "page": 1,
    "people_ahead": 10,
    "staff": 2,
    "service_time": 5,
    "arrival_rate": 1,
    "staff_exp": "Experienced",
    "system_status": "Normal",
    "wait_time": 0,
    "position": 0,
    "served": 0,
    "predicted": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- ML-LIKE PREDICTION ----------------
def predict_wait(p, s, staff, arr, exp, sys, peak):
    exp_w = {"New": 1.2, "Experienced": 1.0, "Expert": 0.8}[exp]
    sys_w = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]
    peak_w = 1.25 if peak else 1.0

    base = (p * s) / max(1, staff)
    arrival_effect = arr * 2

    return round(base * exp_w * sys_w * peak_w + arrival_effect, 1)

# ================= PAGE 1 : INPUT =================
if st.session_state.page == 1:
    st.title("🚦 Queue Waiting Time Predictor")

    st.session_state.people_ahead = st.slider(
        "👥 People Ahead of You", 0, 50, st.session_state.people_ahead
    )
    st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    st.session_state.service_time = st.slider("⏱ Service Time (mins)", 2, 10, st.session_state.service_time)
    st.session_state.arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 5, st.session_state.arrival_rate)

    st.session_state.staff_exp = st.selectbox(
        "🎓 Staff Experience", ["New", "Experienced", "Expert"]
    )
    st.session_state.system_status = st.selectbox(
        "🖥 System Status", ["Normal", "Slow", "Down"]
    )

    peak = st.checkbox("🚨 Peak Hour")

    if st.button("🔍 Predict Waiting Time"):
        st.session_state.wait_time = predict_wait(
            st.session_state.people_ahead,
            st.session_state.service_time,
            st.session_state.staff,
            st.session_state.arrival_rate,
            st.session_state.staff_exp,
            st.session_state.system_status,
            peak
        )
        st.session_state.position = st.session_state.people_ahead
        st.session_state.served = 0
        st.session_state.predicted = True

    if st.session_state.predicted:
        end_time = datetime.now() + timedelta(minutes=st.session_state.wait_time)
        st.success(f"⏳ Waiting Time: {st.session_state.wait_time} minutes")
        st.info(f"🕒 Expected Turn Time: {end_time.strftime('%I:%M %p')}")

        if st.button("➡️ Start Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 : LIVE QUEUE =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Movement")

    st.write(f"🙋 **Your Current Position:** {st.session_state.position}")
    st.write(f"✅ **People Served:** {st.session_state.served}")

    progress = st.progress(0)

    if st.button("▶️ Start Simulation"):
        total = st.session_state.position

        for i in range(total + 1):
            remaining = total - i
            st.session_state.position = remaining
            st.session_state.served += 1

            progress.progress(i / max(1, total))
            st.write(f"👥 Remaining Ahead: **{remaining}**")

            if remaining == 3:
                st.warning("🔔 Your turn is coming soon!")
                st.info("🔊 Voice Alert: Your turn is coming in few minutes")

            time.sleep(1)

        st.success("🎉 Your work is completed!")

    # ---------------- QR CODE ----------------
    st.subheader("📱 Scan QR for Live Queue Status")
    qr_text = f"Position:{st.session_state.position}, Waiting:{st.session_state.wait_time} mins"
    qr_url = f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={qr_text}"
    st.image(qr_url)

    if st.button("➡️ Smart Suggestions"):
        st.session_state.page = 3
        st.rerun()

# ================= PAGE 3 : SMART SUGGESTIONS =================
elif st.session_state.page == 3:
    st.title("💡 Smart Suggestions")

    st.markdown("### ⭐ **BEST VISIT TIME: 4:00 PM – 6:00 PM**")
    st.write("👥 Avoid peak crowd times")
    st.write("🎓 Expert staff reduces delay")
    st.write("🖥 System slow increases waiting")
    st.write("📉 Visit during non-peak hours")

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
Staff Experience: {st.session_state.staff_exp}
System Status: {st.session_state.system_status}

Predicted Waiting Time: {st.session_state.wait_time} minutes

BEST VISIT TIME: 4:00 PM – 6:00 PM

STATUS: Queue completed successfully
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="queue_report.txt"
    )

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
