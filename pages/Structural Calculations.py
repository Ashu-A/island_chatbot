import streamlit as st

st.set_page_config(
    page_title="Island Chatbot",
    page_icon="🏝️",
)
header = st.container()
with header:
    st.title('Island Chatbot')
    st.info('Hi I am SEPI a virtual assistant for Island Team.')

def strength_check(allowable_stress, applied_load, area):
    # Calculation
    stress = applied_load / area

    if stress <= allowable_stress:
        return "Strength check passed."
    else:
        return "Strength check failed."

def moment_check(allowable_moment, applied_moment):
    # Calculation
    if applied_moment <= allowable_moment:
        return "Moment check passed."
    else:
        return "Moment check failed."

def shear_check(allowable_shear, applied_shear):
    # Calculation
    if applied_shear <= allowable_shear:
        return "Shear check passed."
    else:
        return "Shear check failed."

def deflection_check(allowable_deflection, applied_load, modulus_of_elasticity, moment_of_inertia, beam_length):
    # Calculation
    beam_deflection = (applied_load * beam_length ** 3) / (48 * modulus_of_elasticity * moment_of_inertia)

    if beam_deflection <= allowable_deflection:
        return "Deflection check passed."
    else:
        return "Deflection check failed."

# App layout
st.title("Structural Calculations")

# Input fields
allowable_stress = st.number_input("Allowable Stress (in Pascal)", min_value=0.0, step=1e5, format="%.0f")
applied_load = st.number_input("Applied Load (in Newtons)", min_value=0.0, step=10.0, format="%.2f")
area = st.number_input("Cross-sectional Area (in meter^2)", min_value=0.01, step=0.01, format="%.2f")

allowable_moment = st.number_input("Allowable Moment (in Newton-meter)", min_value=0.0, step=10.0, format="%.2f")
applied_moment = st.number_input("Applied Moment (in Newton-meter)", min_value=0.0, step=10.0, format="%.2f")

allowable_shear = st.number_input("Allowable Shear (in Newtons)", min_value=0.0, step=10.0, format="%.2f")
applied_shear = st.number_input("Applied Shear (in Newtons)", min_value=0.0, step=10.0, format="%.2f")

allowable_deflection = st.number_input("Allowable Deflection (in meters)", min_value=0.0, step=0.01, format="%.2f")
modulus_of_elasticity = st.number_input("Modulus of Elasticity (in Pascal)", min_value=1e5, step=1e5, format="%.0f")
moment_of_inertia = st.number_input("Moment of Inertia (in meter^4)", min_value=0.1, step=0.1, format="%.2f")
beam_length = st.number_input("Beam Length (in meters)", min_value=0.1, step=0.1, format="%.2f")

# Calculate and display results
st.subheader("Results:")
st.write("Strength Check:", strength_check(allowable_stress, applied_load, area))
st.write("Moment Check:", moment_check(allowable_moment, applied_moment))
st.write("Shear Check:", shear_check(allowable_shear, applied_shear))
st.write("Deflection Check:", deflection_check(allowable_deflection, applied_load, modulus_of_elasticity, moment_of_inertia, beam_length))

# Footer
st.markdown(
    """
    ---
    Made with ❤️ by Island Team
    """
)
