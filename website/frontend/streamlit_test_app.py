# Auto-install missing dependencies on first run
import sys
import subprocess
import importlib

def _ensure_packages(packages):
    """Install missing packages with pip, preferring pre-built wheels."""
    for pkg in packages:
        try:
            importlib.import_module(pkg)
            print(f"✓ {pkg} already installed")
        except ImportError:
            print(f"Installing {pkg}...")
            # Use --only-binary to avoid building from source (fixes cmake/PyArrow issues on Python 3.14)
            cmd = [sys.executable, '-m', 'pip', 'install', '--only-binary', ':all:', pkg]
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError:
                # Fallback: try without binary restriction
                print(f"Retrying {pkg} without binary restriction...")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

_ensure_packages(['streamlit', 'joblib', 'pandas', 'numpy'])

import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Mental Health Model Tester",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Mental Health Risk Assessment Model Tester")
st.write("Test the trained mental health prediction model with custom input values.")

# Load the model and preprocessor
@st.cache_resource
def load_models():
    model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'saved_models')
    
    try:
        pipeline = joblib.load(os.path.join(model_dir, 'full_pipeline.pkl'))
        feature_importance = pd.read_csv(os.path.join(model_dir, 'feature_importance.csv'))
        return pipeline, feature_importance
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None

pipeline, feature_importance = load_models()

if pipeline is None:
    st.error("Could not load the model. Make sure the saved_models folder contains the necessary files.")
    st.stop()

# Create tabs for organization
tab1, tab2 = st.tabs(["📋 Single Prediction", "📊 Feature Importance"])

with tab1:
    st.subheader("Enter Patient Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Basic Information**")
        age = st.slider("Age", 16, 80, 30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        employment = st.selectbox("Employment Status", 
                                   ["Employed", "Unemployed", "Self-employed", "Retired", "Student"])
        marital = st.selectbox("Marital Status", 
                               ["Single", "Married", "Divorced", "Widowed"])
    
    with col2:
        st.write("**Lifestyle**")
        work_hours = st.slider("Work Hours per Week", 0, 60, 40)
        physical_activity = st.slider("Physical Activity Hours per Week", 0, 20, 3)
        screen_time = st.slider("Screen Time per Day (hours)", 0, 16, 6)
        sleep_hours = st.slider("Sleep Hours per Night", 0, 12, 7)
        alcohol_units = st.slider("Alcohol Units per Week", 0, 20, 2)
        smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
    
    with col3:
        st.write("**Health & Psychological**")
        financial_stress = st.slider("Financial Stress (1-10)", 1, 10, 5)
        family_history = st.selectbox("Family History of Mental Illness", ["No", "Yes"])
        chronic_condition = st.selectbox("Chronic Condition", ["No", "Yes"])
        support_system = st.slider("Support System Score (1-10)", 1, 10, 7)
        stress_level = st.slider("Stress Level Score (1-10)", 1, 10, 5)
        rumination = st.slider("Rumination Score (1-10)", 1, 10, 5)
    
    # Second row of psychological indicators
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.write("**Emotional Indicators**")
        feeling_nervous = st.selectbox("Feeling Nervous", ["No", "Yes"])
        trouble_concentrating = st.selectbox("Trouble Concentrating", ["No", "Yes"])
        hopelessness = st.selectbox("Hopelessness", ["No", "Yes"])
    
    with col5:
        st.write("**Behavioral Indicators**")
        avoids_people = st.selectbox("Avoids People", ["No", "Yes"])
        nightmares = st.selectbox("Nightmares", ["No", "Yes"])
        medication_usage = st.selectbox("Medication Usage", ["No", "Yes"])
    
    with col6:
        st.write("")
        st.write("")
        st.write("")
    
    # Prepare input data
    if st.button("🔍 Predict Mental Health Risk", key="predict_btn"):
        # Create input dataframe with correct format
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
        
        try:
            # Make prediction
            prediction = pipeline.predict(input_data)[0]
            prediction_proba = pipeline.predict_proba(input_data)[0]
            
            # Display results
            st.subheader("📊 Prediction Results")
            
            col_result1, col_result2 = st.columns(2)
            
            with col_result1:
                st.metric(
                    label="Mental Health Status",
                    value="⚠️ At Risk" if prediction == 1 else "✅ Low Risk",
                    delta="Requires attention" if prediction == 1 else "Normal"
                )
            
            with col_result2:
                st.metric(
                    label="Risk Probability",
                    value=f"{prediction_proba[1]*100:.1f}%",
                    delta=f"Confidence: {max(prediction_proba)*100:.1f}%"
                )
            
            # Show probability breakdown
            st.write("**Probability Breakdown:**")
            prob_col1, prob_col2 = st.columns(2)
            with prob_col1:
                st.progress(prediction_proba[0], text=f"Low Risk: {prediction_proba[0]*100:.1f}%")
            with prob_col2:
                st.progress(prediction_proba[1], text=f"At Risk: {prediction_proba[1]*100:.1f}%")
            
            # Show a warning if high risk
            if prediction == 1 and prediction_proba[1] > 0.7:
                st.warning("⚠️ High risk prediction. Consider professional consultation.")
            elif prediction == 1:
                st.info("ℹ️ Moderate risk detected. Monitor health indicators.")
                
        except Exception as e:
            st.error(f"Error making prediction: {e}")
            st.write("Debug info:", str(e))

with tab2:
    st.subheader("📊 Feature Importance Analysis")
    
    # Show top important features
    top_n = st.slider("Show top N features", 5, 30, 15)
    
    # Get top features
    top_features = feature_importance.head(top_n)
    
    # Create two columns for layout
    chart_col, table_col = st.columns([2, 1])
    
    with chart_col:
        # Bar chart
        st.bar_chart(
            data=top_features.set_index('feature')['importance_mean'],
            height=400
        )
    
    with table_col:
        st.write("**Top Features:**")
        st.dataframe(
            top_features[['feature', 'importance_mean']].head(10),
            hide_index=True,
            width=True
        )
    
    # Full feature importance table
    st.write("**All Features Importance:**")
    st.dataframe(feature_importance, width=True, height=400)

st.sidebar.write("---")
st.sidebar.write("**About this app:**")
st.sidebar.write("""
This app uses a trained machine learning model to predict mental health risk based on various lifestyle, 
health, and psychological indicators.

**Model Information:**
- Algorithm: Gradient Boosting Classifier
- Training Method: Stratified K-Fold Cross-Validation
- Features: 22 input variables
- Output: Binary classification (Low Risk / At Risk)
""")
