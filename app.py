import streamlit as st
import time
import pandas as pd
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Live Queue Waiting Time Predictor",
    page_icon="⏱",
    layout="centered"
)

# ---------------- SESSION STATE INIT ----------------
defaults = {
    "page": 1,
    "people": 15,
    "service_time": 5,
    "staff": 2,
    "experience": "Experienced",
    "system": "Normal",
    "peak": False,
    "wait_time": 0,
    "served": 0,
    "predicted": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- FUNCTIONS ----------------
def predict_wait():
    exp_factor = {"New": 1.3, "Experienced": 1.0, "Expert": 0.85}[st.session_state.experience]
    sys_factor = {"Normal": 1.0, "Slow": 1.4, "Down": 1.8}[st.session_state.system]
    peak_factor = 1.25 if st.session_state.peak else 1.0

    base = (st.session_state.people * st.session_state.service_time) / max(1, st.session_state.staff)
    return round(base * exp_factor * sys_factor * peak_factor, 1)

def delay_reasons():
    reasons = []
    if st.session_state.people > 20:
        reasons.append("👥 **High number of people**")
    if st.session_state.experience == "New":
        reasons.append("🎓 **New staff (low experience)**")
    if st.session_state.system != "Normal":
        reasons.append("🖥 **System slow or down**")
    if st.session_state.peak:
        reasons.append("🚨 **Peak hour traffic**")
    return reasons or ["✅ **Queue moving normally**"]

def queue_mood(wait):
    if wait < 10:
        return "🟢 **Low Crowd**"
    elif wait < 25:
        return "🟡 **Medium Crowd**"
    return "🔴 **Heavy Crowd**"

# ---------------- SIDEBAR ----------------
st.sidebar.title("📍 Navigation")
if st.sidebar.button("🏠 Predictor"):
    st.session_state.page = 1
if st.sidebar.button("🔄 Live Queue"):
    st.session_state.page = 2
if st.sidebar.button("💡 Smart Suggestions"):
    st.session_state.page = 3

# ================= PAGE 1 =================
if st.session_state.page == 1:
    st.title("🚦 Queue Waiting Time Predictor")

    st.session_state.people = st.slider("👥 People in Queue", 0, 50, st.session_state.people)
    st.session_state.service_time = st.slider("⏱ Avg Service Time (mins)", 2, 10, st.session_state.service_time)
    st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    st.session_state.experience = st.selectbox("🎓 Staff Experience", ["New", "Experienced", "Expert"])
    st.session_state.system = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
    st.session_state.peak = st.checkbox("🚨 Peak Hour")

    if st.button("🔍 Predict Waiting Time"):
        st.session_state.wait_time = predict_wait()
        st.session_state.predicted = True

    if st.session_state.predicted:
        finish = datetime.now() + timedelta(minutes=st.session_state.wait_time)

        st.success(f"⏳ **Predicted Waiting Time:** {st.session_state.wait_time} minutes")
        st.info(f"🕒 **Expected Turn Time:** {finish.strftime('%I:%M %p')}")
        st.write(f"😐 **Queue Mood:** {queue_mood(st.session_state.wait_time)}")

        st.subheader("❗ **Delay Reason Detection**")
        for r in delay_reasons():
            st.write(r)

# ================= PAGE 2 =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Simulation")

    total = st.session_state.people
    progress = st.progress(0)

    for i in range(total + 1):
        remaining = total - i
        served = st.session_state.served + i

        progress.progress(i / max(1, total))
        st.write(f"🙋 **People remaining:** {remaining}")
        st.write(f"✅ **People served:** {served}")

        if remaining == 3:
            st.warning("🔔 **Alert:** Your turn is coming soon!")

        time.sleep(0.6)

    st.success("🎉 **Your work is completed successfully!**")
    st.session_state.served += total
    st.session_state.people = 0

# ================= PAGE 3 =================
elif st.session_state.page == 3:
    st.title("💡 Smart Suggestions & Peak Analysis")

    st.subheader("⭐ **Smart Recommendations**")
    st.write("⏰ **Best Visiting Time:** 4:00 PM – 6:00 PM")
    st.write("👨‍💼 **Add one staff** during peak hours")
    st.write("🖥 **Avoid system downtime periods**")

    st.subheader("📊 **Peak Hour Crowd Pattern**")
    data = pd.DataFrame({
        "Hour": ["9AM","10AM","11AM","12PM","1PM","2PM","3PM","4PM","5PM","6PM"],
        "Crowd": [5,12,25,40,45,38,22,15,10,6]
    })
    st.bar_chart(data.set_index("Hour"))

    # ---------------- DOWNLOAD REPORT ----------------
    st.subheader("📥 Download Report")

    report = f"""
QUEUE WAITING TIME REPORT

People in Queue: {st.session_state.people}
Staff Count: {st.session_state.staff}
Service Time: {st.session_state.service_time} mins
Predicted Waiting Time: {st.session_state.wait_time} mins

Delay Reasons:
{', '.join(delay_reasons())}

Best Time to Visit: 4 PM - 6 PM
"""

    st.download_button(
        "📄 Download Queue Report",
        report,
        file_name="queue_waiting_time_report.txt"
    )
