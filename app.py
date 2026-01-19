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
if "page" not in st.session_state:
    st.session_state.page = 1

if "people" not in st.session_state:
    st.session_state.people = 15
    st.session_state.staff = 2
    st.session_state.service_time = 5
    st.session_state.wait_time = 0
    st.session_state.position = 0
    st.session_state.served = 0
    st.session_state.predicted = False

# ---------------- FUNCTIONS ----------------
def predict_wait(people, service, staff, peak):
    peak_factor = 1.25 if peak else 1.0
    return round((people * service / max(1, staff)) * peak_factor, 1)

def queue_mood(wait):
    if wait < 10:
        return "🟢 Low Crowd"
    elif wait < 25:
        return "🟡 Medium Crowd"
    return "🔴 Heavy Crowd"

# ================= PAGE 1 : PREDICT =================
if st.session_state.page == 1:
    st.title("🚦 Queue Waiting Time Predictor")

    people = st.slider("👥 People in Queue", 0, 50, st.session_state.people)
    service = st.slider("⏱ Avg Service Time (mins)", 2, 10, st.session_state.service_time)
    staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)
    peak = st.checkbox("🚨 Peak Hour")

    if st.button("🔍 Predict Waiting Time"):
        st.session_state.wait_time = predict_wait(people, service, staff, peak)
        st.session_state.people = people
        st.session_state.staff = staff
        st.session_state.service_time = service
        st.session_state.position = people
        st.session_state.served = 0
        st.session_state.predicted = True

    if st.session_state.predicted:
        finish = datetime.now() + timedelta(minutes=st.session_state.wait_time)

        st.success(f"⏳ **Waiting Time:** {st.session_state.wait_time} minutes")
        st.info(f"🕒 **Expected Turn Time:** {finish.strftime('%I:%M %p')}")
        st.write(f"😐 **Queue Mood:** {queue_mood(st.session_state.wait_time)}")

        if st.button("➡️ Go to Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ================= PAGE 2 : LIVE QUEUE =================
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Movement")

    st.write(f"🙋 **Your Current Position:** {st.session_state.position}")
    st.write(f"✅ **People Served:** {st.session_state.served}")

    progress = st.progress(0)
    start = st.button("▶️ Start Live Queue")

    if start:
        total = st.session_state.position
        for i in range(total + 1):
            remaining = total - i
            st.session_state.position = remaining
            st.session_state.served += 1

            progress.progress(i / max(1, total))
            st.write(f"👥 Remaining People: **{remaining}**")
            st.write(f"✅ Served: **{st.session_state.served}**")

            if remaining == 3:
                st.warning("🔔 **Alert: Your turn is coming soon!**")

            time.sleep(0.8)

        st.success("🎉 **Your work is completed successfully!**")

    # QR CODE (safe)
    st.subheader("📱 Scan QR to View Queue Live")
    qr_url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=LiveQueueStatus"
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

    st.markdown("### ⭐ **Best Visit Time:** **4:00 PM – 6:00 PM**")
    st.write("👨‍💼 Add extra staff during peak hours")
    st.write("📉 Visit during non-peak hours to reduce waiting")
    st.write("🖥 Avoid system slow periods")

    if st.button("➡️ View Graph & Download Report"):
        st.session_state.page = 4
        st.rerun()

    if st.button("⬅️ Back to Live Queue"):
        st.session_state.page = 2
        st.rerun()

# ================= PAGE 4 : GRAPH & REPORT =================
elif st.session_state.page == 4:
    st.title("📊 Peak Hour Analysis & Report")

    data = pd.DataFrame({
        "Hour": ["9AM","10AM","11AM","12PM","1PM","2PM","3PM","4PM","5PM","6PM"],
        "Crowd": [5,12,28,40,45,38,25,15,10,6]
    })
    st.bar_chart(data.set_index("Hour"))

    st.subheader("📥 Download Report")

    report = f"""
SMART QUEUE REPORT

People in Queue: {st.session_state.people}
Staff Count: {st.session_state.staff}
Service Time: {st.session_state.service_time} mins
Predicted Waiting Time: {st.session_state.wait_time} mins

BEST VISIT TIME: 4:00 PM – 6:00 PM

Status: Queue completed successfully
"""

    st.download_button(
        "📄 Download Queue Report",
        report,
        file_name="queue_report.txt"
    )

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
