# app.py
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Waiting Time Predictor",
    page_icon="⏱",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background-color: #f4f9ff;
}
.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = 1

# ---------------- FUNCTIONS ----------------
def predict_wait_time(people, service_time, staff, peak, staff_exp, system_status):
    # Peak hour factor
    peak_factor = 1.5 if peak else 1.0

    # Staff experience factor
    exp_factor = {
        "New": 1.2,
        "Average": 1.0,
        "Expert": 0.8
    }[staff_exp]

    # System status factor
    system_factor = {
        "Normal": 1.0,
        "Slow": 1.3,
        "Down": 1.6
    }[system_status]

    wait_time = (people * service_time * exp_factor) / staff
    final_time = wait_time * peak_factor * system_factor
    return round(final_time, 2)

def queue_mood(wait_time):
    if wait_time <= 15:
        return "🟢 Low Crowd 😎", "green"
    elif wait_time <= 30:
        return "🟡 Medium Crowd 😐", "orange"
    else:
        return "🔴 Heavy Crowd 😫", "red"

def expected_time(wait_time):
    return (datetime.now() + timedelta(minutes=wait_time)).strftime("%I:%M %p")

# ---------------- PAGE 1 : INPUT ----------------
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Waiting Time Predictor")
    st.markdown("### 📝 Enter Queue Details")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    people = st.slider("👥 People Ahead", 0, 100, 20)
    service_time = st.slider("⏱ Average Service Time (minutes)", 1, 10, 5)
    staff = st.slider("👨‍💼 Number of Staff", 1, 10, 3)

    staff_exp = st.selectbox(
        "🎓 Staff Experience",
        ["New", "Average", "Expert"]
    )

    system_status = st.selectbox(
        "🖥 System Status",
        ["Normal", "Slow", "Down"]
    )

    arrival_rate = st.slider("📈 Arrival Rate (people / 10 mins)", 1, 15, 5)
    peak = st.checkbox("🚨 Peak Hour")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Predict Waiting Time ➡️"):
        st.session_state.people = people
        st.session_state.service_time = service_time
        st.session_state.staff = staff
        st.session_state.staff_exp = staff_exp
        st.session_state.system_status = system_status
        st.session_state.arrival_rate = arrival_rate
        st.session_state.peak = peak

        st.session_state.wait_time = predict_wait_time(
            people, service_time, staff, peak, staff_exp, system_status
        )

        st.session_state.page = 2
        st.rerun()

# ---------------- PAGE 2 : RESULT ----------------
elif st.session_state.page == 2:
    st.title("📊 Prediction Result")

    wait_time = st.session_state.wait_time
    mood, color = queue_mood(wait_time)

    st.markdown(f"""
    <div class="card" style="background: linear-gradient(135deg,{color},#ffffff);">
        <h2>⏳ Waiting Time: {wait_time} minutes</h2>
        <h3>{mood}</h3>
        <p>🕒 Expected Service Time: {expected_time(wait_time)}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Factors Affecting Queue")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"""
    👥 People Ahead: {st.session_state.people}  
    👨‍💼 Staff Count: {st.session_state.staff}  
    🎓 Staff Experience: {st.session_state.staff_exp}  
    🖥 System Status: {st.session_state.system_status}  
    🚨 Peak Hour: {'Yes' if st.session_state.peak else 'No'}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.rerun()
    with col2:
        if st.button("⚙️ Optimize ➡️"):
            st.session_state.page = 3
            st.rerun()

# ---------------- PAGE 3 : OPTIMIZATION ----------------
elif st.session_state.page == 3:
    st.title("💡 Smart Optimization")

    improved_staff = st.session_state.staff + 1
    improved_time = predict_wait_time(
        st.session_state.people,
        st.session_state.service_time,
        improved_staff,
        st.session_state.peak,
        "Expert",
        "Normal"
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"""
    ✅ **Suggestions**
    - Add 1 more staff  
    - Assign expert staff  
    - Maintain system in normal mode  

    ⏳ Old Time: **{st.session_state.wait_time} mins**  
    🚀 New Time: **{improved_time} mins**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    if improved_time < 15:
        st.balloons()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 2
            st.rerun()
    with col2:
        if st.button("🔄 Simulation ➡️"):
            st.session_state.page = 4
            st.rerun()

# ---------------- PAGE 4 : SIMULATION ----------------
elif st.session_state.page == 4:
    st.title("🔄 What-If Simulation")

    sim_staff = st.slider("👨‍💼 Staff Count", 1, 10, st.session_state.staff)
    sim_service = st.slider("⏱ Service Time", 1, 10, st.session_state.service_time)

    sim_time = predict_wait_time(
        st.session_state.people,
        sim_service,
        sim_staff,
        st.session_state.peak,
        st.session_state.staff_exp,
        st.session_state.system_status
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"""
    📊 Simulation Result  
    👨‍💼 Staff: {sim_staff}  
    ⏱ Service Time: {sim_service} mins  
    ⏳ Waiting Time: **{sim_time} mins**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    df = pd.DataFrame({
        "Time Slot": ["10m", "20m", "30m", "40m", "50m", "60m"],
        "Queue Size": [st.session_state.people + i*st.session_state.arrival_rate for i in range(1,7)]
    })

    st.altair_chart(
        alt.Chart(df).mark_line(point=True).encode(
            x="Time Slot",
            y="Queue Size"
        ),
        use_container_width=True
    )

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
