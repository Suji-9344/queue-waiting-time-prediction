import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Queue Waiting Time Predictor", layout="centered")
st.title("🚦 Queue Waiting Time Predictor")
st.write("Predict queue waiting time using real-life simulation formula.")

# -----------------------------
# USER INPUT
# -----------------------------
st.sidebar.header("Input Parameters")

people_ahead = st.sidebar.slider("People Ahead", 0, 50, 10)
avg_service_time = st.sidebar.slider("Average Service Time (minutes)", 2, 10, 5)
staff_count = st.sidebar.slider("Number of Staff", 1, 6, 2)

staff_experience = st.sidebar.selectbox(
    "Staff Experience",
    [1, 2, 3],
    format_func=lambda x: {1: "New", 2: "Experienced", 3: "Expert"}[x]
)

priority_ratio = st.sidebar.slider("Priority Ratio", 0.0, 0.5, 0.2)
arrival_rate = st.sidebar.slider("Arrival Rate (people per 10 min)", 0, 12, 5)
service_complexity = st.sidebar.slider("Service Complexity", 1, 4, 3)

system_status = st.sidebar.selectbox(
    "System Status",
    [0, 1, 2],
    format_func=lambda x: {0: "Normal", 1: "Slow", 2: "Down"}[x]
)

peak_hour = st.sidebar.selectbox(
    "Peak Hour",
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

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
