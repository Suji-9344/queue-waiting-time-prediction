import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Queue Waiting Time Predictor", layout="centered")

st.title("🚦 Queue Waiting Time Predictor")
st.write("Predict queue waiting time using Machine Learning")

# -----------------------------
# SAFE PATH HANDLING
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")
MODEL_PATH = os.path.join(MODEL_DIR, "queue_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "data", "queue_waiting_time_formula_guided_1000.csv")

# -----------------------------
# LOAD OR TRAIN MODEL SAFELY
# -----------------------------
@st.cache_resource
def load_model():
    # If model exists → load
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    # Else → train model
    df = pd.read_csv(DATA_PATH)

    X = df.drop("waiting_time", axis=1)
    y = df["waiting_time"]

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )
    model.fit(X, y)

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model

model = load_model()

# -----------------------------
# USER INPUT UI
# -----------------------------
st.sidebar.header("Input Parameters")

people_ahead = st.sidebar.slider("People Ahead in Queue", 0, 50, 10)
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

# -----------------------------
# CREATE INPUT DATAFRAME
# -----------------------------
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
    st.success(f"⏱ Estimated Waiting Time: **{round(prediction[0], 2)} minutes**")
