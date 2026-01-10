import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Queue Waiting Time Predictor", layout="centered")
st.title("🚦 Queue Waiting Time Predictor")
st.write("Predict queue waiting time using Machine Learning")

# -----------------------------
# PATH HANDLING
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_PATH = os.path.join(MODEL_DIR, "queue_model.pkl")
DATA_PATH = os.path.join(DATA_DIR, "queue_waiting_time_formula_guided_1000.csv")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# FUNCTION: GENERATE DATASET IF MISSING
# -----------------------------
def generate_dataset(file_path, n=1000):
    data = []
    for _ in range(n):
        people_ahead = np.random.randint(0, 50)
        avg_service_time = np.random.randint(2, 10)
        staff_count = np.random.randint(1, 6)
        staff_experience = np.random.randint(1, 3)
        priority_ratio = round(np.random.uniform(0, 0.5), 2)
        arrival_rate = np.random.randint(0, 12)
        service_complexity = np.random.randint(1, 4)
        system_status = np.random.randint(0, 2)
        peak_hour = np.random.randint(0, 1)

        experience_factor = {1: 1.2, 2: 1.0, 3: 0.8}[staff_experience]
        system_factor = {0: 1.0, 1: 1.3, 2: 1.6}[system_status]
        peak_factor = 1.25 if peak_hour == 1 else 1.0

        base_time = (people_ahead * avg_service_time) / max(1, staff_count)
        waiting_time = (
            base_time * experience_factor * system_factor * peak_factor
            + (priority_ratio * 10)
            + (arrival_rate * 1.5)
            + (service_complexity * 2)
        )
        waiting_time += np.random.normal(0, 4)
        waiting_time = max(0, round(waiting_time, 2))

        data.append([
            people_ahead, avg_service_time, staff_count, staff_experience,
            priority_ratio, arrival_rate, service_complexity,
            system_status, peak_hour, waiting_time
        ])
    columns = [
        "people_ahead","avg_service_time","staff_count","staff_experience",
        "priority_ratio","arrival_rate","service_complexity",
        "system_status","peak_hour","waiting_time"
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_path, index=False)
    return df

# -----------------------------
# LOAD OR GENERATE DATA
# -----------------------------
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = generate_dataset(DATA_PATH)

# -----------------------------
# TRAIN OR LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    X = df.drop("waiting_time", axis=1)
    y = df["waiting_time"]

    model = RandomForestRegressor(n_estimators=300, random_state=42)
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

model = load_model()

# -----------------------------
# USER INPUT
# -----------------------------
st.sidebar.header("Input Parameters")

people_ahead = st.sidebar.slider("People Ahead", 0, 50, 10)
avg_service_time = st.sidebar.slider("Average Service Time (minutes)", 2, 10, 5)
staff_count = st.sidebar.slider("Number of Staff", 1, 6, 2)

staff_experience = st.sidebar.selectbox(
    "Staff Experience",
    [1, 2, 3],
    format_func=lambda x: {1: "New", 2: "Experienced", 3: "Expert"}[x]
)

priority_ratio = st.sidebar.slider("Priority Ratio", 0.0, 0.5, 0.2)
arrival_rate = st.sidebar.slider("Arrival Rate (people per 10 min)", 0, 12, 5)
service_complexity = st.sidebar.slider("Service Complexity", 1, 4, 3)

system_status = st.sidebar.selectbox(
    "System Status",
    [0, 1, 2],
    format_func=lambda x: {0: "Normal", 1: "Slow", 2: "Down"}[x]
)

peak_hour = st.sidebar.selectbox(
    "Peak Hour",
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

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

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Waiting Time"):
    prediction = model.predict(input_data)
    st.success(f"⏱ Estimated Waiting Time: **{round(prediction[0],2)} minutes**")
