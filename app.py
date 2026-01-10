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
# Tabs for pages
# -----------------------------
tab1, tab2 = st.tabs(["Predict Waiting Time", "Advanced Features / Next Page"])

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
# PAGE 1: INPUT + PREDICT
# -----------------------------
with tab1:
    st.subheader("Input Parameters")
    
    people_ahead = st.number_input("People Ahead", 0, 50, 10, 1)
    avg_service_time = st.number_input("Average Service Time (minutes)", 2, 10, 5, 1)
    staff_count = st.number_input("Number of Staff", 1, 6, 2, 1)
    
    staff_experience = st.selectbox(
        "Staff Experience",
        [("New", 1), ("Experienced", 2), ("Expert", 3)],
        format_func=lambda x: x[0]
    )[1]
    
    priority_ratio = st.number_input("Priority Ratio (0.0 - 0.5)", 0.0, 0.5, 0.2, 0.01)
    arrival_rate = st.number_input("Arrival Rate (people per 10 min)", 0, 12, 5, 1)
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
    
    if st.button("Predict Waiting Time"):
        result, factors = calculate_waiting_time(
            people_ahead, avg_service_time, staff_count, staff_experience,
            priority_ratio, arrival_rate, service_complexity, system_status, peak_hour
        )
        st.session_state["last_result"] = result
        st.session_state["last_factors"] = factors
        st.session_state["inputs"] = {
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

        # Show result
        st.success(f"⏱ Estimated Waiting Time: **{result} minutes**")
        st.markdown("**Factors used in calculation:**")
        st.markdown(f"- Base time = {factors['base_time']}")
        st.markdown(f"- Experience factor = {factors['experience_factor']}")
        st.markdown(f"- System factor = {factors['system_factor']}")
        st.markdown(f"- Peak hour factor = {factors['peak_factor']}")
        st.markdown(f"- Random noise = {factors['noise']}")

# -----------------------------
# PAGE 2: ADVANCED FEATURES / NEXT PAGE
# -----------------------------
with tab2:
    st.subheader("Advanced Features / Scenario Simulation")

    if "last_result" not in st.session_state:
        st.info("Please predict waiting time on Page 1 first.")
    else:
        result = st.session_state["last_result"]
        factors = st.session_state["last_factors"]
        inputs = st.session_state["inputs"]

        # 1️⃣ Color-coded message based on waiting time
        if result < 15:
            st.success("✅ Quick! You barely have to wait.")
        elif result < 45:
            st.info("⏳ Moderate wait expected.")
        elif result < 75:
            st.warning("⚠️ Consider preparing for a long wait.")
        else:
            st.error("🚨 Very long queue! Maybe come later.")

        # 2️⃣ Scenario simulation: Vary staff count
        staff_options = list(range(1, 7))
        sim_results = [
            calculate_waiting_time(
                inputs["people_ahead"], inputs["avg_service_time"], s, inputs["staff_experience"],
                inputs["priority_ratio"], inputs["arrival_rate"], inputs["service_complexity"],
                inputs["system_status"], inputs["peak_hour"]
            )[0] for s in staff_options
        ]
        sim_df = pd.DataFrame({"Staff Count": staff_options, "Predicted Waiting Time": sim_results})
        st.line_chart(sim_df.set_index("Staff Count"))
        st.markdown("**Scenario Simulation:** Changing staff count affects waiting time.")

        # 3️⃣ Priority recommendations
        if inputs["staff_count"] < 3:
            st.info("💡 Consider adding more staff to reduce waiting time.")
        if inputs["peak_hour"]:
            st.info("⚠️ It's peak hour, expect slightly longer waits.")
        if inputs["arrival_rate"] > 8:
            st.info("🚨 High arrival rate detected. Try online booking if available.")

        # 4️⃣ Downloadable prediction
        download_df = pd.DataFrame([{
            **inputs,
            "predicted_waiting_time": result
        }])
        st.download_button("Download Prediction", download_df.to_csv(index=False), "prediction.csv")
