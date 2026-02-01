import streamlit as st
import time
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Predictor & Live Tracker",
    page_icon="🚦",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("🚦 Smart Queue Predictor & Live Tracker")

# ---------------- INPUTS ----------------
people_ahead = st.slider("👥 People Ahead of You", 0, 50, 9)
staff_count = st.slider("🧑‍💼 Staff Count", 1, 10, 2)
avg_service_time = st.slider("⏱ Average Service Time (mins)", 1, 20, 5)
arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 10, 5)

staff_experience = st.selectbox("🎓 Staff Ex…
[8:26 AM, 2/1/2026] Suji🥰: pdf_file = generate_pdf()
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Queue Report (PDF)",
            data=f,
            file_name="Smart_Queue_Report.pdf",
            mime="application/pdf"
        )
[8:32 AM, 2/1/2026] Suji🥰: import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Predictor & Live Tracker",
    page_icon="🚦",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("🚦 Smart Queue Predictor & Live Tracker")

# ---------------- INPUT SECTION ----------------
people_ahead = st.slider("👥 People Ahead of You", 0, 50, 9)
staff_count = st.slider("🧑‍💼 Staff Count", 1, 10, 2)
avg_service_time = st.slider("⏱ Average Service Time (mins)", 1, 20, 5)
arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 10, 5)

staff_experience = st.selectbox("🎓 Staff Experience", ["New", "Intermediate", "Experienced"])
system_status = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
peak_hour = st.checkbox("🚨 Peak Hour")

# ---------------- FACTORS ----------------
experience_factor = {
    "New": 1.2,
    "Intermediate": 1.0,
    "Experienced": 0.8
}

system_factor = {
    "Normal": 1.0,
    "Slow": 1.3,
    "Down": 1.6
}

# ---------------- PREDICT WAIT TIME ----------------
if st.button("🔍 Predict Waiting Time"):
    service_time = avg_service_time * experience_factor[staff_experience]
    service_time *= system_factor[system_status]

    estimated_wait = (people_ahead / staff_count) * service_time
    if peak_hour:
        estimated_wait *= 1.4

    turn_time = datetime.now() + timedelta(minutes=estimated_wait)

    st.success(f"⏳ Estimated Waiting Time: {estimated_wait:.1f} minutes")
    st.info(f"🕒 Expected Turn Time: {turn_time.strftime('%I:%M %p')}")

    if estimated_wait < 30:
        st.success("🟢 Queue Mood: Light Crowd")
    elif estimated_wait < 60:
        st.warning("🟠 Queue Mood: Moderate Crowd")
    else:
        st.error("🔴 Queue Mood: Heavy Crowd")

# ---------------- LIVE QUEUE TRACKER ----------------
st.markdown("---")
st.subheader("📍 Live Queue Status")

st.write(f"👤 Your Current Position: {people_ahead}")
st.write("✅ People Served: 0")

progress = st.progress(0)
icons = "👤 " * min(people_ahead, 10)
st.markdown(icons)

if st.button("▶ Start Simulation"):
    for i in range(people_ahead):
        time.sleep(0.3)
        progress.progress(int(((i + 1) / people_ahead) * 100))
    st.success("✅ Queue Updated")

st.info("ℹ Explainable AI: Queue changed due to arrival/service rate adjustment")
st.success("✅ Good time to join queue now")

# ---------------- RECOMMENDED ACTIONS ----------------
st.markdown("---")
st.header("⭐ Recommended Actions")

st.write("🟢 Dynamic Counter Opening: Add staff if queue > 15")
st.write("🕓 Best Time to Visit: 4:00 PM – 6:00 PM")
st.write("⚠ Join when queue < 12, avoid otherwise")
st.write("🔧 Staff Reallocation: Move staff to busy counters")
st.write("⭐ Priority Queue for seniors & emergencies")

# ---------------- DOWNLOAD REPORT ----------------
st.markdown("---")

report = f"""
SMART QUEUE SYSTEM REPORT
------------------------
People Ahead       : {people_ahead}
Staff Count        : {staff_count}
Avg Service Time   : {avg_service_time} mins
Arrival Rate       : {arrival_rate} people/min
Staff Experience   : {staff_experience}
System Status      : {system_status}
Peak Hour          : {'Yes' if peak_hour else 'No'}

Generated on       : {datetime.now().strftime('%d-%m-%Y %I:%M %p')}
"""

st.download_button(
    label="⬇ Download Report",
    data=report,
    file_name="Smart_Queue_Report.txt",
    mime="text/plain"
)
