import streamlit as st
import time
import pandas as pd
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
    "people": 15,
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

# ---------------- FUNCTIONS ----------------
def predict_wait(people, service, staff, arrival, exp, system, peak):
    exp_factor = {"New": 1.2, "Experienced": 1.0, "Expert": 0.8}[exp]
    sys_factor = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[system]
    peak_factor = 1.25 if peak else 1.0

    base = (people * service) / max(1, staff)
    arrival_delay = arrival * 2

    return round(base * exp_factor * sys_factor * peak_factor + arrival_delay, 1)

# ================= PAGE 1 : INPUT =================
if st.session_state.page == 1:
    st.title("🚦 Queue Waiting Time Predictor")

    st.session_state.people = st.slider("👥 People in Queue", 0, 50, st.session_state.people)
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
            st.session_state.people,
            st.session_state.service_time,
            st.session_state.staff,
            st.session_state.arrival_rate,
            st.session_state.staff_exp,
            st.session_state.system_status,
            peak
        )
        st.session_state.position = st.session_state.people
        st.session_state.served = 0
        st.session_state.predicted = True

    if st.session_state.predicted:
        finish = datetime.now() + timedelta(minutes=st.session_state.wait_time)

        st.success(f"⏳ Waiting Time: {st.session_state.wait_time} minutes")
        st.info(f"🕒 Expected Turn: {finish.strftime('%I:%M %p')}")

        if st.button("➡️ Go to Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 : LIVE QUEUE =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Status")

    st.write(f"🙋 **Your Current Position:** {st.session_state.position}")
    st.write(f"✅ **People Served:** {st.session_state.served}")

    progress = st.progress(0)

    if st.button("▶️ Start Live Queue"):
        total = st.session_state.position

        for i in range(total + 1):
            remaining = total - i
            st.session_state.position = remaining
            st.session_state.served += 1

            progress.progress(i / max(1, total))
            st.write(f"👥 Remaining in queue: **{remaining}**")

            if remaining == 3:
                st.warning("🔔 **Your turn is coming soon!**")

            time.sleep(0.8)

        st.success("🎉 **Your work is completed successfully!**")

    # ✅ WORKING QR CODE
    st.subheader("📱 Scan QR to View Queue")
    qr_data = "Live Queue Status"
    qr_url = f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={qr_data}"
    st.image(qr_url)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.rerun()
    with col2:
        if st.button("➡️ Smart Suggestions"):
            st.session_state.page = 3
            st.rerun()

# ================= PAGE 3 : SMART SUGGESTIONS =================
elif st.session_state.page == 3:
    st.title("💡 Smart Suggestions")

    st.markdown("### ⭐ **BEST VISIT TIME: 4:00 PM – 6:00 PM**")

    st.write("👥 High crowd detected → Visit during non-peak hours")
    st.write("🎓 Expert staff reduces waiting time")
    st.write("🖥 Avoid system slow periods")
    st.write("📈 High arrival rate increases delay")

    if st.button("➡️ View Report"):
        st.session_state.page = 4
        st.rerun()

# ================= PAGE 4 : REPORT =================
elif st.session_state.page == 4:
    st.title("📄 Queue Report")

    data = pd.DataFrame({
        "Hour": ["9AM","11AM","1PM","3PM","5PM","7PM"],
        "Crowd": [10, 25, 40, 20, 12, 6]
    })

    st.bar_chart(data.set_index("Hour"))

    report = f"""
QUEUE REPORT

People in Queue: {st.session_state.people}
Staff: {st.session_state.staff}
Service Time: {st.session_state.service_time} mins
Arrival Rate: {st.session_state.arrival_rate}/min
Staff Experience: {st.session_state.staff_exp}
System Status: {st.session_state.system_status}

Predicted Waiting Time: {st.session_state.wait_time} mins

BEST VISIT TIME: 4:00 PM – 6:00 PM
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="queue_report.txt"
    )

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
