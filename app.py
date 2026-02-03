import streamlit as st
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Smart Queue Management System",
    page_icon="⏱",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #FFD700;
    text-align: center;
}

.card {
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    padding: 20px;
    border-radius: 15px;
    color: white;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

.highlight {
    color: #00FFD1;
    font-weight: bold;
}

.alert-card {
    background: linear-gradient(135deg, #ff512f, #dd2476);
    padding: 20px;
    border-radius: 15px;
    color: white;
    font-weight: bold;
}

.success-card {
    background: linear-gradient(135deg, #11998e, #38ef7d);
    padding: 20px;
    border-radius: 15px;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="main-title">SMART QUEUE MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)
st.write("")

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "⏳ Predict Waiting Time",
    "📱 Live Queue QR",
    "💡 Suggestions",
    "🚨 Priority & Alerts"
])

# ==================================================
# TAB 1 – WAIT TIME PREDICTION
# ==================================================
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Enter Queue Details")

    people_ahead = st.number_input("People Ahead", min_value=0, value=10)
    service_time = st.number_input("Service Time per Person (minutes)", min_value=1, value=5)

    if st.button("Predict Waiting Time"):
        waiting_minutes = people_ahead * service_time
        current_time = datetime.now()
        expected_time = current_time + timedelta(minutes=waiting_minutes)

        st.markdown(f"""
        <p class="highlight">Estimated Waiting Time: {waiting_minutes} minutes</p>
        <p class="highlight">Expected Turn Time: {expected_time.strftime("%I:%M %p")}</p>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# TAB 2 – LIVE QR CODE
# ==================================================
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Live Queue Status QR Code")

    qr_data = "Live Queue Status: ACTIVE | People in Queue"
    qr = qrcode.make(qr_data)

    buffer = BytesIO()
    qr.save(buffer)
    st.image(buffer.getvalue(), width=250)

    st.success("Scan this QR code to view live queue status")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# TAB 3 – SUGGESTIONS
# ==================================================
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Smart Suggestions")

    col1, col2 = st.columns(2)

    with col1:
        st.image("suggestion1.png", use_container_width=True)
        st.markdown("✔ Visit during **non-peak hours**")

    with col2:
        st.image("suggestion2.png", use_container_width=True)
        st.markdown("✔ Use **QR check-in** to save time")

    st.info("AI suggests visiting early morning or late afternoon for faster service")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# TAB 4 – PRIORITY & ALERTS
# ==================================================
with tab4:
    st.markdown('<div class="alert-card">', unsafe_allow_html=True)

    st.subheader("🚨 Crowd Alerts")
    st.image("alert.png", width=120)
    st.write("⚠ Heavy Crowd Incoming!")
    st.write("⚠ Delay Expected")

    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")

    st.markdown('<div class="success-card">', unsafe_allow_html=True)

    st.subheader("⭐ Priority Queue")
    st.image("priority.png", width=120)
    st.write("✔ Senior Citizens")
    st.write("✔ Emergency Patients")
    st.write("✔ Disabled Access")

    st.markdown('</div>', unsafe_allow_html=True)
