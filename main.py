import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import os

# 1. Page Config
st.set_page_config(page_title="Ventilation Dashboard", layout="wide")

# --- NAVIGATION LOGIC ---
query_params = st.query_params
current_page = query_params.get("page", "seazero")

# Function to encode local image to base64
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# Path to your logo and SeaZero image
logo_path = "resource\Teknotherm_logo_2020.png"
seazero_img_path = "resource\Screenshot 2026-01-01 173700.png"

logo_base64 = get_base64_of_bin_file(logo_path)
seazero_base64 = get_base64_of_bin_file(seazero_img_path)

logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo-img">' if logo_base64 else '<span class="nav-logo" style="color:#000000; font-weight:900;">TEKNOTHERM</span>'

# Enhanced CSS
st.markdown(f"""
    <style>
    @import url('https://cdn.fontshare.com/vv2/pack.css?family=satoshi@300,400,500,700,900');

    .stApp {{ background-color: #FFFFFF; font-family: 'Satoshi', sans-serif; }}
    .main .block-container {{ padding-top: 0.5rem !important; max-width: 98%; overflow: visible !important; }}

    .nav-container {{ display: flex; justify-content: space-between; align-items: center; padding: 0.1rem 0; background-color: #FFFFFF; margin-bottom: 1.5rem; border: none !important; }}
    .nav-logo-img {{ height: 38px; width: auto; }}
    .nav-menu {{ display: flex; gap: 2rem; margin-right: 3rem; margin-left: auto; }}
    
    .nav-item {{ font-family: 'Satoshi', sans-serif; font-weight: 400; font-size: 14px; color: #000000 !important; text-decoration: none !important; }}
    .active-nav {{ color: #004499 !important; font-weight: 700 !important; }}
    
    .user-profile {{ display: flex; align-items: center; gap: 0.5rem; font-family: 'Satoshi', sans-serif; font-size: 13px; color: #475569; }}

    .main-title {{ font-family: 'Satoshi', sans-serif; font-size: 18px; font-weight: 500; color: #171C35; margin: 0; text-align: left; }}
    
    /* SeaZero Font Styling - High specificity for Satoshi */
    .seazero-content {{ 
        font-family: 'Satoshi', sans-serif !important; 
        font-size: 15px; 
        color: #475569; 
        line-height: 1.8; 
    }}
    .seazero-content p, .seazero-content li, .seazero-content b, .seazero-content span {{ 
        font-family: 'Satoshi', sans-serif !important; 
    }}

    .kpi-container {{ background-color: #F8FAFC; padding: 8px 15px; border-radius: 8px; border: 1px solid #F1F5F9; min-width: 140px; margin-top: 10px; }}
    .kpi-label {{ font-family: 'Satoshi', sans-serif; font-size: 11px; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.02em; }}
    .kpi-value {{ font-family: 'Satoshi', sans-serif; font-size: 18px; font-weight: 500; color: #1E293B; }}

    div[data-testid="stSelectbox"] {{ width: 110px !important; margin-left: auto; }}
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: transparent; border: 1px solid #E2E8F0; border-radius: 6px; min-height: 28px !important; font-size: 13px !important; padding: 0px 4px !important;
    }}
    div[data-testid="stSelectbox"] label {{ display: none; }}
    </style>
    """, unsafe_allow_html=True)

