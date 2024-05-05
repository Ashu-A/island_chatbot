import streamlit as st
st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)
header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Hi I am SEPI a virtual assistant for Island Team')

def strength_check():
    st.subheader("Strength Check")
    # Input fields
    allowable_stress = st.number_input("Allowable Stress (in Pascal)", min_value=0.0, step=1e5, format="%.0f")
    applied_load = st.number_input("Applied Load (in Newtons)", min_value=0.0, step=10.0, format="%.2f")
    area = st.number_input("Cross-sectional Area (in meter^2)", min_value=0.01, step=0.01, format="%.2f")

    # Calculation
    stress = applied_load / area

    if stress <= allowable_stress:
        st.write("Strength check passed.")
    else:
        st.write("Strength check failed.")

def moment_check():
    st.subheader("Moment Check")
    # Input fields
    allowable_moment = st.number_input("Allowable Moment (in Newton-meter)", min_value=0.0, step=10.0, format="%.2f")
    applied_moment = st.number_input("Applied Moment (in Newton-meter)", min_value=0.0, step=10.0, format="%.2f")

    # Calculation
    if applied_moment <= allowable_moment:
        st.write("Moment check passed.")
    else:
        st.write("Moment check failed.")

def shear_check():
    st.subheader("Shear Check")
    # Input fields
    allowable_shear = st.number_input("Allowable Shear (in Newtons)", min_value=0.0, step=10.0, format="%.2f")
    applied_shear = st.number_input("Applied Shear (in Newtons)", min_value=0.0, step=10.0, format="%.2f")

    # Calculation
    if applied_shear <= allowable_shear:
        st.write("Shear check passed.")
    else:
        st.write("Shear check failed.")

def deflection_check():
    st.subheader("Deflection Check")
    # Input fields
    allowable_deflection = st.number_input("Allowable Deflection (in meters)", min_value=0.0, step=0.01, format="%.2f")
    applied_load = st.number_input("Applied Load (in Newtons)", min_value=0.0, step=10.0, format="%.2f")
    modulus_of_elasticity = st.number_input("Modulus of Elasticity (in Pascal)", min_value=1e5, step=1e5, format="%.0f")
    moment_of_inertia = st.number_input("Moment of Inertia (in meter^4)", min_value=0.1, step=0.1, format="%.2f")
    beam_length = st.number_input("Beam Length (in meters)", min_value=0.1, step=0.1, format="%.2f")

    # Calculation
    beam_deflection = (applied_load * beam_length ** 3) / (48 * modulus_of_elasticity * moment_of_inertia)

    if beam_deflection <= allowable_deflection:
        st.write("Deflection check passed.")
    else:
        st.write("Deflection check failed.")

# App layout
st.title("Structural Calculations")

calculation_choice = st.sidebar.selectbox(
    "Select Calculation",
    ("Strength Check", "Moment Check", "Shear Check", "Deflection Check")
)

if calculation_choice == "Strength Check":
    strength_check()
elif calculation_choice == "Moment Check":
    moment_check()
elif calculation_choice == "Shear Check":
    shear_check()
elif calculation_choice == "Deflection Check":
    deflection_check()


# Footer
st.markdown(
    """
    ---
    Made with ❤️ by Island Team
    """
)
