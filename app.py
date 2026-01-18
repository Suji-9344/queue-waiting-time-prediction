import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Smart Queue Waiting Time Predictor",
    page_icon="⏱",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
body {background-color: #f0f8ff;}
h1,h2,h3 {color: #0d47a1;}
.card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.scroll-box {
    max-height: 300px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

# -----------------------------
# WAITING TIME FUNCTION
# -----------------------------
def calculate_waiting_time(people_ahead, avg_service_time, staff_count, staff_experience,
                           priority_ratio, arrival_rate, service_complexity,
                           system_status, peak_hour):
    experience_factor = {1: 1.2, 2: 1.0, 3: 0.8}[staff_experience]
    system_factor = {0: 1.0, 1: 1.3, 2: 1.6}[system_status]
    peak_factor = 1.25 if peak_hour == 1 else 1.0

    experience_factor *= np.random.uniform(0.95, 1.05)
    system_factor *= np.random.uniform(0.95, 1.05)
    peak_factor *= np.random.uniform(0.95, 1.05)

    base_time = (people_ahead * avg_service_time) / max(1, staff_count)
    noise = np.random.normal(0, base_time * 0.1)

    waiting_time = (
        base_time * experience_factor * system_factor * peak_factor
        + (priority_ratio * 10)
        + (arrival_rate * 1.5)
        + (service_complexity * 2)
        + noise
    )

    waiting_time = max(0, round(waiting_time, 2))
    factors = {
        "base_time": round(base_time, 2),
        "experience_factor": round(experience_factor, 2),
        "system_factor": round(system_factor, 2),
        "peak_factor": round(peak_factor, 2),
        "noise": round(noise, 2)
    }
    return waiting_time, factors

# -----------------------------
# QUEUE MOOD FUNCTION
# -----------------------------
def queue_mood(wait_time):
    if wait_time <= 15:
        return "🟢 Queue moving fast – almost no wait", "green"
    elif wait_time <= 45:
        return "🟡 Queue is moving steadily", "orange"
    else:
        return "🔴 Queue is slow – expect delay", "red"

# -----------------------------
# PAGE 1: INPUT
# -----------------------------
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Waiting Time Predictor")
    st.subheader("📝 Enter Queue Details")

    people_ahead = st.number_input("👥 People Ahead", 0, 50, 10, 1)
    avg_service_time = st.number_input("⏱ Average Service Time (minutes)", 2, 10, 5, 1)
    staff_count = st.number_input("👨‍💼 Number of Staff", 1, 6, 2, 1)

    staff_experience = st.selectbox(
        "Staff Experience",
        [("New", 1), ("Experienced", 2), ("Expert", 3)],
        format_func=lambda x: x[0]
    )[1]

    priority_ratio = st.number_input("Priority Ratio (0.0 - 0.5)", 0.0, 0.5, 0.2, 0.01)
    arrival_rate = st.number_input("📈 Arrival Rate (people per 10 min)", 0, 12, 5, 1)
    service_complexity = st.number_input("Service Complexity", 1, 4, 3, 1)

    system_status = st.selectbox(
        "System Status",
        [("Normal", 0), ("Slow", 1), ("Down", 2)],
        format_func=lambda x: x[0]
    )[1]

    peak_hour = st.selectbox(
        "Peak Hour",
        [("No", 0), ("Yes", 1)],
        format_func=lambda x: x[0]
    )[1]

    if st.button("🔍 Predict Waiting Time ➡️"):
        result, factors = calculate_waiting_time(
            people_ahead, avg_service_time, staff_count, staff_experience,
            priority_ratio, arrival_rate, service_complexity, system_status, peak_hour
        )
        # STORE ONLY NEEDED VALUES IN SESSION STATE
        st.session_state.result = result
        st.session_state.factors = factors
        st.session_state.inputs = {
            "people_ahead": people_ahead,
            "avg_service_time": avg_service_time,
            "staff_count": staff_count,
            "staff_experience": staff_experience,
            "priority_ratio": priority_ratio,
            "arrival_rate": arrival_rate,
            "service_complexity": service_complexity,
            "system_status": system_status,
            "peak_hour": peak_hour
        }
        st.session_state.page = 2
        st.experimental_rerun()

# -----------------------------
# PAGE 2: RESULTS
# -----------------------------
elif st.session_state.page == 2:
    st.title("📊 Queue Analysis & Smart Decisions")

    result = st.session_state.result
    factors = st.session_state.factors
    inputs = st.session_state.inputs

    # Scrollable output
    st.subheader("⏱ Waiting Time Result")
    st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
    st.write(f"**Estimated Waiting Time:** {result} minutes")
    st.markdown("**Factors:**")
    for k, v in factors.items():
        st.write(f"- {k.replace('_',' ').title()} = {v}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Queue Mood
    mood_text, mood_color = queue_mood(result)
    st.markdown(f"**Status:** <span style='color:{mood_color};font-weight:bold'>{mood_text}</span>", unsafe_allow_html=True)

    # Live Queue Movement
    st.subheader("🔄 Live Queue Movement")
    served_people = max(1, inputs["staff_count"])
    reduced_time = round(result - (served_people * inputs["avg_service_time"] * 0.5), 2)
    reduced_time = max(0, reduced_time)
    st.write(f"👥 People Served Recently: {served_people}")
    st.write(f"⏬ Updated Waiting Time: {reduced_time} minutes")
    if reduced_time < result:
        st.success("✅ Queue is moving! Your waiting time has reduced automatically.")
    else:
        st.warning("⚠️ Queue movement is slow.")

    # Smart Decisions
    st.subheader("🧠 Smart Suggestions")
    if inputs["staff_count"] < 3:
        st.info("➕ Add more staff to speed up queue movement")
    if inputs["arrival_rate"] > 8:
        st.info("🚨 High arrival rate – expect congestion")
    if inputs["peak_hour"]:
        st.info("⏰ Peak hour detected – delays are normal")

    # Scenario Simulation
    st.subheader("📊 Scenario Simulation – Staff Count")
    staff_range = range(1, 7)
    sim_times = [
        calculate_waiting_time(
            inputs["people_ahead"], inputs["avg_service_time"], s,
            inputs["staff_experience"], inputs["priority_ratio"],
            inputs["arrival_rate"], inputs["service_complexity"],
            inputs["system_status"], inputs["peak_hour"]
        )[0]
        for s in staff_range
    ]
    df = pd.DataFrame({"Staff Count": staff_range, "Waiting Time": sim_times}).set_index("Staff Count")
    st.line_chart(df)

    # Best visiting time
    st.subheader("🕒 Best Time to Visit")
    best_time = "2:30 PM – 4:00 PM" if inputs["peak_hour"] else "Any non-peak hour"
    st.success(f"Recommended visiting time: {best_time}")

    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.experimental_rerun()
    with col2:
        if st.button("🔄 Next / What-If Simulation"):
            st.session_state.page = 3
            st.experimental_rerun()

# -----------------------------
# PAGE 3: WHAT-IF SIMULATION
# -----------------------------
elif st.session_state.page == 3:
    st.title("🔄 What-If Simulation")

    inputs = st.session_state.inputs
    sim_staff = st.slider("👨‍💼 Change Staff Count", 1, 6, inputs["staff_count"])
    sim_service = st.slider("⏱ Change Service Time (minutes)", 1, 10, inputs["avg_service_time"])

    sim_time = calculate_waiting_time(
        inputs["people_ahead"], sim_service, sim_staff,
        inputs["staff_experience"], inputs["priority_ratio"],
        inputs["arrival_rate"], inputs["service_complexity"],
        inputs["system_status"], inputs["peak_hour"]
    )[0]

    st.subheader("📊 Simulation Result")
    st.write(f"Staff Count: {sim_staff}")
    st.write(f"Service Time: {sim_service} minutes")
    st.write(f"Predicted Waiting Time: {sim_time} minutes")

    # Navigation Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 2
            st.experimental_rerun()
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 1
            st.experimental_rerun()
