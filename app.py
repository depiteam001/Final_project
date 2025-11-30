# Mental Health Risk Assessment Model Tester
# Streamlit Community Cloud deployment entry point

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# Page Config
st.set_page_config(
    page_title="Mental Health Model Tester",
    page_icon="🧠",
    layout="wide"
)

# Sidebar Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Model Tester", "Who Are We"]
)

# ================================
# LOAD MODEL
# ================================
@st.cache_resource
def load_models():
    model_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
    try:
        pipeline = joblib.load(os.path.join(model_dir, 'full_pipeline.pkl'))
        feature_importance = pd.read_csv(os.path.join(model_dir, 'feature_importance.csv'))
        return pipeline, feature_importance
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

pipeline, feature_importance = load_models()


# =============================================================================
# PAGE 1 — MODEL TESTING
# =============================================================================
if page == "Model Tester":
    st.title("🧠 Mental Health Risk Assessment Model Tester")
    st.write("Fill in all fields to test the mental health risk prediction model.")

    if pipeline is None:
        st.error("❌ Model could not be loaded. Ensure saved_models folder contains the files.")
        st.stop()

    tab1, tab2 = st.tabs(["📋 Single Prediction", "📊 Feature Importance"])

    # ================================
    # TAB 1 — PREDICTION
    # ================================
    with tab1:
        st.subheader("Enter Patient Information")

        # ========== ALL FIELDS REQUIRED ==========
        def required_select(label, options):
            value = st.selectbox(label, ["-- Select --"] + options)
            return None if value == "-- Select --" else value

        def required_slider(label, min_v, max_v):
            value = st.slider(label, min_v, max_v, value=None)
            return value

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("### Basic Information")
            age = required_slider("Age", 16, 80)
            gender = required_select("Gender", ["Male", "Female", "Other"])
            employment = required_select("Employment Status",
                                         ["Employed", "Unemployed", "Self-employed", "Retired", "Student"])
            marital = required_select("Marital Status",
                                      ["Single", "Married", "Divorced", "Widowed"])

        with col2:
            st.write("### Lifestyle")
            work_hours = required_slider("Work Hours per Week", 0, 60)
            physical_activity = required_slider("Physical Activity Hours per Week", 0, 20)
            screen_time = required_slider("Screen Time per Day (hours)", 0, 16)
            sleep_hours = required_slider("Sleep Hours per Night", 0, 12)
            alcohol_units = required_slider("Alcohol Units per Week", 0, 20)
            smoking = required_select("Smoking Status", ["Never", "Former", "Current"])

        with col3:
            st.write("### Health & Psychological")
            financial_stress = required_slider("Financial Stress (1-10)", 1, 10)
            family_history = required_select("Family History of Mental Illness", ["No", "Yes"])
            chronic_condition = required_select("Chronic Condition", ["No", "Yes"])
            support_system = required_slider("Support System Score (1-10)", 1, 10)
            stress_level = required_slider("Stress Level Score (1-10)", 1, 10)
            rumination = required_slider("Rumination Score (1-10)", 1, 10)

        col4, col5, col6 = st.columns(3)

        with col4:
            st.write("### Emotional Indicators")
            feeling_nervous = required_select("Feeling Nervous", ["No", "Yes"])
            trouble_concentrating = required_select("Trouble Concentrating", ["No", "Yes"])
            hopelessness = required_select("Hopelessness", ["No", "Yes"])

        with col5:
            st.write("### Behavioral Indicators")
            avoids_people = required_select("Avoids People", ["No", "Yes"])
            nightmares = required_select("Nightmares", ["No", "Yes"])
            medication_usage = required_select("Medication Usage", ["No", "Yes"])

        with col6:
            st.write("")

        # Check if all fields are filled
        all_values = [
            age, gender, employment, marital,
            work_hours, physical_activity, screen_time, sleep_hours, alcohol_units,
            smoking, financial_stress, family_history, chronic_condition,
            support_system, stress_level, rumination,
            feeling_nervous, trouble_concentrating, hopelessness,
            avoids_people, nightmares, medication_usage
        ]

        if st.button("🔍 Predict Mental Health Risk"):
            if any(v is None for v in all_values):
                st.error("❌ Please fill ALL fields before submitting.")
                st.stop()

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
                    "Mental Health Status",
                    "⚠️ At Risk" if prediction == 1 else "✅ Low Risk"
                )

            with colB:
                st.metric(
                    "Risk Probability",
                    f"{proba[1] * 100:.1f}%"
                )

    # ================================
    # TAB 2 — FEATURE IMPORTANCE
    # ================================
    with tab2:
        st.subheader("📊 Feature Importance Analysis")

        top_n = st.slider("Show top N features", 5, 30, 15)
        top_features = feature_importance.head(top_n)

        colC, colD = st.columns([2, 1])

        with colC:
            st.bar_chart(
                data=top_features.set_index('feature')['importance_mean'],
                height=400
            )

        with colD:
            st.write("**Top Features:**")
            st.dataframe(top_features[['feature', 'importance_mean']], hide_index=True)

        st.write("### All Features")
        st.dataframe(feature_importance, height=400)


# =============================================================================
# PAGE 2 — WHO ARE WE
# =============================================================================
if page == "Who Are We":
    st.title("👥 Who Are We?")
    st.write("Meet the team behind the Mental Health Risk Assessment System.")

    st.markdown("""
    ### **Team Members**
    - 👑 **Sherif Karam** — *Team Leader*  
    - **Ahmed Hazem**  
    - **Hussein Khalaf**  
    - **Salma Ahmed**  
    - **Habiba Youssef**  
    - **Nouran Shawkat**  
    """)

    st.success("We are a dedicated team working on innovative AI healthcare solutions ❤️")
