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
# Tabs
# -----------------------------
tab1, tab2 = st.tabs(["Predict Waiting Time", "Advanced Features / Next Page"])

# -----------------------------
# WAITING TIME FUNCTION
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
# PAGE 1
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

        st.session_state["result"] = result
        st.session_state["inputs"] = locals()

        st.success(f"⏱ Estimated Waiting Time: **{result} minutes**")

        st.markdown("**Factors Used:**")
        for k, v in factors.items():
            st.write(f"- {k.replace('_',' ').title()} = {v}")

# -----------------------------
# PAGE 2 – ADVANCED
# -----------------------------
with tab2:
    st.subheader("Advanced Features & Smart Decisions")

    if "result" not in st.session_state:
        st.info("Please predict waiting time first.")
    else:
        result = st.session_state["result"]
        inputs = st.session_state["inputs"]

        # -----------------------------
        # VISUAL
        # -----------------------------
        st.progress(min(result / 120, 1.0))
        st.metric("Waiting Time Visual", f"{result} min")

        # -----------------------------
        # STATUS MESSAGE
        # -----------------------------
        if result < 15:
            st.success("🟢 Queue moving fast – almost no wait.")
        elif result < 45:
            st.info("🟡 Queue is moving steadily.")
        else:
            st.warning("🔴 Queue is slow – expect delay.")

        # -----------------------------
        # 🆕 QUEUE MOVEMENT OPERATION (UNIQUE)
        # -----------------------------
        st.subheader("🔄 Live Queue Movement Impact")

        served_people = max(1, inputs["staff_count"])
        reduced_time = round(result - (served_people * inputs["avg_service_time"] * 0.5), 2)
        reduced_time = max(0, reduced_time)

        st.write(f"👥 **People Served Recently:** {served_people}")
        st.write(f"⏬ **Updated Waiting Time:** {reduced_time} minutes")

        if reduced_time < result:
            st.success("✅ Queue is moving! Your waiting time has reduced automatically.")
        else:
            st.warning("⚠️ Queue movement is slow.")

        # -----------------------------
        # SMART DECISIONS
        # -----------------------------
        st.subheader("🧠 Smart Decisions")

        if inputs["staff_count"] < 3:
            st.info("➕ Add more staff to speed up queue movement.")
        if inputs["arrival_rate"] > 8:
            st.info("🚨 High arrival rate – expect congestion.")
        if inputs["peak_hour"]:
            st.info("⏰ Peak hour detected – delays are normal.")

        # -----------------------------
        # SCENARIO SIMULATION
        # -----------------------------
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

        df = pd.DataFrame({
            "Staff Count": staff_range,
            "Waiting Time": sim_times
        }).set_index("Staff Count")

        st.line_chart(df)

        # -----------------------------
        # DOWNLOAD
        # -----------------------------
        download_df = pd.DataFrame([{
            "Initial Waiting Time": result,
            "Updated Waiting Time (Queue Moving)": reduced_time,
            "Staff Count": inputs["staff_count"],
            "Arrival Rate": inputs["arrival_rate"]
        }])

        st.download_button(
            "📥 Download Prediction",
            download_df.to_csv(index=False),
            "queue_prediction.csv"
        )

        st.success("✅ Smart queue analysis completed.")
