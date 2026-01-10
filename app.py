import streamlit as st
import pandas as pd
import joblib

# Load trained model
model = joblib.load("model/queue_model.pkl")

st.set_page_config(page_title="Queue Waiting Time Predictor", layout="centered")

st.title("🚦 Queue Waiting Time Predictor")
st.write("Predict estimated waiting time using Machine Learning")

st.sidebar.header("Input Parameters")

people_ahead = st.sidebar.slider("People Ahead in Queue", 0, 50, 10)
avg_service_time = st.sidebar.slider("Avg Service Time (minutes)", 2, 10, 5)
staff_count = st.sidebar.slider("Staff Count", 1, 6, 2)
staff_experience = st.sidebar.selectbox(
    "Staff Experience", [1, 2, 3],
    format_func=lambda x: {1: "New", 2: "Experienced", 3: "Expert"}[x]
)
priority_ratio = st.sidebar.slider("Priority Ratio", 0.0, 0.5, 0.2)
arrival_rate = st.sidebar.slider("Arrival Rate (per 10 min)", 0, 12, 5)
service_complexity = st.sidebar.slider("Service Complexity", 1, 4, 3)
system_status = st.sidebar.selectbox(
    "System Status", [0, 1, 2],
    format_func=lambda x: {0: "Normal", 1: "Slow", 2: "Down"}[x]
)
peak_hour = st.sidebar.selectbox("Peak Hour", [0, 1], format_func=lambda x: "Yes" if x else "No")

input_data = pd.DataFrame([{
    "people_ahead": people_ahead,
    "avg_service_time": avg_service_time,
    "staff_count": staff_count,
    "staff_experience": staff_experience,
    "priority_ratio": priority_ratio,
    "arrival_rate": arrival_rate,
    "service_complexity": service_complexity,
    "system_status": system_status,
    "peak_hour": peak_hour
}])

if st.button("Predict Waiting Time"):
    prediction = model.predict(input_data)
    st.success(f"⏱ Estimated Waiting Time: **{round(prediction[0], 2)} minutes**")
