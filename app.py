import streamlit as st
import numpy as np
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Smart Queue Predictor",
    page_icon="⏱",
    layout="centered"
)

# -----------------------------
# CSS STYLING
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
    max-height: 250px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = 1
if "inputs" not in st.session_state:
    st.session_state.inputs = {}
if "result" not in st.session_state:
    st.session_state.result = 0
if "factors" not in st.session_state:
    st.session_state.factors = {}

# -----------------------------
# WAITING TIME FUNCTION
# -----------------------------
def calculate_waiting_time(people_ahead, avg_service_time, staff_count, staff_exp,
                           priority_ratio, arrival_rate, service_complexity,
                           system_status, peak_hour):
    exp_factor = {1: 1.2, 2: 1.0, 3: 0.8}[staff_exp]
    sys_factor = {0: 1.0, 1: 1.3, 2: 1.6}[system_status]
    peak_factor = 1.25 if peak_hour else 1.0

    exp_factor *= np.random.uniform(0.95, 1.05)
    sys_factor *= np.random.uniform(0.95, 1.05)
    peak_factor *= np.random.uniform(0.95, 1.05)

    base_time = (people_ahead * avg_service_time) / max(1, staff_count)
    noise = np.random.normal(0, base_time*0.1)

    wait_time = base_time * exp_factor * sys_factor * peak_factor + \
                (priority_ratio*10) + (arrival_rate*1.5) + (service_complexity*2) + noise
    wait_time = max(0, round(wait_time,2))

    factors = {
        "Base Time": round(base_time,2),
        "Experience Factor": round(exp_factor,2),
        "System Factor": round(sys_factor,2),
        "Peak Factor": round(peak_factor,2),
        "Random Noise": round(noise,2)
    }
    return wait_time, factors

# -----------------------------
# QUEUE MOOD
# -----------------------------
def queue_mood(wait_time):
    if wait_time <= 15: return "🟢 Fast – almost no wait", "green"
    elif wait_time <= 45: return "🟡 Moderate wait", "orange"
    else: return "🔴 Heavy queue – expect delay", "red"

# -----------------------------
# FRONT PAGE
# -----------------------------
if st.session_state.page == 1:
    st.title("🚦 Queue Waiting Time Predictor")
    st.markdown("""
    **How it works:**  
    1. Enter number of people ahead, staff, and service details.  
    2. System calculates **estimated waiting time** using simulation.  
    3. You get a **queue mood**, smart suggestions, and live updates.
    """)

    with st.form("input_form"):
        people_ahead = st.number_input("👥 People Ahead", 0, 50, 10, 1)
        avg_service_time = st.number_input("⏱ Avg Service Time (minutes)", 2, 10, 5, 1)
        staff_count = st.number_input("👨‍💼 Number of Staff", 1, 6, 2, 1)
        staff_exp = st.selectbox("Staff Experience", ["New","Experienced","Expert"], 0)
        staff_exp_map = {"New":1,"Experienced":2,"Expert":3}[staff_exp]

        priority_ratio = st.number_input("Priority Ratio (0.0 - 0.5)", 0.0, 0.5, 0.2, 0.01)
        arrival_rate = st.number_input("📈 Arrival Rate per 10 min", 0, 12, 5, 1)
        service_complexity = st.number_input("Service Complexity (1-4)", 1, 4, 3, 1)
        system_status = st.selectbox("System Status", ["Normal","Slow","Down"], 0)
        system_status_map = {"Normal":0,"Slow":1,"Down":2}[system_status]
        peak_hour = st.selectbox("Peak Hour", ["No","Yes"], 0)
        peak_hour_map = 1 if peak_hour=="Yes" else 0

        submitted = st.form_submit_button("🔍 Predict Waiting Time ➡️")
        if submitted:
            result, factors = calculate_waiting_time(
                people_ahead, avg_service_time, staff_count, staff_exp_map,
                priority_ratio, arrival_rate, service_complexity, system_status_map, peak_hour_map
            )
            st.session_state.inputs = {
                "people_ahead": people_ahead,
                "avg_service_time": avg_service_time,
                "staff_count": staff_count,
                "staff_exp": staff_exp_map,
                "priority_ratio": priority_ratio,
                "arrival_rate": arrival_rate,
                "service_complexity": service_complexity,
                "system_status": system_status_map,
                "peak_hour": peak_hour_map
            }
            st.session_state.result = result
            st.session_state.factors = factors
            st.session_state.page = 2

# -----------------------------
# RESULTS PAGE
# -----------------------------
elif st.session_state.page == 2:
    st.title("📊 Queue Analysis & Smart Suggestions")
    result = st.session_state.result
    factors = st.session_state.factors
    inputs = st.session_state.inputs

    # Scrollable factors
    st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
    st.write(f"⏱ **Estimated Waiting Time:** {result} minutes")
    st.write("**Factors considered:**")
    for k,v in factors.items():
        st.write(f"- {k}: {v}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Queue mood
    mood, color = queue_mood(result)
    st.markdown(f"**Status:** <span style='color:{color};font-weight:bold'>{mood}</span>", unsafe_allow_html=True)

    # Live queue movement
    st.subheader("🔄 Live Queue Movement")
    reduced_time = max(0, round(result - (inputs["staff_count"] * inputs["avg_service_time"] * 0.5),2))
    st.write(f"👥 People Served Recently: {inputs['staff_count']}")
    st.write(f"⏬ Updated Waiting Time: {reduced_time} minutes")
    if reduced_time < result: st.success("✅ Queue is moving, waiting time reduced!")
    else: st.warning("⚠️ Queue moving slowly")

    # Scenario simulation
    st.subheader("📊 Staff Count Simulation")
    staff_range = range(1,7)
    sim_times = [
        calculate_waiting_time(
            inputs["people_ahead"], inputs["avg_service_time"], s,
            inputs["staff_exp"], inputs["priority_ratio"], inputs["arrival_rate"],
            inputs["service_complexity"], inputs["system_status"], inputs["peak_hour"]
        )[0] for s in staff_range
    ]
    df = pd.DataFrame({"Staff Count": staff_range, "Waiting Time": sim_times}).set_index("Staff Count")
    st.line_chart(df)

    # Best time to visit
    best_time = "2:30 PM – 4:00 PM" if inputs["peak_hour"] else "Any non-peak hour"
    st.success(f"🕒 Recommended Time to Visit: {best_time}")

    # Navigation buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
    with col2:
        if st.button("🔄 Next / Simulation"):
            st.session_state.page = 3

# -----------------------------
# WHAT-IF SIMULATION PAGE
# -----------------------------
elif st.session_state.page == 3:
    st.title("🔄 What-If Simulation")
    inputs = st.session_state.inputs
    sim_staff = st.slider("👨‍💼 Staff Count", 1,6, inputs["staff_count"])
    sim_service = st.slider("⏱ Service Time (minutes)", 1,10, inputs["avg_service_time"])

    sim_time = calculate_waiting_time(
        inputs["people_ahead"], sim_service, sim_staff,
        inputs["staff_exp"], inputs["priority_ratio"], inputs["arrival_rate"],
        inputs["service_complexity"], inputs["system_status"], inputs["peak_hour"]
    )[0]

    st.subheader("📊 Simulation Result")
    st.write(f"Staff: {sim_staff}")
    st.write(f"Service Time: {sim_service} min")
    st.write(f"Predicted Waiting Time: {sim_time} min")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 2
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 1