# --- Navigation Bar ---
st.markdown(f"""
    <div class="nav-container">
        <a href="/?page=seazero" target="_self">{logo_html}</a>
        <div class="nav-menu">
            <a class="nav-item {'active-nav' if current_page == 'seazero' else ''}" href="/?page=seazero" target="_self">SeaZero</a>
            <a class="nav-item {'active-nav' if current_page == 'measurement' else ''}" href="/?page=measurement" target="_self">Measurement data</a>
            <a class="nav-item" href="#">Energy Calculation</a>
        </div>
        <div class="user-profile">
            <span>Admin User</span>
            <div class="avatar" style="width: 28px; height: 28px; background-color: #F1F5F9; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: 700; border: 1px solid #E2E8F0;">A</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PAGE CONTENT LOGIC ---

if current_page == "seazero":
    # --- SeaZero Page ---
    st.markdown('<div class="main-title" style="font-size: 18px; font-weight: 500; margin-bottom: 25px;">Introduction of SeaZero</div>', unsafe_allow_html=True)
    
    # --- Section 1: Introduction ---
    col1, col2 = st.columns([6.5, 3.5], gap="large")
    
    with col1:
        st.markdown("""
            <div class="seazero-content">
                <p>The <b>SeaZero</b> research project aims to develop Hurtigruten's next-generation zero-emission vessel in partnership with the research institute SINTEF and 12 maritime industry partners. The project has been awarded €7 million in public funding and has a total budget of €13 million.</p>
                <p>To achieve this ambitious goal, the project explores a wide range of measures to maximize energy efficiency:</p>
                <ul style="color: #475569; padding-left: 20px;">
                    <li>State-of-the-art battery solutions</li>
                    <li>Advanced propulsion technologies</li>
                    <li>Optimized hull design</li>
                    <li>Sustainable shipbuilding practices</li>
                    <li>Smart cabins with real-time energy monitoring</li>
                </ul>
                <p>As a key partner, <b>Teknotherm</b> is responsible for developing a <b>Smart Cabin Concept</b> that enables <b>Demand Control Ventilation (DCV)</b> and <b>real-time monitoring</b> of energy consumption for passengers.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if seazero_base64:
            st.markdown(f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                    <img src="data:image/png;base64,{seazero_base64}" style="width: 100%; border-radius: 12px; border: 1px solid #E2E8F0;">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("SeaZero image not found at the specified path.")

    # --- Section 2: Smart Cabin (Horizontal Divider) ---
    st.markdown("<hr style='border-top: 1px solid #F1F5F9; margin: 40px 0;'>", unsafe_allow_html=True)
    st.markdown('<div class="main-title" style="font-size: 18px; font-weight: 500; margin-bottom: 25px;">Smart Cabin</div>', unsafe_allow_html=True)

    # Two columns for Smart Cabin content and Timeline
    sc_col1, sc_col2 = st.columns([6.5, 3.5], gap="large")


    with sc_col1:
        st.markdown("""
            <div class="seazero-content">
                <p>To realize the Smart Cabin Concept, Teknotherm retrofitted a cabin on the Hurtigruten vessel MS Trollfjord 
                    with demand control ventilation and advanced monitoring.</p>
                <p>By using <b>real-time CO₂ level</b> as an indicator of occupancy, the system automatically 
                    adjusts ventilation rate. This significantly reduces energy consumption during unoccupied periods 
                    without compromising passenger comfort or air quality.</p>
            </div>
        """, unsafe_allow_html=True)

    with sc_col2:
        # Styled Vertical Timeline
        st.markdown("""
            <style>
                .timeline-container { border-left: 2px solid #E2E8F0; padding-left: 20px; margin-left: 10px; position: relative; }
                .timeline-item { position: relative; margin-bottom: 25px; }
                .timeline-dot { position: absolute; left: -27px; top: 10px; width: 12px; height: 12px; background-color: #0EA5E9; border-radius: 50%; border: 2px solid white; }
                .timeline-date { font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
                .timeline-content { font-size: 0.95rem; color: #1E293B; margin-top: 2px; }
                .status-done { background-color: #DCFCE7; color: #166534; font-size: 0.7rem; padding: 2px 8px; border-radius: 10px; margin-left: 5px; font-weight: 700; vertical-align: middle; }
            </style>
            <div class="timeline-container">
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">May 19, 2025</div>
                    <div class="timeline-content">Start Monitoring Phase</div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-date">Nov 10, 2025</div>
                    <div class="timeline-content">DCV Implementation <br><small style="color: #94A3B8;">(First on-boarding)</small></div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-dot" style="background-color: #22C55E;"></div>
                    <div class="timeline-date">Dec 02, 2025</div>
                    <div class="timeline-content">DCV Implementation <span class="status-done">DONE</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

else:
    # --- Measurement Data Page ---
    try:
        dataset_CO2 = pd.read_csv('dataset/updated_file_summary_2025_07_2025_12_co2.csv')
        dataset_velocity = pd.read_csv('dataset/updated_file_summary_2025_07_2025_12_velocity.csv')
        dataset_CO2['Time'] = pd.to_datetime(dataset_CO2['Time'])
        dataset_velocity['Time'] = pd.to_datetime(dataset_velocity['Time'])
        dataset_CO2['Month_Display'] = dataset_CO2['Time'].dt.strftime('%Y.%m')

        kpi_table = {
            "2025.07": {"orig": "1,000", "dcv": "1,000", "save": "0%"},
            "2025.08": {"orig": "1,500", "dcv": "1,500", "save": "0%"},
            "2025.09": {"orig": "2,310", "dcv": "2,310", "save": "0%"},
            "2025.10": {"orig": "1,530", "dcv": "1,530", "save": "0%"},
            "2025.11": {"orig": "1,500", "dcv": "900", "save": "30%"},
            "2025.12": {"orig": "1,400", "dcv": "1,000", "save": "25%"}
        }

        header_col, selector_col = st.columns([8, 2])
        with header_col:
            st.markdown('<div class="main-title">Demand Control Ventilation of the Smart Cabin in Hurtigruten MS Trollfjord</div>', unsafe_allow_html=True)
        with selector_col:
            display_options = sorted(list(kpi_table.keys()))
            selected_display = st.selectbox("", options=display_options, index=0)

        monthly_values = kpi_table.get(selected_display, {"orig": "0", "dcv": "0", "save": "0%"})
        kpi_1, kpi_2, kpi_3, kpi_spacer = st.columns([1.2, 1.2, 1.2, 6])

        with kpi_1:
            st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Original Volume</div><div class="kpi-value">{monthly_values['orig']} m³</div></div>""", unsafe_allow_html=True)
        with kpi_2:
            st.markdown(f"""<div class="kpi-container"><div class="kpi-label">DCV Volume</div><div class="kpi-value">{monthly_values['dcv']} m³</div></div>""", unsafe_allow_html=True)
        with kpi_3:
            st.markdown(f"""<div class="kpi-container"><div class="kpi-label">Saving</div><div class="kpi-value" style="color: #10B981;">{monthly_values['save']}</div></div>""", unsafe_allow_html=True)

        f_co2 = dataset_CO2[dataset_CO2['Month_Display'] == selected_display]
        f_vel = dataset_velocity[pd.to_datetime(dataset_velocity['Time']).dt.strftime('%Y.%m') == selected_display]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=("CO2 Concentration (ppm)", "VAV Supply Air Velocity (m/s)"))
        fig.add_trace(go.Scatter(x=f_co2['Time'], y=f_co2['CO2_SENSOR'], mode='lines', line=dict(color='#ff730f', width=1), fill='tozeroy', fillcolor='rgba(255, 115, 15, 0.05)'), row=1, col=1)
        fig.add_trace(go.Scatter(x=f_vel['Time'], y=f_vel['SmartCabin - Supply velocity'], mode='lines', line=dict(color='#004499', width=1), fill='tozeroy', fillcolor='rgba(0, 68, 153, 0.05)'), row=2, col=1)

        fig.update_layout(height=500, margin=dict(l=0, r=0, t=50, b=20), showlegend=False, template="plotly_white", hovermode="x unified")
        fig.update_annotations(font_size=13, font_family="Satoshi, sans-serif", x=0, xanchor='left')
        fig.update_xaxes(showline=False, zeroline=False, gridcolor='#F5F5F5')
        fig.update_yaxes(showline=False, zeroline=False, gridcolor='#F5F5F5')
        fig.update_yaxes(range=[300, f_co2['CO2_SENSOR'].max() * 1.1], row=1, col=1)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except Exception as e:

        st.error(f"Error loading datasets: {e}")

