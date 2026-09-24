import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# PAGE CONFIGURATION & TITLE
# ==============================================================================
st.set_page_config(
    page_title="Cantilever Beam Calculator",
    page_icon="🏗️",
    layout="wide"
)

st.title("🏗️ Cantilever Beam Deflection & Stress Calculator")
st.markdown("---")

# ==============================================================================
# SIDEBAR: TEAM DETAILS
# ==============================================================================
st.sidebar.header("📋 Project & Team Details")
st.sidebar.write("*Course:* Diploma in Mechanical Engineering (Sem 3)")
st.sidebar.write("*Topic:* Cantilever Beam Deflection & Stress Analysis")
st.sidebar.markdown("---")
st.sidebar.subheader("👥 Group Members")
st.sidebar.text("1. Name 1 (Enrollment No. 1)")
st.sidebar.text("2. Name 2 (Enrollment No. 2)")
st.sidebar.text("3. Name 3 (Enrollment No. 3)")
st.sidebar.text("4. Name 4 (Enrollment No. 4)")
st.sidebar.markdown("---")

# ==============================================================================
# INPUT SECTION: MATERIAL PROPERTIES
# ==============================================================================
st.subheader("1. Select Material & Beam Length")

col_mat1, col_mat2 = st.columns(2)

with col_mat1:
    material = st.selectbox(
        "Select Material",
        ["Mild Steel", "Aluminum", "Brass"]
    )

# Material Database: E in GPa, Yield Strength (sigma_y) in MPa
material_db = {
    "Mild Steel": {"E": 200, "yield_strength": 250},
    "Aluminum": {"E": 69, "yield_strength": 95},
    "Brass": {"E": 105, "yield_strength": 200}
}

E_GPa = material_db[material]["E"]
E = E_GPa * 1e9  # Convert GPa to N/m² (Pa)
yield_strength = material_db[material]["yield_strength"]  # in MPa

with col_mat2:
    length_m = st.number_input(
        "Beam Length (m)",
        min_value=0.1,
        max_value=10.0,
        value=2.0,
        step=0.1,
        help="Length of the cantilever beam in meters."
    )

st.info(f"*Selected Material Properties:* Young's Modulus ($E$) = {E_GPa} GPa | Yield Strength ($\sigma_y$) = {yield_strength} MPa")
st.markdown("---")

# ==============================================================================
# INPUT SECTION: CROSS-SECTION & LOAD
# ==============================================================================
col_sec, col_load = st.columns(2)

with col_sec:
    st.subheader("2. Select Cross-Section")
    shape = st.radio(
        "Cross-Sectional Shape",
        ["Solid Rectangle", "Solid Circular", "I-Section"]
    )
    
    I = 0.0  # Moment of inertia (m^4)
    y_max = 0.0  # Distance to extreme fiber (m)
    
    if shape == "Solid Rectangle":
        b_mm = st.number_input("Width, b (mm)", min_value=1.0, value=50.0, step=5.0)
        h_mm = st.number_input("Height, h (mm)", min_value=1.0, value=100.0, step=5.0)
        
        b = b_mm / 1000.0  # Convert mm to m
        h = h_mm / 1000.0
        
        I = (b * (h ** 3)) / 12.0
        y_max = h / 2.0
        
    elif shape == "Solid Circular":
        d_mm = st.number_input("Diameter, d (mm)", min_value=1.0, value=60.0, step=5.0)
        
        d = d_mm / 1000.0  # Convert mm to m
        
        I = (np.pi * (d ** 4)) / 64.0
        y_max = d / 2.0
        
    elif shape == "I-Section":
        st.caption("Symmetric I-Section Dimensions:")
        B_mm = st.number_input("Flange Width, B (mm)", min_value=1.0, value=100.0, step=5.0)
        H_mm = st.number_input("Total Height, H (mm)", min_value=1.0, value=150.0, step=5.0)
        tf_mm = st.number_input("Flange Thickness, t_f (mm)", min_value=1.0, value=10.0, step=1.0)
        tw_mm = st.number_input("Web Thickness, t_w (mm)", min_value=1.0, value=8.0, step=1.0)
        
        # Validation for I-section geometry
        if 2 * tf_mm >= H_mm:
            st.error("⚠️ Invalid Dimensions: Total flange thickness (2 × t_f) cannot be greater than or equal to total height (H)!")
            st.stop()
        if tw_mm >= B_mm:
            st.error("⚠️ Invalid Dimensions: Web thickness (t_w) cannot be greater than or equal to flange width (B)!")
            st.stop()
            
        B = B_mm / 1000.0
        H = H_mm / 1000.0
        tf = tf_mm / 1000.0
        tw = tw_mm / 1000.0
        
        h_inner = H - 2 * tf
        b_inner = B - tw
        
        I = ((B * (H * 3)) - (b_inner * (h_inner * 3))) / 12.0
        y_max = H / 2.0

