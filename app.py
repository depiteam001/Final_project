import streamlit as st
import joblib
import pandas as pd
import numpy as np
import os
from PIL import Image

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Mental Health Risk Assessment",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    /* Main Background & Fonts */
    .main {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Custom Card Style */
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.2s;
        border: 1px solid #e0e0e0;
    }
    .stCard:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    h1 { text-align: center; margin-bottom: 30px; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #2c3e50;
    }
    
    /* Team Section */
    .team-member-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
        margin-top: 10px;
        text-align: center;
    }
    .team-member-role {
        font-size: 0.9rem;
        color: #666;
        font-style: italic;
        text-align: center;
        margin-bottom: 15px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        height: 50px;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -----------------------------------------------------------------------------

@st.cache_resource
def load_models():
    """Loads the ML pipeline and feature importance data."""
    model_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
    try:
        pipeline = joblib.load(os.path.join(model_dir, 'full_pipeline.pkl'))
        feature_importance = pd.read_csv(os.path.join(model_dir, 'feature_importance.csv'))
        return pipeline, feature_importance
    except Exception as e:
        return None, None

def render_team_member(image_path, name, role):
    """Renders a single team member card."""
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    
    # Check for image extensions
    img_found = None
    for ext in ['.jpg', '.jpeg', '.png']:
        full_path = os.path.join("pictures", name + ext)
        if os.path.exists(full_path):
            img_found = full_path
            break
            
    if img_found:
        st.image(img_found, use_container_width=True)
    else:
        # Fallback placeholder if image missing
        st.markdown(f"""
        <div style="height:200px; background-color:#eee; display:flex; 
                    align-items:center; justify-content:center; border-radius:10px;">
            <span style="font-size:40px;">👤</span>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
        <div class="team-member-name">{name}</div>
        <div class="team-member-role">{role}</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. NAVIGATION & LAYOUT
# -----------------------------------------------------------------------------

# Load Models
pipeline, feature_importance = load_models()

# Sidebar Navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062331.png", width=100)
    st.title("Navigation")
    page = st.radio("Go to", ["🧠 Model Tester", "👥 Who Are We"])
    
    st.markdown("---")
    st.info("**System Status:** " + ("✅ Online" if pipeline else "❌ Model Error"))
    if not pipeline:
        st.error("Saved models not found. Please check 'saved_models' folder.")

# -----------------------------------------------------------------------------
# 4. PAGE: MODEL TESTER
# -----------------------------------------------------------------------------
if page == "🧠 Model Tester":
    st.markdown("<h1>🧠 Mental Health Risk Assessment</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Fill in the details below to assess potential risk factors. All fields are required.</p>", unsafe_allow_html=True)

    if pipeline:
        # Form Container
        with st.container():
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.subheader("📋 Patient Information Form")
            st.markdown("---")

            # --- Row 1: Demographics ---
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                age = st.number_input("Age (16-80)", min_value=16, max_value=80, value=None, step=1, placeholder="Type age...")
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=None, placeholder="Select...")
            with col3:
                employment = st.selectbox("Employment Status", ["Employed", "Unemployed", "Self-employed", "Retired", "Student"], index=None, placeholder="Select...")
            with col4:
                marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"], index=None, placeholder="Select...")

            st.write("") # Spacer

            # --- Row 2: Lifestyle ---
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                work_hours = st.number_input("Work Hours/Week", min_value=0, max_value=100, value=None, step=1, placeholder="0-100")
            with col2:
                physical_activity = st.number_input("Activity Hours/Week", min_value=0, max_value=50, value=None, step=1, placeholder="0-50")
            with col3:
                screen_time = st.number_input("Screen Time (Hours/Day)", min_value=0, max_value=24, value=None, step=1, placeholder="0-24")
            with col4:
                sleep_hours = st.number_input("Sleep Hours/Night", min_value=0, max_value=24, value=None, step=1, placeholder="0-24")

            st.write("") # Spacer

            # --- Row 3: Habits & Health ---
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                alcohol_units = st.number_input("Alcohol Units/Week", min_value=0, max_value=50, value=None, step=1)
            with col2:
                smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"], index=None, placeholder="Select...")
            with col3:
                family_history = st.selectbox("Family History of Mental Illness", ["No", "Yes"], index=None, placeholder="Select...")
            with col4:
                chronic_condition = st.selectbox("Chronic Condition", ["No", "Yes"], index=None, placeholder="Select...")

            st.markdown("</div>", unsafe_allow_html=True)

            # --- Psychological Indicators (Rankings 1-10) ---
            st.markdown('<div class="stCard">', unsafe_allow_html=True)
            st.subheader("🧘 Psychological & Behavioral Indicators")
            st.info("Please rate the following on a scale of 1 to 10 (1 = Lowest, 10 = Highest)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                financial_stress = st.number_input("Financial Stress (1-10)", min_value=1, max_value=10, value=None, step=1)
                support_system = st.number_input("Support System (1-10)", min_value=1, max_value=10, value=None, step=1)
            with col2:
                stress_level = st.number_input("Stress Level (1-10)", min_value=1, max_value=10, value=None, step=1)
                rumination = st.number_input("Rumination Score (1-10)", min_value=1, max_value=10, value=None, step=1)
            with col3:
                pass # Empty column for balance

            st.write("---")
            st.write("**Specific Symptoms (Yes/No)**")
            
            # Symptoms Matrix
            sym_col1, sym_col2, sym_col3 = st.columns(3)
            with sym_col1:
                feeling_nervous = st.selectbox("Feeling Nervous?", ["No", "Yes"], index=None, placeholder="Select...")
                avoids_people = st.selectbox("Avoids People?", ["No", "Yes"], index=None, placeholder="Select...")
            with sym_col2:
                trouble_concentrating = st.selectbox("Trouble Concentrating?", ["No", "Yes"], index=None, placeholder="Select...")
                nightmares = st.selectbox("Experiencing Nightmares?", ["No", "Yes"], index=None, placeholder="Select...")
            with sym_col3:
                hopelessness = st.selectbox("Feeling Hopeless?", ["No", "Yes"], index=None, placeholder="Select...")
                medication_usage = st.selectbox("Using Medication?", ["No", "Yes"], index=None, placeholder="Select...")
            
            st.markdown("</div>", unsafe_allow_html=True)

            # --- Prediction Logic ---
            predict_btn = st.button("🔍 Analyze & Predict Risk")

            if predict_btn:
                # 1. Validation Check: Ensure NO field is None
                input_vars = [age, gender, employment, marital, work_hours, physical_activity, 
                              screen_time, sleep_hours, alcohol_units, smoking, family_history, 
                              chronic_condition, financial_stress, support_system, stress_level, 
                              rumination, feeling_nervous, avoids_people, trouble_concentrating, 
                              nightmares, hopelessness, medication_usage]

                if any(v is None for v in input_vars):
                    st.error("⚠️ Incomplete Data: Please fill out ALL fields before predicting. Default values are not allowed.")
                else:
                    # 2. Data Preparation
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
                        # 3. Prediction
                        prediction = pipeline.predict(input_data)[0]
                        prediction_proba = pipeline.predict_proba(input_data)[0]

                        # 4. Results Display
                        st.markdown('<div class="stCard">', unsafe_allow_html=True)
                        st.subheader("📊 Assessment Results")
                        
                        res_col1, res_col2 = st.columns(2)
                        
                        with res_col1:
                            if prediction == 1:
                                st.error(f"## ⚠️ Status: At Risk\n\nThe model indicates a potential risk for mental health issues.")
                            else:
                                st.success(f"## ✅ Status: Low Risk\n\nThe model indicators suggest a stable mental health state.")
                                
                        with res_col2:
                            st.metric("Risk Probability", f"{prediction_proba[1]*100:.1f}%")
                            st.progress(prediction_proba[1])
                            st.caption(f"Confidence Level: {max(prediction_proba)*100:.1f}%")
                        
                        st.markdown("</div>", unsafe_allow_html=True)

                        # Feature Importance Expander
                        with st.expander("Show Contributing Factors (Feature Importance)"):
                            if feature_importance is not None:
                                top_features = feature_importance.head(10)
                                st.bar_chart(top_features.set_index('feature')['importance_mean'])
                            else:
                                st.warning("Feature importance data not found.")

                    except Exception as e:
                        st.error(f"An error occurred during processing: {str(e)}")

# -----------------------------------------------------------------------------
# 5. PAGE: WHO ARE WE
# -----------------------------------------------------------------------------
elif page == "👥 Who Are We":
    st.markdown("<h1>Meet the Team</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1em;'>The dedicated minds behind the Mental Health Risk Assessment Model.</p><br>", unsafe_allow_html=True)

    # Team Data
    team = [
        {"name": "Sherif Karam", "role": "Team Leader", "id": 1},
        {"name": "Ahmed Hazem", "role": "Team Member", "id": 2},
        {"name": "Hussein Khalaf", "role": "Team Member", "id": 3},
        {"name": "Salma Ahmed", "role": "Team Member", "id": 4},
        {"name": "Habiba Youssef", "role": "Team Member", "id": 5},
        {"name": "Nouran Shawkat", "role": "Team Member", "id": 6},
    ]

    # Render Grid (3 columns wide)
    row1 = st.columns(3)
    row2 = st.columns(3)
    
    # First Row
    for i, col in enumerate(row1):
        if i < len(team):
            member = team[i]
            with col:
                render_team_member(None, member["name"], member["role"])
    
    # Second Row
    for i, col in enumerate(row2):
        idx = i + 3
        if idx < len(team):
            member = team[idx]
            with col:
                render_team_member(None, member["name"], member["role"])

    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888;'>© 2025 Mental Health AI Project</p>", unsafe_allow_html=True)
