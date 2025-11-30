import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# -------------------------------------------
# PAGE SETUP
# -------------------------------------------
st.set_page_config(
    page_title="Mental Health Model Tester",
    page_icon="🧠",
    layout="wide"
)

# -------------------------------------------
# LOAD MODEL + FEATURE IMPORTANCE
# -------------------------------------------
@st.cache_resource
def load_models():
    model_dir = os.path.join(os.path.dirname(__file__), "saved_models")
    try:
        pipeline = joblib.load(os.path.join(model_dir, "full_pipeline.pkl"))
        feature_importance = pd.read_csv(os.path.join(model_dir, "feature_importance.csv"))
        return pipeline, feature_importance
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

pipeline, feature_importance = load_models()
if pipeline is None:
    st.stop()

# -------------------------------------------
# VALIDATION FUNCTION (NO DECIMALS)
# -------------------------------------------
def int_input(label, min_val, max_val):
    val = st.number_input(label, min_value=min_val, max_value=max_val, step=1)
    if isinstance(val, float) and not val.is_integer():
        st.error("❌ Only whole numbers allowed — no decimals.")
        st.stop()
    return int(val)

# -------------------------------------------
# "WHO WE ARE" PAGE
# -------------------------------------------
def load_image(name):
    folder = os.path.join(os.path.dirname(__file__), "pictures")
    for ext in [".jpg", ".jpeg", ".png"]:
        img_path = os.path.join(folder, name + ext)
        if os.path.exists(img_path):
            return img_path
    return None

def who_we_are_page():
    st.title("Who We Are")
    st.write("""
    Welcome to our Mental Health Risk Assessment project.  
    We are a collaborative team focused on building meaningful data products that help improve well-being.
    """)

    team = [
        ("Sherif Karam", "Team Leader"),
        ("Ahmed Hazem", "Team Member"),
        ("Hussein Khalaf", "Team Member"),
        ("Salma Ahmed", "Team Member"),
        ("Habiba Youssef", "Team Member"),
        ("Nouran Shawkat", "Team Member")
    ]

    cols = st.columns(3)

    for i, (name, role) in enumerate(team):
        with cols[i % 3]:
            img_path = load_image(name)
            if img_path:
                st.image(img_path, caption=name, width=220)
            else:
                st.warning(f"No image found for {name}")

            st.markdown(f"""
            ### {name}
            **{role}**
            """)

