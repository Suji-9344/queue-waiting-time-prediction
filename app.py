import streamlit as st
import numpy as np
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Queue Waiting Time Predictor",
    page_icon="⏱",
    layout="centered"
)

st.title("🚦 Queue Waiting Time Predictor")
st.write("Predict waiting time using real-life queue conditions")

# ---------------- FUNCTION ----------------
def calculate_waiting_time(people, avg_service, staff, experience, system, peak):
    exp_factor = {"New": 1.2, "Experienced": 1.0, "Expert": 0.85}[experience]
    sys_factor = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[system]
    peak_factor = 1.25 if pea…
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Queue Waiting Time Predictor",
    page_icon="⏱",
    layout="centered"
)

st.title("🚦 Queue Waiting Time Predictor")
st.write("Predict waiting time using real-life queue conditions")

# ---------------- FUNCTION ----------------
def calculate_waiting_time(people, avg_service, staff, experience, system, peak):
    exp_factor = {"New": 1.2, "Experienced": 1.0, "Expert": 0.85}[experience]
    sys_factor = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[system]
    peak_factor = 1.25 if peak else 1.0

    base_time = (people * avg_service) / max(1, staff)
    noise = np.random.normal(0, base_time * 0.1)

    waiting_time = base_time * exp_factor * sys_factor * peak_factor + noise
    waiting_time = max(0, round(waiting_time, 2))

    factors = {
        "Base Time": round(base_time, 2),
        "Experience Factor": round(exp_factor, 2),
        "System Factor": round(sys_factor, 2),
        "Peak Factor": round(peak_factor, 2),
        "Noise": round(noise, 2)
    }

    return waiting_time, factors

def detect_delay(people, experience, system, peak):
    reasons = []
    if people > 25:
        reasons.append("👥 High number of people in queue")
    if experience == "New":
        reasons.append("🎓 New or less experienced staff")
    if system != "Normal":
        reasons.append("🖥 System is slow or down")
    if peak:
        reasons.append("🚨 Peak hour traffic")
    return reasons

def best_visit_time(peak):
    return "2:30 PM – 4:00 PM" if peak else "Any non-peak hour (Morning/Afternoon)"

# ---------------- INPUTS ----------------
st.subheader("Input Parameters")

people = st.number_input("👥 People Ahead", 0, 50, 15)
avg_service = st.number_input("⏱ Average Service Time (minutes)", 2, 10, 5)
staff = st.number_input("👨‍💼 Number of Staff", 1, 6, 2)

experience = st.selectbox("🎓 Staff Experience", ["New", "Experienced", "Expert"])
system = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
peak = st.selectbox("🚨 Peak Hour", ["No", "Yes"]) == "Yes"

# ---------------- PREDICT ----------------
if st.button("Predict Waiting Time"):
    wait_time, factors = calculate_waiting_time(
        people, avg_service, staff, experience, system, peak
    )

    now = datetime.now()
    finish_time = now + timedelta(minutes=wait_time)

    st.success(f"⏱ Estimated Waiting Time: *{wait_time} minutes*")

    st.write("### ⏰ Time Details")
    st.write(f"🕒 Current Time: *{now.strftime('%I:%M %p')}*")
    st.write(f"✅ Expected Service Time: *{finish_time.strftime('%I:%M %p')}*")

    st.write("### 📊 Factors Used")
    for k, v in factors.items():
        st.write(f"• *{k}* = {v}")

    # ---------------- DELAY REASONS ----------------
    st.write("### ❗ Delay Reason Detection")
    reasons = detect_delay(people, experience, system, peak)
    if reasons:
        for r in reasons:
            st.write(f"- {r}")
    else:
        st.write("✅ No major delay detected")

    # ---------------- BEST TIME ----------------
    st.write("### 🕒 Best Time to Visit")
    st.info(best_visit_time(peak))

    # ---------------- LIVE QUEUE INFO ----------------
    st.write("### 🔄 Live Queue Status")
    st.write(f"🙋 Your position in queue: *{people}*")
    st.write(f"⏳ Approx waiting time remaining: *{wait_time} minutes*")

    # ---------------- PDF REPORT ----------------
    def generate_pdf():
        file_name = "queue_report.pdf"
        doc = SimpleDocTemplate(file_name)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("Queue Waiting Time Report", styles["Title"]))
        content.append(Paragraph(f"Estimated Waiting Time: {wait_time} minutes", styles["Normal"]))
        content.append(Paragraph(f"Current Time: {now.strftime('%I:%M %p')}", styles["Normal"]))
        content.append(Paragraph(f"Expected Service Time: {finish_time.strftime('%I:%M %p')}", styles["Normal"]))

        content.append(Paragraph("Factors Used:", styles["Heading2"]))
        for k, v in factors.items():
            content.append(Paragraph(f"{k}: {v}", styles["Normal"]))

        content.append(Paragraph("Delay Reasons:", styles["Heading2"]))
        if reasons:
            for r in reasons:
                content.append(Paragraph(r, styles["Normal"]))
        else:
            content.append(Paragraph("No major delay detected", styles["Normal"]))

        content.append(Paragraph(f"Best Time to Visit: {best_visit_time(peak)}", styles["Normal"]))

        doc.build(content)
        return file_name

    pdf_file = generate_pdf()

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Report (PDF)",
            data=f,
            file_name="Queue_Waiting_Time_Report.pdf",
            mime="application/pdf"
        )
