import streamlit as st
import os
from PIL import Image

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Team & Model App",
    layout="wide"
)

# ---------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------
st.markdown("""
<style>

body {
    overflow: hidden !important;
}

/* Team card styling */
.team-card {
    border: 2px solid #e2e8f0;
    border-radius: 18px;
    padding: 20px;
    background: #ffffff;
    transition: 0.25s ease;
    text-align: center;
}
.team-card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.12);
    border-color: #4aa3ff;
}

.team-img {
    border-radius: 14px;
    width: 100%;
    height: 260px;
    object-fit: cover;
    margin-bottom: 15px;
}

.team-name {
    font-size: 1.4rem;
    font-weight: 700;
}

.team-role {
    font-size: 1rem;
    color: #4aa3ff;
    margin-bottom: 12px;
}

/* Input styling */
input[type=text] {
    font-size: 1.1rem;
}

.note {
    font-size: 0.85rem;
    color: #777;
    margin-top: -8px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["👥 Who We Are", "🧮 Model Inputs"])

# =========================================================
# PAGE 1 — TEAM PAGE
# =========================================================
if page == "👥 Who We Are":

    st.markdown("<h1 style='text-align:center;'>Meet Our Team</h1>", unsafe_allow_html=True)
    st.write("")

    team = [
        ("Sherif Karam", "Team Leader"),
        ("Ahmed Hazem", "Member"),
        ("Hussein Khalaf", "Member"),
        ("Salma Ahmed", "Member"),
        ("Habiba Youssef", "Member"),
        ("Nouran Shawkat", "Member"),
    ]

    cols = st.columns(3, gap="large")

    for i, (name, role) in enumerate(team):
        with cols[i % 3]:

            # Auto-detect picture (.png or .jpg)
            img_path_png = f"pictures/{name}.png"
            img_path_jpg = f"pictures/{name}.jpg"
            img_file = img_path_png if os.path.exists(img_path_png) else img_path_jpg

            st.markdown("<div class='team-card'>", unsafe_allow_html=True)

            if os.path.exists(img_file):
                st.image(img_file, use_column_width=True, caption="", output_format="PNG")
            else:
                st.write("📌 No image found")

            st.markdown(
                f"""
                <div class='team-name'>{name}</div>
                <div class='team-role'>{role}</div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# PAGE 2 — MODEL INPUTS
# =========================================================
elif page == "🧮 Model Inputs":

    st.markdown("<h1 style='text-align:center;'>Model Feature Inputs</h1>", unsafe_allow_html=True)
    st.write("")

    st.markdown("### Please enter **integer values from 1 to 10 only**.")

    def feature_input(label, note=""):
        col = st.container()

        value = col.text_input(label, "")

        # Note under input
        if note:
            col.markdown(f"<div class='note'>{note}</div>", unsafe_allow_html=True)

        # Validation
        if value == "":
            return None

        if not value.isdigit():
            st.error(f"❌ '{label}' must be a whole number.")
            return None

        value = int(value)

        if value < 1 or value > 10:
            st.error(f"❌ '{label}' must be between **1 and 10**.")
            return None

        return value

    col1, col2 = st.columns(2)

    with col1:
        f1 = feature_input("Feature 1", "This represents X1 in the model.")
        f2 = feature_input("Feature 2", "Measures behavioural trend.")
        f3 = feature_input("Feature 3")

    with col2:
        f4 = feature_input("Feature 4")
        f5 = feature_input("Feature 5", "Used for interpretation of category Y.")
        f6 = feature_input("Feature 6")

    st.write("")
    if st.button("Submit Inputs"):
        features = [f1, f2, f3, f4, f5, f6]

        if any(v is None for v in features):
            st.error("⚠️ Please correct all inputs before submitting.")
        else:
            st.success("✔️ All inputs are valid! Ready for model prediction.")
            st.write("### Final Values:", features)
