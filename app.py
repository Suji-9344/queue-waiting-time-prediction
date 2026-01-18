import streamlit as st
import time
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Real-Time Queue Waiting Time Predictor",
    page_icon="⏱",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
defaults = {
    "people": 20,
    "staff": 3,
    "service_time": 5,
    "staff_exp": "Average",
    "system_status": "Normal",
    "arrival_rate": 2,
    "served": 0,
    "running": False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- CSS ----------------
st.markdown("""
<style>
body {background: linear-gradient(to bottom right,#e3f2fd,#ffffff);}
.card {
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:2px 2px 12px rgba(0,0,0,0.15);
    margin-bottom:15px;
}
.green{color:#2e7d32;}
.orange{color:#ff8f00;}
.red{color:#c62828;}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def exp_factor(exp):
    return {"New":0.8,"Average":1.0,"Expert":1.3}[exp]

def system_factor(sys):
    return {"Normal":1.0,"Slow":1.3,"Down":1.6}[sys]

def predict_wait(queue):
    base = (queue * st.session_state.service_time) / st.session_state.staff
    return round(base * system_factor(st.session_state.system_status), 2)

def mood(wait):
    if wait <= 15:
        return "🟢 Low Crowd","green"
    elif wait <= 30:
        return "🟡 Medium Crowd","orange"
    else:
        return "🔴 Heavy Crowd","red"

# ---------------- INPUT UI ----------------
st.title("🚦 Real-Time Queue Waiting Time Predictor")

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.session_state.people = st.slider("👥 Current Queue Size",1,100,st.session_state.people)
    st.session_state.staff = st.slider("👨‍💼 Staff Available",1,10,st.session_state.staff)
    st.session_state.service_time = st.slider("⏱ Service Time (mins)",1,10,st.session_state.service_time)

    st.session_state.staff_exp = st.selectbox(
        "🎓 Staff Experience",
        ["New","Average","Expert"],
        index=["New","Average","Expert"].index(st.session_state.staff_exp)
    )

    st.session_state.system_status = st.selectbox(
        "🖥 System Status",
        ["Normal","Slow","Down"],
        index=["Normal","Slow","Down"].index(st.session_state.system_status)
    )

    st.session_state.arrival_rate = st.slider("📈 New Arrivals / min",0,5,st.session_state.arrival_rate)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- CONTROLS ----------------
col1,col2 = st.columns(2)
if col1.button("▶ Start Live Queue"):
    st.session_state.running = True
if col2.button("⏹ Stop"):
    st.session_state.running = False

# ---------------- LIVE QUEUE ----------------
if st.session_state.running:
    box = st.empty()
    bar = st.progress(0)

    for i in range(30):
        served_now = int(st.session_state.staff * exp_factor(st.session_state.staff_exp))
        arrived_now = st.session_state.arrival_rate

        st.session_state.people = max(0, st.session_state.people - served_now + arrived_now)
        st.session_state.served += served_now

        wait = predict_wait(st.session_state.people)
        mood_txt, mood_col = mood(wait)

        bar.progress((i+1)*3)

        box.markdown(f"""
        <div class="card">
            <h3>⏳ Live Waiting Time: {wait} mins</h3>
            <h4 class="{mood_col}">{mood_txt}</h4>
            👥 Queue Remaining: <b>{st.session_state.people}</b><br>
            ✅ People Served: <b>{st.session_state.served}</b><br>
            🕒 Expected Service: {(datetime.now()+timedelta(minutes=wait)).strftime("%I:%M %p")}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1)

# ---------------- DELAY REASON ----------------
st.markdown("### ❗ Delay Reason")
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.system_status != "Normal":
        st.write("🖥 System slowdown increasing service time")
    if st.session_state.staff_exp == "New":
        st.write("🎓 New staff handling customers slowly")
    if st.session_state.people > 30:
        st.write("👥 High crowd volume")
    if st.session_state.arrival_rate > 2:
        st.write("📈 High arrival rate")

    if (
        st.session_state.system_status == "Normal"
        and st.session_state.staff_exp == "Expert"
        and st.session_state.people < 15
    ):
        st.write("✅ Queue running efficiently")

    st.markdown('</div>', unsafe_allow_html=True)