# -------------------------------------------
# MAIN APP PAGE
# -------------------------------------------
def model_tester_page():

    st.title("🧠 Mental Health Risk Assessment Model Tester")

    tab1, tab2 = st.tabs(["📋 Single Prediction", "📊 Feature Importance"])

    with tab1:
        st.subheader("Enter Patient Information (All fields required)")

        col1, col2, col3 = st.columns(3)

        # -------- BASIC INFORMATION --------
        with col1:
            st.write("### Basic Information")
            age = int_input("Age", 16, 80)
            gender = st.selectbox("Gender *", ["Choose...", "Male", "Female", "Other"])
            if gender == "Choose...":
                st.error("Please select a gender.")
                st.stop()

            employment = st.selectbox("Employment Status *",
                ["Choose...", "Employed", "Unemployed", "Self-employed", "Retired", "Student"])
            if employment == "Choose...":
                st.error("Please select an employment status.")
                st.stop()

            marital = st.selectbox("Marital Status *",
                ["Choose...", "Single", "Married", "Divorced", "Widowed"])
            if marital == "Choose...":
                st.error("Please select a marital status.")
                st.stop()

        # -------- LIFESTYLE --------
        with col2:
            st.write("### Lifestyle")
            work_hours = int_input("Work Hours per Week", 0, 60)
            physical_activity = int_input("Physical Activity Hours per Week", 0, 20)
            screen_time = int_input("Screen Time per Day (hours)", 0, 16)
            sleep_hours = int_input("Sleep Hours per Night", 0, 12)
            alcohol_units = int_input("Alcohol Units per Week", 0, 20)
            smoking = st.selectbox("Smoking Status *", ["Choose...", "Never", "Former", "Current"])
            if smoking == "Choose...":
                st.error("Please select a smoking status.")
                st.stop()

        # -------- HEALTH --------
        with col3:
            st.write("### Health & Psychological")
            financial_stress = int_input("Financial Stress (1-10)", 1, 10)
            family_history = st.selectbox("Family History of Mental Illness *", ["Choose...", "No", "Yes"])
            if family_history == "Choose...":
                st.error("Please select an answer.")
                st.stop()

            chronic_condition = st.selectbox("Chronic Condition *", ["Choose...", "No", "Yes"])
            if chronic_condition == "Choose...":
                st.error("Please select an answer.")
                st.stop()

            support_system = int_input("Support System Score (1-10)", 1, 10)
            stress_level = int_input("Stress Level Score (1-10)", 1, 10)
            rumination = int_input("Rumination Score (1-10)", 1, 10)

        # -------- PSYCHOLOGICAL --------
        col4, col5 = st.columns(2)

        with col4:
            st.write("### Emotional Indicators")
            feeling_nervous = st.selectbox("Feeling Nervous *", ["Choose...", "No", "Yes"])
            trouble_concentrating = st.selectbox("Trouble Concentrating *", ["Choose...", "No", "Yes"])
            hopelessness = st.selectbox("Hopelessness *", ["Choose...", "No", "Yes"])

            for field in [feeling_nervous, trouble_concentrating, hopelessness]:
                if field == "Choose...":
                    st.error("Please answer all emotional indicators.")
                    st.stop()

        with col5:
            st.write("### Behavioral Indicators")
            avoids_people = st.selectbox("Avoids People *", ["Choose...", "No", "Yes"])
            nightmares = st.selectbox("Nightmares *", ["Choose...", "No", "Yes"])
            medication_usage = st.selectbox("Medication Usage *", ["Choose...", "No", "Yes"])

            for field in [avoids_people, nightmares, medication_usage]:
                if field == "Choose...":
                    st.error("Please answer all behavioral indicators.")
                    st.stop()

        # -------- PREDICTION --------
        if st.button("🔍 Predict Mental Health Risk"):
            input_data = pd.DataFrame({
                'Age': [age],
                'Gender': [gender],
                'Employment_Status': [employment],
                'Marital_Status': [marital],
                'Work_Hours_per_Week': [work_hours],
                'Financial_Stress': [financial_stress],
                'Physical_Activity_Hours_per_Week': [physical_activity],
                'Screen_Time_per_Day_hours': [screen_time],
                'Sleep_Hours_per_Night': [sleep_hours],
                'Alcohol_Units_per_Week': [alcohol_units],
                'Smoking_Status': [smoking],
                'Family_History': [1 if family_history == "Yes" else 0],
                'Chronic_Condition': [1 if chronic_condition == "Yes" else 0],
                'Support_System_Score': [support_system],
                'Stress_Level_Score': [stress_level],
                'Rumination_Score': [rumination],
                'Feeling_Nervous': [1 if feeling_nervous == "Yes" else 0],
                'Trouble_Concentrating': [1 if trouble_concentrating == "Yes" else 0],
                'Hopelessness': [1 if hopelessness == "Yes" else 0],
                'Avoids_People': [1 if avoids_people == "Yes" else 0],
                'Nightmares': [1 if nightmares == "Yes" else 0],
                'Medication_Usage': [1 if medication_usage == "Yes" else 0]
            })

            prediction = pipeline.predict(input_data)[0]
            proba = pipeline.predict_proba(input_data)[0]

            st.subheader("📊 Prediction Results")

            colA, colB = st.columns(2)
            with colA:
                st.metric(
                    label="Mental Health Status",
                    value="⚠️ At Risk" if prediction == 1 else "✅ Low Risk"
                )
            with colB:
                st.metric(
                    "Risk Probability",
                    f"{proba[1]*100:.1f}%"
                )

    with tab2:
        st.subheader("Feature Importance")
        top_n = st.slider("Top N Features", 5, 30, 15)
        top_features = feature_importance.head(top_n)

        st.bar_chart(top_features.set_index("feature")["importance_mean"])


# -------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------
page = st.sidebar.selectbox("Navigate", ["Model Tester", "Who We Are"])

if page == "Model Tester":
    model_tester_page()
else:
    who_we_are_page()