with col_load:
    st.subheader("3. Apply End Point Load")
    load_kN = st.slider(
        "Point Load at Free End, P (kN)",
        min_value=0.1,
        max_value=50.0,
        value=5.0,
        step=0.1
    )
    P = load_kN * 1000.0  # Convert kN to N

st.markdown("---")

# ==============================================================================
# CALCULATIONS
# ==============================================================================
# 1. Section Modulus Z = I / y_max
Z_m3 = I / y_max
Z_cm3 = Z_m3 * 1e6  # Convert m³ to cm³

# 2. Maximum Bending Moment M_max = P * L
M_max = P * length_m  # N·m

# 3. Maximum Bending Stress sigma_max = M_max / Z
sigma_max_Pa = M_max / Z_m3
sigma_max_MPa = sigma_max_Pa / 1e6  # Convert Pa to MPa

# 4. Maximum Deflection delta_max = (P * L^3) / (3 * E * I)
delta_max_m = (P * (length_m ** 3)) / (3 * E * I)
delta_max_mm = delta_max_m * 1000.0  # Convert m to mm

# ==============================================================================
# DISPLAY RESULTS & SAFETY VALIDATION
# ==============================================================================
st.subheader("📊 Output & Safety Analysis")

res_col1, res_col2, res_col3 = st.columns(3)

with res_col1:
    st.metric(label="Section Modulus (Z)", value=f"{Z_cm3:.2f} cm³")

with res_col2:
    st.metric(label="Max Bending Stress (σ_max)", value=f"{sigma_max_MPa:.2f} MPa")

with res_col3:
    st.metric(label="Max End Deflection (δ_max)", value=f"{delta_max_mm:.2f} mm")

# Safety Status Flagging
if sigma_max_MPa > yield_strength:
    st.error(
        f"🚨 *FAILURE WARNING:* Bending Stress ({sigma_max_MPa:.2f} MPa) exceeds "
        f"Material Yield Strength ({yield_strength} MPa)! The beam will suffer permanent plastic deformation."
    )
else:
    factor_of_safety = yield_strength / sigma_max_MPa
    st.success(
        f"✅ *DESIGN SAFE:* Bending Stress ({sigma_max_MPa:.2f} MPa) is within "
        f"Yield Strength ({yield_strength} MPa). *Factor of Safety (FOS): {factor_of_safety:.2f}*"
    )

st.markdown("---")

# ==============================================================================
# VISUALIZATION: DEFLECTION CURVE PLOT
# ==============================================================================
st.subheader("📈 Cantilever Beam Deflection Curve")

# x-coordinates along the beam from fixed end (x=0) to free end (x=L)
x = np.linspace(0, length_m, 200)

# Deflection formula along length: v(x) = (P * x^2 * (3L - x)) / (6 * E * I)
# Deflection is downwards, so we negate it for plotting in mm
y_deflection_mm = -((P * (x ** 2) * (3 * length_m - x)) / (6 * E * I)) * 1000.0

fig, ax = plt.subplots(figsize=(10, 4))

# Plot undeformed beam line
ax.plot([0, length_m], [0, 0], 'k--', label="Undeformed Beam Neutral Axis", linewidth=1.5)

# Plot deflected beam curve
ax.plot(x, y_deflection_mm, 'b-', label="Deflected Beam Shape", linewidth=2.5)

# Indicate fixed support at x=0
ax.plot(0, 0, marker='s', markersize=12, color='black', label='Fixed Support (x = 0)')

# Indicate point load at x=L
ax.annotate(
    f'P = {load_kN} kN',
    xy=(length_m, y_deflection_mm[-1]),
    xytext=(length_m * 0.85, y_deflection_mm[-1] * 0.5 if y_deflection_mm[-1] != 0 else 5),
    arrowprops=dict(facecolor='red', shrink=0.05, width=2, headwidth=8),
    fontsize=10,
    color='red',
    weight='bold'
)

ax.set_title("Deflection Profile along Beam Length", fontsize=12, fontweight='bold')
ax.set_xlabel("Position along Beam, x (m)", fontsize=10)
ax.set_ylabel("Deflection, δ (mm)", fontsize=10)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc="lower left")

st.pyplot(fig)

# ==============================================================================
# FORMULAS USED REFERENCE
# ==============================================================================
with st.expander("📚 View Engineering Formulas Used"):
    st.latex(r"Z = \frac{I}{y_{max}}")
    st.latex(r"M_{max} = P \times L")
    st.latex(r"\sigma_{max} = \frac{M_{max}}{Z} = \frac{P \cdot L \cdot y_{max}}{I}")
    st.latex(r"\delta(x) = \frac{P x^2 (3L - x)}{6 E I} \quad \implies \quad \delta_{max} = \frac{P L^3}{3 E I}")
