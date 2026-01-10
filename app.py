import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Queue Waiting Time Predictor", layout="centered")
st.title("🚦 Queue Waiting Time Predictor")
st.write("Predict queue waiting time using real-life simulation formula.\nFill all inputs below and click Predict.")

# -----------------------------
# USER INPUTS ON MAIN PAGE
# -----------------------------
people_ahead = st.number_input("People Ahead", min_value=0, max_value=50, value=10, step=1)
avg_service_time = st.number_input("Average Service Time (minutes)", min_value=2, max_value=10, value=5, step=1)
staff_count = st.number_input("Number of Staff", min_value=1, max_value=6, value=2, step=1)

staff_experience = st.selectbox(
    "Staff Experience",
    [("New", 1), ("Experienced", 2), ("Expert", 3)],
    format_func=lambda x: x[0]
)[1]  # Get the numeric value

priority_ratio = st.number_input("Priority Ratio (0.0 - 0.5)", min_value=0.0, max_value=0.5, value=0.2, step=0.01)
arrival_rate = st.number_input("Arrival Rate (people per 10 min)", min_value=0, max_value=12, value=5, step=1)
service_complexity = st.number_input("Service Complexity", min_value=1, max_value=4, value=3, step=1)

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

# -----------------------------
# FUNCTION TO CALCULATE WAITING TIME (UNIQUE)
# -----------------------------
def calculate_waiting_time(
    people_ahead,
    avg_service_time,
    staff_count,
    staff_experience,
    priority_ratio,
    arrival_rate,
    service_complexity,
    system_status,
    peak_hour
):
    # Base factors
    experience_factor = {1: 1.2, 2: 1.0, 3: 0.8}[staff_experience]
    system_factor = {0: 1.0, 1: 1.3, 2: 1.6}[system_status]
    peak_factor = 1.25 if peak_hour == 1 else 1.0

    # Add small random variation to make output unique
    experience_factor *= np.random.uniform(0.95, 1.05)
    system_factor *= np.random.uniform(0.95, 1.05)
    peak_factor *= np.random.uniform(0.95, 1.05)

    # Base waiting time
    base_time = (people_ahead * avg_service_time) / max(1, staff_count)

    # Add randomness proportional to base_time
    noise = np.random.normal(0, base_time * 0.1)

    # Final waiting time formula
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
# BUTTON TO CALCULATE
# -----------------------------
if st.button("Predict Waiting Time"):
    result, factors = calculate_waiting_time(
        people_ahead,
        avg_service_time,
        staff_count,
        staff_experience,
        priority_ratio,
        arrival_rate,
        service_complexity,
        system_status,
        peak_hour
    )

    st.success(f"⏱ Estimated Waiting Time: **{result} minutes**")

    # Show factor breakdown
    st.markdown("**Factors used in calculation:**")
    st.markdown(f"- Base time = {factors['base_time']} (people ahead × avg service time / staff count)")
    st.markdown(f"- Experience factor = {factors['experience_factor']}")
    st.markdown(f"- System factor = {factors['system_factor']}")
    st.markdown(f"- Peak hour factor = {factors['peak_factor']}")
    st.markdown(f"- Priority impact = {priority_ratio*10}")
    st.markdown(f"- Arrival rate impact = {arrival_rate*1.5}")
    st.markdown(f"- Service complexity impact = {service_complexity*2}")
    st.markdown(f"- Random noise added = {factors['noise']} (for uniqueness)")
