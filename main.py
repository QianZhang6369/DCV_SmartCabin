import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import os
import numpy as np

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
logo_path = "resource/Teknotherm_logo_2020.png"
seazero_img_path = "resource/Screenshot 2026-01-01 173700.png"

logo_base64 = get_base64_of_bin_file(logo_path)
seazero_base64 = get_base64_of_bin_file(seazero_img_path)

logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="nav-logo-img">' if logo_base64 else '<span class="nav-logo" style="color:#000000; font-weight:900;">TEKNOTHERM</span>'

# Enhanced CSS (Consolidated)
st.markdown(f"""
    <style>
    @import url('https://cdn.fontshare.com/vv2/pack.css?family=satoshi@300,400,500,700,900');

    .stApp {{ background-color: #FFFFFF; font-family: 'Satoshi', sans-serif; }}
    .main .block-container {{ padding-top: 0.5rem !important; max-width: 98%; overflow: visible !important; }}

    /* Navigation */
    .nav-container {{ display: flex; justify-content: space-between; align-items: center; padding: 0.1rem 0; background-color: #FFFFFF; margin-bottom: 1.5rem; border: none !important; }}
    .nav-logo-img {{ height: 38px; width: auto; }}
    .nav-menu {{ display: flex; gap: 2rem; margin-right: 3rem; margin-left: auto; }}
    .nav-item {{ font-family: 'Satoshi', sans-serif; font-weight: 400; font-size: 14px; color: #000000 !important; text-decoration: none !important; }}
    .active-nav {{ color: #004499 !important; font-weight: 700 !important; }}
    .user-profile {{ display: flex; align-items: center; gap: 0.5rem; font-family: 'Satoshi', sans-serif; font-size: 13px; color: #475569; }}

    /* Titles & Content */
    .main-title {{ font-family: 'Satoshi', sans-serif; font-size: 18px; font-weight: 500; color: #171C35; margin: 0; text-align: left; }}
    .seazero-content {{ font-family: 'Satoshi', sans-serif !important; font-size: 15px; color: #475569; line-height: 1.8; }}

    /* Shared Result/KPI Cards */
    .result-card {{
        background: white;
        border: 1px solid #e2e8f0;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    .kpi-label-alt {{
        color: #64748b;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    .kpi-value-alt {{
        color: #1e293b;
        font-size: 20px;
        font-weight: 700;
        margin-top: 4px;
    }}
    .saving-badge {{
        display: inline-flex;
        align-items: center;
        background-color: #dcfce7;
        color: #15803d;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 8px;
    }}

    /* Selectbox Styling */
    div[data-testid="stSelectbox"] {{ width: 110px !important; margin-left: auto; }}
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: transparent; border: 1px solid #E2E8F0; border-radius: 6px; min-height: 28px !important; font-size: 13px !important; padding: 0px 4px !important;
    }}
    div[data-testid="stSelectbox"] label {{ display: none; }}

    /* Energy Page Specifics */
    div.stButton > button:first-child {{
        background-color: #004499; color: white; border-radius: 6px; padding: 0.6rem 2rem; border: none; font-weight: 600; font-size: 13px !important; width: 200px; margin-top: 30px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- Navigation Bar ---
st.markdown(f"""
    <div class="nav-container">
        <a href="/?page=seazero" target="_self">{logo_html}</a>
        <div class="nav-menu">
            <a class="nav-item {'active-nav' if current_page == 'seazero' else ''}" href="/?page=seazero" target="_self">SeaZero</a>
            <a class="nav-item {'active-nav' if current_page == 'measurement' else ''}" href="/?page=measurement" target="_self">Measurement data</a>
            <a class="nav-item {'active-nav' if current_page == 'energy' else ''}" href="/?page=energy" target="_self">Energy Calculation</a>
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

elif current_page == "measurement":
    try:
        dataset_CO2 = pd.read_csv('dataset/updated_file_summary_2025_07_2025_12_co2.csv')
        dataset_velocity = pd.read_csv('dataset/updated_file_summary_2025_07_2025_12_velocity.csv')
        dataset_CO2['Time'] = pd.to_datetime(dataset_CO2['Time'])
        dataset_velocity['Time'] = pd.to_datetime(dataset_velocity['Time'])
        dataset_CO2['Month_Display'] = dataset_CO2['Time'].dt.strftime('%Y.%m')

        kpi_table = {
            "2025.07": {"orig": "57,862", "dcv": "57,862", "save": "0%"},
            "2025.08": {"orig": "57,862", "dcv": "57,862", "save": "0%"},
            "2025.09": {"orig": "55,956", "dcv": "55,956", "save": "0%"},
            "2025.10": {"orig": "57,862", "dcv": "57,862", "save": "0%"},
            "2025.11": {"orig": "55,956", "dcv": "32,148", "save": "42.5%"},
            "2025.12": {"orig": "57,862", "dcv": "38,635", "save": "33.2%"}
        }

        header_col, selector_col = st.columns([8, 2])
        with header_col:
            st.markdown('<div class="main-title">Demand Control Ventilation of the Smart Cabin in Hurtigruten MS Trollfjord</div>', unsafe_allow_html=True)
        with selector_col:
            display_options = sorted(list(kpi_table.keys()))
            selected_display = st.selectbox("", options=display_options, index=5)

        monthly_values = kpi_table.get(selected_display, {"orig": "0", "dcv": "0", "save": "0%"})
        
        # Updated KPI Section using Energy Result Card format
        kpi_1, kpi_2, kpi_3, kpi_spacer = st.columns([1.5, 1.5, 1.5, 5.5])
        with kpi_1:
            st.markdown(f'<div class="result-card"><div class="kpi-label-alt">Original Volume</div><div class="kpi-value-alt">{monthly_values["orig"]}<span style="font-size:11px;"> m³</span></div></div>', unsafe_allow_html=True)
        with kpi_2:
            st.markdown(f'<div class="result-card"><div class="kpi-label-alt">DCV Volume</div><div class="kpi-value-alt">{monthly_values["dcv"]}<span style="font-size:11px;"> m³</span></div></div>', unsafe_allow_html=True)
        with kpi_3:
            st.markdown(f"""
                <div class="result-card" style="border-color: #86efac; background-color: #f0fdf4;">
                    <div class="kpi-label-alt" style="color: #15803d;">Fresh Air Amount Savings</div>
                    <div style="display: flex; align-items: baseline; margin-top: 4px;">
                        <span style="color: #15803d; font-size: 20px; font-weight: 700;">{monthly_values["save"]}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        f_co2 = dataset_CO2[dataset_CO2['Month_Display'] == selected_display]
        f_vel = dataset_velocity[dataset_velocity['Time'].dt.strftime('%Y.%m') == selected_display]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=("CO2 Concentration (ppm)", "VAV Supply Air Velocity (m/s)"))
        fig.add_trace(go.Scatter(x=f_co2['Time'], y=f_co2['CO2_SENSOR'], mode='lines', line=dict(color='#ff730f', width=1), fill='tozeroy', fillcolor='rgba(255, 115, 15, 0.05)'), row=1, col=1)
        fig.add_trace(go.Scatter(x=f_vel['Time'], y=f_vel['SmartCabin - Supply velocity'], mode='lines', line=dict(color='#004499', width=1), fill='tozeroy', fillcolor='rgba(0, 68, 153, 0.05)'), row=2, col=1)
        fig.update_layout(height=500, margin=dict(l=0, r=0, t=50, b=20), showlegend=False, template="plotly_white")
        fig.update_annotations(
                font_size=13, 
                font_family="Satoshi, sans-serif",
                x=0.5, 
                xanchor='left'
            )
        fig.update_xaxes(tickfont=dict(size=12), gridcolor='#F5F5F5')
        fig.update_yaxes(tickfont=dict(size=12), gridcolor='#F5F5F5')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except Exception as e:
        st.error(f"Error loading datasets: {e}")


elif current_page == "energy":
    # --- 1. CONSOLIDATED CSS STYLING ---
    st.markdown("""
        <style>
        /* Input constraints */
        div[data-testid="stTextInput"] { width: 250px !important; }
        div[data-testid="stSelectbox"] { width: 250px !important; margin-left: 0 !important; }
        
        /* Action Button */
        div.stButton > button:first-child {
            background-color: #004499;
            color: white;
            border-radius: 6px;
            padding: 0.6rem 2rem;
            border: none;
            font-weight: 600;
            font-size: 13px !important;
            width: 200px;
            margin-top: 30px;
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: #003377;
            border-color: #003377;
            color: white;
        }

        /* Result Cards */
        .result-card {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 16px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .kpi-label-alt {
            color: #64748b;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .kpi-value-alt {
            color: #1e293b;
            font-size: 20px;
            font-weight: 700;
            margin-top: 4px;
        }
        .saving-badge {
            display: inline-flex;
            align-items: center;
            background-color: #dcfce7;
            color: #15803d;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            margin-left: 8px;
        }

        /* Improved Popover Assumption UI */
        div[data-testid="stPopover"] > button {
            border: none !important;
            background-color: transparent !important;
            padding: 0 !important;
            font-size: 18px !important;
            color: #94A3B8 !important;
            margin-left: -10px !important;
        }
        .assumption-container { min-width: 300px; padding: 10px 5px; }
        .spec-header {
            font-size: 0.75rem; font-weight: 800; text-transform: uppercase;
            color: #004499; margin-bottom: 12px; border-bottom: 2px solid #e2e8f0; padding-bottom: 4px;
        }
        .spec-item { margin-bottom: 16px; }
        .spec-label { font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 2px; }
        .spec-desc { font-size: 12px; color: #64748b; line-height: 1.4; }
        .formula-tag {
            display: inline-block; background: #f1f5f9; color: #004499; padding: 4px 8px;
            border-radius: 4px; font-family: monospace; font-weight: 700; font-size: 11px;
            margin-top: 6px; border: 1px solid #e2e8f0;
        }
                
        /* --- SMALL FLOATING DROP-UP CSS --- */
        .footer-fixed-wrapper {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            z-index: 999;
            background-color: white;
            border-top: 1px solid #e2e8f0;
        }

        details {
            display: flex;
            flex-direction: column-reverse;
        }

        summary {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 40px;
            cursor: pointer;
            list-style: none;
            background-color: white;
        }

        summary::-webkit-details-marker { display: none; }

        /* The Smaller Assumption Box */
        .dropup-content {
            position: absolute;
            bottom: 60px; /* Sits exactly above the footer bar */
            left: 40px;   /* Aligned with the 'Calculation Assumptions' text */
            width: 350px; /* Controlled width for a smaller box */
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            box-shadow: 0 -10px 25px rgba(0,0,0,0.1); /* Shadow to make it 'pop' */
            max-height: 400px;
            overflow-y: auto;
        }

        .footer-nav-label {
            color: #004499;
            font-weight: 400;
            font-size: 12px;
            letter-spacing: 0.5px;
        }

        .footer-copyright {
            font-size: 11px;
            color: #94a3b8;
        }

        /* Content inside the small box */
        .inner-markdown h4 { 
            color: #004499; 
            font-size: 14px; 
            margin-top: 0; 
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 8px;
        }
        .inner-markdown p, .inner-markdown li { 
            color: #475569; 
            font-size: 12px; 
            line-height: 1.5; 
        }
        .formula-box {
            background: #f8fafc;
            padding: 8px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 11px;
            margin: 10px 0;
            border: 1px solid #e2e8f0;
            color: #004499;
        }

        </style>
    """, unsafe_allow_html=True)

    # --- 2. PAGE LAYOUT ---
    left_col, right_col = st.columns([1, 2], gap="large")

    with left_col:
        st.markdown('<p style="font-weight: 700; color: #1E293B; font-size: 16px; margin-bottom: 0;">Cabin Configuration</p>', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        
        # Cabin Input (Converted to int for the function)
        cabin_input = st.text_input("Total Vessel Cabins", value="120")
        
        st.markdown('<p style="font-size: 14px; margin-bottom: 8px; font-weight: 500;">Sailing Route</p>', unsafe_allow_html=True)
        route = st.selectbox("", options=["Oslo - Honningsvåg - Oslo", "Bergen - Kirkenes - Bergen"], index=0, label_visibility="collapsed")
        
        run_calc = st.button("Run Calculation")

    # --- 3. COMPUTATION LOGIC ---
    with right_col:
        if run_calc:
            try:
                # Local paths (Update these to your local or relative Streamlit paths)
                weather_path = "dataset/hourly_schedule_weather - Copy.csv"
                velocity_path = "dataset/VAV_velocity_Oslo-Honningsvåg-Oslo.csv"
                
                # Input conversion
                num_cabins = int(cabin_input)

                # Physics & Data Processing
                # (Integrating your logic here)
                from CoolProp.HumidAirProp import HAPropsSI
                
                # Data Loading
                df_w = pd.read_csv(weather_path)
                df_w['time'] = pd.to_datetime(df_w['time'])
                df_w = df_w.groupby('time').mean().resample('10T').interpolate(method='linear')

                df_v = pd.read_csv(velocity_path)
                df_v['Time'] = pd.to_datetime(df_v['Time'])
                df_v = df_v.groupby('Time').mean().resample('10T').mean()

                full_year_index = pd.date_range(start='2025-01-01 00:00:00', end='2025-12-31 23:50:00', freq='10T')
                master_df = pd.DataFrame(index=full_year_index).join(df_w, how='left').join(df_v, how='left')

                # Constants
                P_asm, T_supply_c, RH_supply = 101325, 15, 0.85
                duct_diameter_m, design_flow_per_cabin = 0.08, 85
                SFP, COP, dt = 2.5, 3.0, 10 / 60

                # Physics Calculations
                h_supply = HAPropsSI('H', 'T', T_supply_c + 273.15, 'P', P_asm, 'R', RH_supply) / 1000.0
                
                master_df['ambient_enthalpy_kj_kg'] = master_df.apply(lambda x: HAPropsSI('H', 'T', x['temperature_2m'] + 273.15, 'P', P_asm, 'R', x['relative_humidity_2m']/100.0)/1000.0 if not np.isnan(x['temperature_2m']) else np.nan, axis=1)
                master_df['air_density_kg_m3'] = master_df.apply(lambda x: 1.0/HAPropsSI('V', 'T', x['temperature_2m'] + 273.15, 'P', P_asm, 'R', x['relative_humidity_2m']/100.0) if not np.isnan(x['temperature_2m']) and x['temperature_2m'] != 0 else 1.225, axis=1)

                # Flow Rates
                master_df['actual_flow_rate_m3h'] = master_df['Velocity'] * (np.pi * (duct_diameter_m/2)**2) * 3600 * num_cabins
                design_total_flow = design_flow_per_cabin * num_cabins
                master_df['vessel_design_flow_m3h'] = np.where(master_df['Velocity'].isna(), np.nan, design_total_flow)

                # Power Formulas
                design_fan_power_kw_const = (design_total_flow / 3600) * SFP
                
                def fan_poly(flow, d_flow):
                    if d_flow <= 0 or flow <= 0 or np.isnan(flow): return 0.0
                    x = flow / d_flow
                    return (0.0013 + 0.147*x + 0.9506*x**2 - 0.0998*x**3) * design_fan_power_kw_const

                master_df['actual_fan_power_kw'] = np.vectorize(fan_poly)(master_df['actual_flow_rate_m3h'], master_df['vessel_design_flow_m3h'])
                master_df['design_fan_power_kw'] = np.where(master_df['vessel_design_flow_m3h'] > 0, design_fan_power_kw_const, 0)

                # ... [Previous physics calculations remain the same until Energy Integration] ...

                # --- NEW: TIME-BASED FILTERING FOR HEATING ---
                # We calculate heating power for the whole year, 
                # then zero out any values outside 08:00 - 14:00.
                master_df['actual_heating_kw'] = master_df.apply(
                    lambda x: ((x['actual_flow_rate_m3h']/3600)*x['air_density_kg_m3']*(h_supply - x['ambient_enthalpy_kj_kg']))/COP 
                    if x['ambient_enthalpy_kj_kg'] < h_supply else 0, axis=1
                )
                master_df['design_heating_kw'] = master_df.apply(
                    lambda x: ((x['vessel_design_flow_m3h']/3600)*x['air_density_kg_m3']*(h_supply - x['ambient_enthalpy_kj_kg']))/COP 
                    if x['ambient_enthalpy_kj_kg'] < h_supply else 0, axis=1
                )

                # Create a mask: True only between 08:00 and 14:00
                heating_mask = (master_df.index.hour >= 8) & (master_df.index.hour < 14)
                
                # Apply the mask to heating columns (Zero out everything else)
                master_df.loc[~heating_mask, 'actual_heating_kw'] = 0
                master_df.loc[~heating_mask, 'design_heating_kw'] = 0

                # --- ENERGY INTEGRATION ---
                # Ventilation Fans (Running 24/7)
                fan_orig = (((master_df['design_fan_power_kw'] + master_df['design_fan_power_kw'].shift(1, fill_value=0)) / 2) * dt).sum()
                fan_dcv = (((master_df['actual_fan_power_kw'] + master_df['actual_fan_power_kw'].shift(1, fill_value=0)) / 2) * dt).sum()
                
                # Heating (Now restricted by the mask above)
                heat_orig = (((master_df['design_heating_kw'] + master_df['design_heating_kw'].shift(1, fill_value=0)) / 2) * dt).sum()
                heat_dcv = (((master_df['actual_heating_kw'] + master_df['actual_heating_kw'].shift(1, fill_value=0)) / 2) * dt).sum()

                # --- UI DISPLAY ---
                # [Rest of the code follows...]
                # UI Display
                st.markdown('<p style="font-weight: 700; color: #1E293B; font-size: 18px; margin-bottom: 20px;">Detailed Calculation Results</p>', unsafe_allow_html=True)
                
                results = [
                    ("Ventilation Fan System", fan_orig, fan_dcv, "#004499"),
                    ("Heating System", heat_orig, heat_dcv, "#950606")
                ]

                for title, orig, dcv, color in results:
                    save = orig - dcv
                    pct = (save / orig * 100) if orig > 0 else 0
                    st.markdown(f'<p style="font-weight: 700; color: {color}; font-size: 12px; margin-top: 20px; text-transform: uppercase;">{title}</p>', unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    with c1: st.markdown(f'<div class="result-card"><div class="kpi-label-alt">Baseline</div><div class="kpi-value-alt">{orig:,.0f}<span style="font-size:11px;"> kWh</span></div></div>', unsafe_allow_html=True)
                    with c2: st.markdown(f'<div class="result-card"><div class="kpi-label-alt">DCV Mode</div><div class="kpi-value-alt">{dcv:,.0f}<span style="font-size:11px;"> kWh</span></div></div>', unsafe_allow_html=True)
                    with c3: st.markdown(f'<div class="result-card" style="border-color: #86efac; background-color: #f0fdf4;"><div class="kpi-label-alt" style="color: #15803d;">Savings</div><div style="display: flex; align-items: baseline; margin-top: 4px;"><span style="color: #15803d; font-size: 20px; font-weight: 700;">{save:,.0f}</span><span style="color: #15803d; font-size: 11px; font-weight: 600; margin-left: 4px;">kWh</span><span class="saving-badge">-{pct:.1f}%</span></div></div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Calculation Error: {e}. Please check if dataset files exist in the /dataset directory.")
        else:
            st.markdown("""
                <div style="border: 2px dashed #E2E8F0; border-radius: 12px; height: 450px; display: flex; align-items: center; justify-content: center; color: #94A3B8; text-align: center;">
                    <div><p style="font-size: 48px; margin-bottom: 10px;">🍃</p><p style="font-weight: 500; color: #64748B;">Ready to Calculate</p><p style="font-size: 13px;">Adjust parameter and run calculation.</p></div>
                </div>
            """, unsafe_allow_html=True)
    # --- 3. STABLE FOOTER WITH SMALL FLOATING BOX ---
    st.markdown("""
        <div class="footer-fixed-wrapper">
            <details>
                <div class="dropup-content">
                    <div class="inner-markdown">
                        <h4>Assumptions</h4>
                        <ul>
                            <li>Sailing Route: Oslo - Honningsvåg - Oslo with 14 round-trip sailings; schedule via official website.</li>
                            <li>Data: December's smart cabin flow rates (extrapolated for the full year).</li>
                            <li>AHU Total Flow Rate: Flow rates determined by cabin number & smart cabin usage.</li>
                            <li>Fan: Fan energy consumption follows ASHRAE 90.1-2019.</li>
                        </ul>
                    </div>
                </div>
                <summary>
                    <div class="footer-nav-label">▲ Calculation Assumptions</div>
                    <div class="footer-copyright">© 2026 Teknotherm sales tool for Demand Control Ventilation</div>
                </summary>
            </details>
        </div>
        <div style="margin-bottom: 80px;"></div>
    """, unsafe_allow_html=True)