import streamlit as st
import pandas as pd
import altair as alt
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Waiting Time Predictor",
    page_icon="⏱",
    layout="centered"
)

# ---------------- SESSION STATE DEFAULTS ----------------
defaults = {
    "page": 1,
    "people": 20,
    "service_time": 5,
    "staff": 3,
    "staff_exp": "Average",
    "system_status": "Normal",
    "arrival_rate": 5,
    "peak": False,
    "wait_time": 0
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right,#e3f2fd,#ffffff);
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 15px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}
.mood-green {color:#2e7d32;}
.mood-orange {color:#ff8f00;}
.mood-red {color:#c62828;}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def predict_wait_time(p, s, stf, peak, exp, sys):
    peak_f = 1.5 if peak else 1
    exp_f = {"New":1.2,"Average":1,"Expert":0.8}[exp]
    sys_f = {"Normal":1,"Slow":1.3,"Down":1.6}[sys]
    return round((p * s * exp_f / stf) * peak_f * sys_f, 2)

def mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd 😎","mood-green"
    elif wait <= 30:
        return "🟡 Medium Crowd 😐","mood-orange"
    else:
        return "🔴 Heavy Crowd 😫","mood-red"

def expected_time(wait):
    return (datetime.now() + timedelta(minutes=wait)).strftime("%I:%M %p")

# ---------------- PAGE 1 : INPUT ----------------
if st.session_state.page == 1:
    st.title("🚦 Smart Queue Waiting Time Predictor")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.session_state.people = st.slider("👥 People Ahead",0,100,st.session_state.people)
    st.session_state.service_time = st.slider("⏱ Service Time (mins)",1,10,st.session_state.service_time)
    st.session_state.staff = st.slider("👨‍💼 Staff Count",1,10,st.session_state.staff)

    st.session_state.staff_exp = st.selectbox("🎓 Staff Experience",
        ["New","Average","Expert"],
        index=["New","Average","Expert"].index(st.session_state.staff_exp)
    )

    st.session_state.system_status = st.selectbox("🖥 System Status",
        ["Normal","Slow","Down"],
        index=["Normal","Slow","Down"].index(st.session_state.system_status)
    )

    st.session_state.arrival_rate = st.slider("📈 Arrival Rate /10 mins",1,15,st.session_state.arrival_rate)
    st.session_state.peak = st.checkbox("🚨 Peak Hour",st.session_state.peak)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔍 Predict"):
        st.session_state.wait_time = predict_wait_time(
            st.session_state.people,
            st.session_state.service_time,
            st.session_state.staff,
            st.session_state.peak,
            st.session_state.staff_exp,
            st.session_state.system_status
        )
        st.session_state.page = 2
        st.rerun()

# ---------------- PAGE 2 : LIVE RESULT ----------------
elif st.session_state.page == 2:
    st.title("📊 Live Queue Status")

    mood_txt, mood_class = mood(st.session_state.wait_time)

    st.markdown(f"""
    <div class="card">
        <h2>⏳ Waiting Time: {st.session_state.wait_time} mins</h2>
        <h3 class="{mood_class}">{mood_txt}</h3>
        <p>🕒 Expected Service Time: {expected_time(st.session_state.wait_time)}</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Live Progress Bar ----------
    st.markdown("### 🔄 Live Waiting Progress")
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)

    # ---------- Queue Movement Simulation ----------
    st.markdown("### 👥 Queue Movement")
    q = st.session_state.people
    placeholder = st.empty()
    for i in range(5):
        q = max(0, q - st.session_state.staff)
        placeholder.info(f"People Remaining in Queue: {q}")
        time.sleep(0.4)

    # ---------- Delay Reason ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("### ❗ Delay Reasons")
    if st.session_state.system_status != "Normal":
        st.write("🖥 System issues increasing delay")
    if st.session_state.staff_exp == "New":
        st.write("🎓 New staff handling time slower")
    if st.session_state.peak:
        st.write("🚨 Peak hour crowd surge")
    st.markdown('</div>', unsafe_allow_html=True)

    col1,col2 = st.columns(2)
    if col1.button("⬅️ Back"):
        st.session_state.page = 1
        st.rerun()
    if col2.button("⚙️ Smart Suggestions"):
        st.session_state.page = 3
        st.rerun()

# ---------------- PAGE 3 : SMART INSIGHTS ----------------
elif st.session_state.page == 3:
    st.title("💡 Smart Insights & Suggestions")

    improved_time = predict_wait_time(
        st.session_state.people,
        st.session_state.service_time,
        st.session_state.staff + 1,
        False,
        "Expert",
        "Normal"
    )

    best_time = "2:30 PM – 4:00 PM" if st.session_state.peak else "Any non-peak hour"

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"""
    ✅ **Smart Suggestions**
    - 👨‍💼 Add one more staff
    - 🎓 Assign expert staff
    - 🖥 Fix system delays
    - 🕒 Visit during non-peak hours

    ⏳ Current: {st.session_state.wait_time} mins  
    🚀 Optimized: {improved_time} mins  
    🕒 Best Time to Visit: **{best_time}**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    if improved_time < 15:
        st.balloons()

    if st.button("📊 Visual Analytics"):
        st.session_state.page = 4
        st.rerun()

# ---------------- PAGE 4 : VISUAL ANALYTICS ----------------
elif st.session_state.page == 4:
    st.title("📊 Queue Analytics Dashboard")

    df = pd.DataFrame({
        "Time Slot":["10m","20m","30m","40m","50m","60m"],
        "Queue Size":[st.session_state.people + i*st.session_state.arrival_rate for i in range(1,7)],
        "Waiting Time":[st.session_state.wait_time + i*2 for i in range(6)]
    })

    st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x="Time Slot",
            y="Queue Size",
            color="Waiting Time"
        ),
        use_container_width=True
    )

    if st.button("🏠 Home"):
        st.session_state.page = 1
        st.rerun()
