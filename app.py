import streamlit as st

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
.main {
    background: linear-gradient(to bottom right, #e3f2fd, #ffffff);
    padding: 20px;
    border-radius: 10px;
}
h1, h2, h3 {
    color: #0d47a1;
}
.card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = 1

# ---------------- FUNCTIONS ----------------
def predict_wait_time(people, service_time, staff, peak):
    peak_factor = 1.5 if peak else 1.0
    wait_time = (people * service_time) / staff
    return round(wait_time * peak_factor, 2)

def queue_mood(wait_time):
    if wait_time <= 15:
        return "🟢 Low Crowd", "green"
    elif wait_time <= 30:
        return "🟡 Medium Crowd", "orange"
    else:
        return "🔴 Heavy Crowd", "red"

# ---------------- PAGE 1 : INPUT ----------------
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Waiting Time Predictor")

    st.markdown("### 📝 Enter Queue Details")

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        people = st.slider("👥 People Ahead", 0, 100, 20)
        service_time = st.slider("⏱ Average Service Time (minutes)", 1, 10, 5)
        staff = st.slider("👨‍💼 Number of Staff", 1, 10, 3)
        arrival_rate = st.slider("📈 Arrival Rate (people / 10 mins)", 1, 15, 5)
        peak = st.checkbox("🚨 Peak Hour")

        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Predict Waiting Time ➡️"):
        st.session_state.people = people
        st.session_state.service_time = service_time
        st.session_state.staff = staff
        st.session_state.arrival_rate = arrival_rate
        st.session_state.peak = peak
        st.session_state.wait_time = predict_wait_time(people, service_time, staff, peak)
        st.session_state.page = 2
        st.rerun()

# ---------------- PAGE 2 : RESULT ----------------
elif st.session_state.page == 2:
    st.title("📊 Prediction Result")

    wait_time = st.session_state.wait_time
    mood, color = queue_mood(wait_time)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("⏳ Predicted Waiting Time", f"{wait_time} minutes")
    st.markdown(f"### {mood}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🧠 Why is the waiting time high?")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"""
    • 👥 People ahead: {st.session_state.people}  
    • 👨‍💼 Staff available: {st.session_state.staff}  
    • ⏱ Service time: {st.session_state.service_time} mins  
    • 🚨 Peak hour: {'Yes' if st.session_state.peak else 'No'}
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 1
            st.rerun()
    with col2:
        if st.button("⚙️ Optimize & Suggestions ➡️"):
            st.session_state.page = 3
            st.rerun()

# ---------------- PAGE 3 : OPTIMIZATION ----------------
elif st.session_state.page == 3:
    st.title("💡 Smart Optimization Suggestions")

    improved_staff = st.session_state.staff + 1
    improved_time = predict_wait_time(
        st.session_state.people,
        st.session_state.service_time,
        improved_staff,
        st.session_state.peak
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"""
    👨‍💼 **Suggestion:** Add **1 more staff**  
    ⏳ Old Waiting Time: **{st.session_state.wait_time} mins**  
    ✅ New Waiting Time: **{improved_time} mins**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    best_time = "2:30 PM – 4:00 PM" if st.session_state.peak else "Any non-peak hour"

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"🕒 **Best Time to Visit:** {best_time}")
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.page = 2
            st.rerun()
    with col2:
        if st.button("🔄 What-If Simulation ➡️"):
            st.session_state.page = 4
            st.rerun()

# ---------------- PAGE 4 : SIMULATION ----------------
elif st.session_state.page == 4:
    st.title("🔄 What-If Simulation")

    sim_staff = st.slider("👨‍💼 Change Staff Count", 1, 10, st.session_state.staff)
    sim_service = st.slider("⏱ Change Service Time", 1, 10, st.session_state.service_time)

    sim_time = predict_wait_time(
        st.session_state.people,
        sim_service,
        sim_staff,
        st.session_state.peak
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"""
    📊 **Simulation Result**  
    👨‍💼 Staff: {sim_staff}  
    ⏱ Service Time: {sim_service} mins  
    ⏳ New Waiting Time: **{sim_time} mins**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🏠 Back to Home"):
        st.session_state.page = 1
        st.rerun()
