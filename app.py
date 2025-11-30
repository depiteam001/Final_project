import streamlit as st
import os
from PIL import Image

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Project App", layout="wide")

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>

/* Remove scroll */
section.main > div { padding-top: 20px !important; }

/* Navigation buttons */
.nav-btn {
    display: inline-block;
    padding: 10px 18px;
    background: #4aa3ff;
    color: white;
    border-radius: 10px;
    margin-right: 10px;
    font-weight: 600;
    transition: 0.2s;
}
.nav-btn:hover {
    background: #1d8bff;
}

/* Team cards */
.team-card {
    border: 2px solid #e5e5e5;
    border-radius: 16px;
    padding: 20px;
    transition: all 0.2s ease-in-out;
    background: #ffffff;
    text-align: center;
}
.team-card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
    border-color: #4aa3ff;
}
.team-img {
    border-radius: 12px;
    width: 100%;
    height: 280px;
    object-fit: cover;
    margin-bottom: 15px;
}
.team-name {
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 5px;
}
.team-role {
    font-size: 1rem;
    color: #4aa3ff;
    margin-bottom: 12px;
}

input[type=number] {
    -moz-appearance: textfield;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PAGE NAVIGATION
# ---------------------------------------------------------
st.markdown(
    """
    <a class='nav-btn' href='/?page=team'>Who We Are</a>
    <a class='nav-btn' href='/?page=model'>Model Inputs</a>
    """,
    unsafe_allow_html=True
)

query_params = st.query_params
page = query_params.get("page", ["team"])[0]

# ---------------------------------------------------------
# TEAM PAGE
# ---------------------------------------------------------
if page == "team":

    st.title("Meet Our Team")

    team = [
        ("Sherif Karam", "Team Leader"),
        ("Ahmed Hazem", "Member"),
        ("Hussein Khalaf", "Member"),
        ("Salma Ahmed", "Member"),
        ("Habiba Youssef", "Member"),
        ("Nouran Shawkat", "Member"),
    ]

    cols = st.columns(3)

    for i, (name, role) in enumerate(team):
        with cols[i % 3]:
            img_path_jpg = f"pictures/{name}.jpg"
            img_path_png = f"pictures/{name}.png"
            img_to_use = img_path_png if os.path.exists(img_path_png) else img_path_jpg

            st.markdown(f"""
                <div class='team-card'>
                    <img src='{img_to_use}' class='team-img'>
                    <div class='team-name'>{name}</div>
                    <div class='team-role'>{role}</div>
                </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MODEL INPUTS PAGE
# ---------------------------------------------------------
elif page == "model":

    st.title("Model Feature Inputs")

    st.markdown("""
    Enter a value **between 1 and 10** for each feature (integers only).  
    """)

    def int_input(label, help_text=""):
        value = st.text_input(label, value="", help=help_text)

        if value.strip() == "":
            return None

        if not value.isdigit():
            st.error("❌ Only whole numbers are allowed.")
            return None

        value = int(value)

        if value < 1 or value > 10:
            st.error("❌ Value must be between 1 and 10.")
            return None

        return value

    st.subheader("🔧 Model Features")

    col1, col2 = st.columns(2)

    with col1:
        feature1 = int_input("Feature 1", "This represents X1 meaning ...")
        feature2 = int_input("Feature 2", "This measures behaviour Y ...")
        feature3 = int_input("Feature 3")

    with col2:
        feature4 = int_input("Feature 4")
        feature5 = int_input("Feature 5", "Useful when analyzing ...")
        feature6 = int_input("Feature 6")

    if st.button("Submit"):
        if None in [feature1, feature2, feature3, feature4, feature5, feature6]:
            st.error("⚠️ Please complete all fields correctly.")
        else:
            st.success("✔️ All inputs are valid! Ready for model processing.")
