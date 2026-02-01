[8:32 AM, 2/1/2026] Suji🥰: import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Predictor & Live Tracker",
    page_icon="🚦",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("🚦 Smart Queue Predictor & Live Tracker")

# ---------------- INPUT SECTION ----------------
people_ahead = st.slider("👥 People Ahead of You", 0, 50, 9)
staff_count = st.slider("🧑‍💼 Staff Count", 1, 10, 2)
avg_service_time = st.slider("⏱ Average Service Time (mins)", 1, 20, 5)
arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 10, 5)

staff_experience = st.selectbox("🎓 Staff Experience", ["New", "Intermediate", "Experienced"])
system_status = st.selectbo…
[8:36 AM, 2/1/2026] Suji🥰: import streamlit as st
import time
import random
from datetime import datetime, timedelta

---------------- PAGE CONFIG ----------------

st.set_page_config(
page_title="Smart Queue System",
page_icon="⏱",
layout="centered"
)

---------------- CUSTOM CSS ----------------

st.markdown("""

<style>  
body {  
    background-color: #f4f9ff;  
    font-family: 'Arial', sans-serif;  
}  
.queue-box {  
    border: 2px solid #0073e6;  
    padding: 15px;  
    border-radius: 10px;  
    background-color: #ffffff;  
    margin-bottom: 10px;  
}  
</style>  """, unsafe_allow_html=True)

---------------- SESSION STATE ----------------

defaults = {
"page": 1,
"people_ahead": 10,
"staff": 2,
"service_time": 5,
"arrival_rate": 1,
"staff_exp": "Experienced",
"system_status": "Normal",
"peak": False,
"wait_time": 0,
"position": 0,
"served": 0,
"predicted": False
}
for k, v in defaults.items():
if k not in st.session_state:
st.session_state[k] = v

---------------- ML-LIKE WAIT TIME PREDICTION ----------------

def predict_wait(p, s, staff, arr, exp, sys, peak):
exp_w = {"New": 1.2, "Experienced": 1.0, "Expert": 0.8}[exp]
sys_w = {"Normal": 1.0, "Slow": 1.3, "Down": 1.6}[sys]
peak_w = 1.25 if peak else 1.0
base = (p * s) / max(1, staff)
arrival_effect = arr * 2
return round(base * exp_w * sys_w * peak_w + arrival_effect, 1)

---------------- QUEUE MOOD ----------------

def queue_mood(wait):
if wait <= 15:
return "🟢 Low Crowd"
elif wait <= 30:
return "🟡 Medium Crowd"
else:
return "🔴 Heavy Crowd"

================= PAGE 1 : INPUT =================

if st.session_state.page == 1:
st.title("🚦 Smart Queue Predictor & Live Tracker")

st.session_state.people_ahead = st.slider("👥 People Ahead of You", 0, 50, st.session_state.people_ahead)  
st.session_state.staff = st.slider("👨‍💼 Staff Count", 1, 5, st.session_state.staff)  
st.session_state.service_time = st.slider("⏱ Average Service Time (mins)", 2, 10, st.session_state.service_time)  
st.session_state.arrival_rate = st.slider("📈 Arrival Rate (people/min)", 0, 5, st.session_state.arrival_rate)  

st.session_state.staff_exp = st.selectbox("🎓 Staff Experience", ["New", "Experienced", "Expert"])  
st.session_state.system_status = st.selectbox("🖥 System Status", ["Normal", "Slow", "Down"])  
st.session_state.peak = st.checkbox("🚨 Peak Hour")  

if st.button("🔍 Predict Waiting Time"):  
    st.session_state.wait_time = predict_wait(  
        st.session_state.people_ahead,  
        st.session_state.service_time,  
        st.session_state.staff,  
        st.session_state.arrival_rate,  
        st.session_state.staff_exp,  
        st.session_state.system_status,  
        st.session_state.peak  
    )  
    st.session_state.position = st.session_state.people_ahead  
    st.session_state.served = 0  
    st.session_state.predicted = True  

if st.session_state.predicted:  
    end_time = datetime.now() + timedelta(minutes=st.session_state.wait_time)  
    st.success(f"⏳ Estimated Waiting Time: {st.session_state.wait_time} minutes")  
    st.info(f"🕒 Expected Turn Time: {end_time.strftime('%I:%M %p')}")  
    st.write(f"Queue Mood: {queue_mood(st.session_state.wait_time)}")  

    if st.button("➡️ Start Live Queue"):  
        st.session_state.page = 2  
        st.rerun()

================= PAGE 2 : LIVE QUEUE =================

elif st.session_state.page == 2:
st.title("🔄 Live Queue Simulation")

st.write(f"🙋 *Your Current Position:* {st.session_state.position}")  
st.write(f"✅ *People Served:* {st.session_state.served}")  
progress_bar = st.progress(0)  
queue_container = st.empty()  

if st.button("▶️ Start Simulation"):  
    total = st.session_state.position  
    for i in range(total + 1):  
        remaining = total - i  
        st.session_state.position = remaining  
        st.session_state.served += 1  

        # Progress  
        progress_bar.progress(i / max(1, total))  
          
        # Digital Twin  
        people_icons = "👤 " * remaining  
        queue_container.markdown(f"<div class='queue-box'>{peo
