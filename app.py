import streamlit as st
import numpy as np
import time
from datetime import datetime, timedelta
import pandas as pd
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Waiting Time Predictor",
    page_icon="🚦",
    layout="centered"
)

# ---------------- STYLE (Mobile Friendly) ----------------
st.markdown("""
<style>
.card {
    background:white;
    padding:15px;
    border-radius:12px;
    box-shadow:0px 2px 10px rgba(0,0,0,0.15);
    margin-bottom:12px;
}
.alert {
    background:#fff3cd;
    padding:10px;
    border-radius:8px;
    font-weight:bold;
}
.done {
    background:#d1e7dd;
    padding:12px;
    border-radius:8px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION INIT ----------------
if "page" not in st.session_state:
    st.session_state.page = 1

# ---------------- FUNCTIONS ----------------
def calculate_waiting_time(people, service, staff, exp, system, peak):
    exp_f = {"New": 1.2, "Experienced": 1.0, "Expert": 0.85}[exp]
    sys_f = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[system]
    peak_f = 1.25 if peak else 1.0

    base = (people * service) / max(1, staff)
    noise = np.random.normal(0, base * 0.1)
    wait = base * exp_f * sys_f * peak_f + noise

    return round(max(wait, 0), 2), base, exp_f, sys_f, peak_f, noise

def queue_mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd"
    elif wait <= 30:
        return "🟡 Medium Crowd"
    else:
        return "🔴 Heavy Crowd"

# ---------------- PAGE 1: PREDICT ----------------
if st.session_state.page == 1:
    st.title("🚦 Queue Waiting Time Predictor")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    people = st.number_input("👥 People Ahead", 0, 50, 15)
    service = st.number_input("⏱ Service Time (minutes)", 2, 10, 5)
    staff = st.number_input("👨‍💼 Staff Count", 1, 5, 2)
    exp = st.selectbox("🎓 Staff Experience", ["New", "Experienced", "Expert"])
    system = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])
    peak = st.selectbox("🚨 Peak Hour", ["No", "Yes"]) == "Yes"
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Predict Waiting Time"):
        wait, base, ef, sf, pf, noise = calculate_waiting_time(
            people, service, staff, exp, system, peak
        )

        st.session_state.wait = wait
        st.session_state.people = people
        st.session_state.staff = staff
        st.session_state.service = service
        st.session_state.exp = exp
        st.session_state.system = system
        st.session_state.peak = peak

        finish = datetime.now() + timedelta(minutes=wait)

        st.success(f"⏱ Estimated Waiting Time: **{wait} minutes**")
        st.write(f"🕒 Expected Service Time: **{finish.strftime('%I:%M %p')}**")
        st.write(f"Queue Mood: **{queue_mood(wait)}**")

        st.subheader("Factors Used")
        st.write(f"• Base Time = {round(base,2)}")
        st.write(f"• Experience Factor = {round(ef,2)}")
        st.write(f"• System Factor = {round(sf,2)}")
        st.write(f"• Peak Factor = {round(pf,2)}")
        st.write(f"• Noise = {round(noise,2)}")

        if st.button("🔄 Go to Live Queue"):
            st.session_state.page = 2
            st.rerun()

# ---------------- PAGE 2: LIVE QUEUE ----------------
elif st.session_state.page == 2:
    st.title("🔄 Live Queue Simulation")

    position = st.session_state.people
    served = 0
    box = st.empty()
    bar = st.progress(0)

    while position > 0:
        time.sleep(1.5)
        served += 1
        position -= 1

        remaining_wait = round((position * st.session_state.service) / st.session_state.staff, 2)

        alert = ""
        if position == 2:
            alert = "🔔 Your turn is coming soon!"
        if position == 0:
            alert = "✅ Your work is completed!"

        box.markdown(f"""
        <div class="card">
        👥 Remaining People: <b>{position}</b><br>
        ✅ Served People: <b>{served}</b><br>
        ⏱ Remaining Wait: <b>{remaining_wait} minutes</b><br>
        {f'<div class="alert">{alert}</div>' if alert else ''}
        </div>
        """, unsafe_allow_html=True)

        bar.progress(int(((served) / (served + position)) * 100))

    if st.button("💡 Smart Suggestions"):
        st.session_state.page = 3
        st.rerun()

# ---------------- PAGE 3: SMART SUGGESTIONS ----------------
elif st.session_state.page == 3:
    st.title("💡 Smart Suggestions")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("❗ Delay Reasons Detected")
    if st.session_state.people > 20:
        st.write("👥 High number of people")
    if st.session_state.exp == "New":
        st.write("🎓 Less experienced staff")
    if st.session_state.system != "Normal":
        st.write("🖥 System issues")
    if st.session_state.peak:
        st.write("🚨 Peak hour traffic")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("🕒 Best Time to Visit")
    st.write("2:30 PM – 4:00 PM (Low traffic)")
    st.markdown('</div>', unsafe_allow_html=True)

    # Peak Heat Map (Simulated)
    st.subheader("📊 Peak Hour Heat Map")
    hours = ["9AM", "11AM", "1PM", "3PM", "5PM"]
    traffic = [random.randint(10, 50) for _ in hours]
    st.bar_chart(pd.DataFrame({"Traffic": traffic}, index=hours))

    if st.button("📄 Download Report"):
        st.session_state.page = 4
        st.rerun()

# ---------------- PAGE 4: REPORT ----------------
elif st.session_state.page == 4:
    st.title("📄 Download Report")

    report_df = pd.DataFrame({
        "Metric": ["People Ahead", "Staff", "Service Time", "Estimated Wait"],
        "Value": [
            st.session_state.people,
            st.session_state.staff,
            st.session_state.service,
            st.session_state.wait
        ]
    })

    st.dataframe(report_df)
    st.line_chart(report_df.set_index("Metric"))

    report_text = f"""
QUEUE WAITING TIME REPORT
------------------------
Estimated Waiting Time: {st.session_state.wait} minutes
Generated At: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}
"""

    st.download_button(
        "⬇ Download Report",
        report_text,
        file_name="queue_report.txt"
    )

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
