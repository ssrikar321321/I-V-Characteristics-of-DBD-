#!/usr/bin/env python3
"""
Enhanced Discharge I-V Analysis Tool
Comprehensive analysis with publication-ready dual-axis plots

Copyright (c) 2024 P. Srikar
All rights reserved.

When using this tool in research or publications, please cite:
    Srikar, P. (2024). Enhanced Discharge I-V Analysis Tool. 
    GitHub repository: https://github.com/ssrikar321321/I-V-Characteristics-of-DBD-

License: MIT License
For full license text, see LICENSE file.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Page config
st.set_page_config(page_title="Enhanced I-V Analyzer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main {padding: 0rem 1rem;}
    .stButton>button {width: 100%;}
    h1 {color: #1f77b4;}
    .metric-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Enhanced Discharge I-V Analysis")

# Sidebar
with st.sidebar:
    st.header("📁 Upload Files")
    w1_v_file = st.file_uploader("W1 Voltage CSV", type=['csv'], key='w1v')
    w1_i_file = st.file_uploader("W1 Current CSV", type=['csv'], key='w1i')
    w2_v_file = st.file_uploader("W2 Voltage CSV", type=['csv'], key='w2v')
    w2_i_file = st.file_uploader("W2 Current CSV", type=['csv'], key='w2i')
    
    st.divider()
    st.header("⚙️ Settings")
    frequency = st.number_input("Frequency (Hz)", value=20000, step=1000)
    phase_offset = st.slider("W2 Phase Offset (°)", 0, 360, 180)
    
    st.divider()
    st.header("🎨 Display")
    line_width = st.slider("Line Width", 1.0, 4.0, 2.0, 0.5)
    show_grid = st.checkbox("Show Grid", value=True)
    plot_height = st.slider("Plot Height (px)", 400, 1000, 600, 50)
    
    st.divider()
    
    # About & Citation section
    with st.expander("ℹ️ About & Citation"):
        st.markdown("""
        **Enhanced Discharge I-V Analyzer**
        
        **Author:** P. Srikar  
        **Year:** 2024  
        **License:** MIT License
        
        ---
        
        **Citation:**
        ```
        Srikar, P. (2024). Enhanced Discharge 
        I-V Analysis Tool. 
        https://github.com/YOUR_USERNAME/
        discharge-iv-analyzer
        ```
        
        **BibTeX:**
        ```bibtex
        @software{srikar2024ivanalyzer,
          author = {Srikar, P.},
          title = {Enhanced Discharge I-V 
                   Analysis Tool},
          year = {2024},
          url = {https://github.com/YOUR_USERNAME/
                 discharge-iv-analyzer}
        }
        ```
        
        ---
        
        © 2024 P. Srikar. All rights reserved.
        """)

@st.cache_data
def load_csv(file):
    if file is None:
        return None
    df = pd.read_csv(file, skiprows=16)
    return {'time': df.iloc[:, 0].values, 'signal': df.iloc[:, 1].values}

def calculate_metrics(time, voltage, current, frequency):
    dt = time[-1] - time[0]
    power_inst = voltage * current
    power_inst_abs = np.abs(power_inst)
    
    return {
        'time': time,
        'voltage': voltage,
        'current': current,
        'power_signed': power_inst,
        'power_rectified': power_inst_abs,
        'avg_voltage': np.trapezoid(np.abs(voltage), time) / dt,
        'avg_current': np.trapezoid(np.abs(current), time) / dt,
        'avg_power_signed': np.trapezoid(power_inst, time) / dt,
        'avg_power_rectified': np.trapezoid(power_inst_abs, time) / dt,
        'v_rms': np.sqrt(np.trapezoid(voltage**2, time) / dt),
        'i_rms': np.sqrt(np.trapezoid(current**2, time) / dt),
        'v_peak': np.max(np.abs(voltage)),
        'i_peak': np.max(np.abs(current)),
        'p_peak': np.max(power_inst_abs),
        'energy_per_cycle': np.trapezoid(power_inst_abs, time) / dt / frequency if frequency > 0 else 0,
        'power_factor': np.trapezoid(power_inst, time) / dt / (np.sqrt(np.trapezoid(voltage**2, time) / dt) * np.sqrt(np.trapezoid(current**2, time) / dt)) if np.sqrt(np.trapezoid(voltage**2, time) / dt) * np.sqrt(np.trapezoid(current**2, time) / dt) > 0 else 0,
        'apparent_power': np.sqrt(np.trapezoid(voltage**2, time) / dt) * np.sqrt(np.trapezoid(current**2, time) / dt)
    }

data = {k: load_csv(v) for k, v in {'w1_v': w1_v_file, 'w1_i': w1_i_file, 'w2_v': w2_v_file, 'w2_i': w2_i_file}.items()}
all_loaded = all(v is not None for v in data.values())

if all_loaded:
    phase_shift = (phase_offset / 360) / frequency
    t_w1 = (data['w1_v']['time'] - data['w1_v']['time'][0]) * 1e6
    t_w2 = (data['w2_v']['time'] + phase_shift - data['w2_v']['time'][0]) * 1e6
    
    v1, i1 = data['w1_v']['signal'], data['w1_i']['signal']
    v2, i2 = data['w2_v']['signal'], data['w2_i']['signal']
    
    metrics_w1 = calculate_metrics(t_w1*1e-6, v1, i1, frequency)
    metrics_w2 = calculate_metrics(t_w2*1e-6, v2, i2, frequency)
    
    total_power = metrics_w1['avg_power_rectified'] + metrics_w2['avg_power_rectified']
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📊 Comprehensive Analysis")
        
        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=('Voltage', 'Current', 'Power (Rectified)', 'Power (Signed)', 
                          'Lissajous W1', 'Lissajous W2', 'Power Bars', 'Phase'),
            specs=[[{}, {}], [{}, {}], [{}, {}], [{"type": "bar"}, {}]],
            vertical_spacing=0.08, horizontal_spacing=0.1
        )
        
        # Voltage & Current
        for t, v, name, color in [(t_w1, v1, 'W1', 'red'), (t_w2, v2, 'W2', 'blue')]:
            fig.add_trace(go.Scatter(x=t, y=v, name=name, line=dict(color=color, width=line_width)), row=1, col=1)
        for t, i, color in [(t_w1, i1, 'red'), (t_w2, i2, 'blue')]:
            fig.add_trace(go.Scatter(x=t, y=i*1e3, showlegend=False, line=dict(color=color, width=line_width)), row=1, col=2)
        
        # Power
        for t, p, color in [(t_w1, metrics_w1['power_rectified'], 'red'), (t_w2, metrics_w2['power_rectified'], 'blue')]:
            fig.add_trace(go.Scatter(x=t, y=p, showlegend=False, line=dict(color=color, width=line_width)), row=2, col=1)
        for t, p, color in [(t_w1, metrics_w1['power_signed'], 'red'), (t_w2, metrics_w2['power_signed'], 'blue')]:
            fig.add_trace(go.Scatter(x=t, y=p, showlegend=False, line=dict(color=color, width=line_width)), row=2, col=2)
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=2)
        
        # Lissajous
        fig.add_trace(go.Scatter(x=v1, y=i1*1e3, mode='lines', showlegend=False, line=dict(color='red', width=line_width)), row=3, col=1)
        fig.add_trace(go.Scatter(x=v2, y=i2*1e3, mode='lines', showlegend=False, line=dict(color='blue', width=line_width)), row=3, col=2)
        
        # Power bars
        fig.add_trace(go.Bar(x=['W1', 'W2', 'Total'], 
                            y=[metrics_w1['avg_power_rectified'], metrics_w2['avg_power_rectified'], total_power],
                            marker_color=['red', 'blue', 'green'], showlegend=False), row=4, col=1)
        
        # Phase
        v1_norm = v1 / np.max(np.abs(v1))
        i1_norm = i1 / np.max(np.abs(i1))
        fig.add_trace(go.Scatter(x=t_w1, y=v1_norm, name='V', line=dict(color='red', width=line_width)), row=4, col=2)
        fig.add_trace(go.Scatter(x=t_w1, y=i1_norm, name='I', line=dict(color='orange', width=line_width, dash='dash')), row=4, col=2)
        
        # Update axes
        for i in range(1, 5):
            for j in range(1, 3):
                fig.update_xaxes(showgrid=show_grid, row=i, col=j)
                fig.update_yaxes(showgrid=show_grid, row=i, col=j)
        
        fig.update_xaxes(title_text="Time (µs)", row=1, col=1)
        fig.update_xaxes(title_text="Time (µs)", row=1, col=2)
        fig.update_yaxes(title_text="Voltage (V)", row=1, col=1)
        fig.update_yaxes(title_text="Current (mA)", row=1, col=2)
        fig.update_yaxes(title_text="Power (W)", row=2, col=1)
        fig.update_yaxes(title_text="Power (W)", row=2, col=2)
        fig.update_xaxes(title_text="Voltage (V)", row=3, col=1)
        fig.update_xaxes(title_text="Voltage (V)", row=3, col=2)
        fig.update_yaxes(title_text="Current (mA)", row=3, col=1)
        fig.update_yaxes(title_text="Current (mA)", row=3, col=2)
        fig.update_yaxes(title_text="Power (W)", row=4, col=1)
        fig.update_yaxes(title_text="Normalized", row=4, col=2)
        
        fig.update_layout(height=plot_height*1.5, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Metrics")
        
        st.markdown(f"### 🔥 Total Power")
        st.markdown(f"<div class='metric-box'><h2 style='color: green;'>{total_power:.2f} W</h2></div>", unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### ⚡ Electrode 1")
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | V_RMS | {metrics_w1['v_rms']:.0f} V |
        | I_RMS | {metrics_w1['i_rms']*1e3:.2f} mA |
        | V_peak | {metrics_w1['v_peak']:.0f} V |
        | I_peak | {metrics_w1['i_peak']*1e3:.2f} mA |
        | **Power** | **{metrics_w1['avg_power_rectified']:.2f} W** |
        | P_peak | {metrics_w1['p_peak']:.2f} W |
        | Energy/cyc | {metrics_w1['energy_per_cycle']*1e6:.1f} µJ |
        | PF | {metrics_w1['power_factor']:.3f} |
        """)
        
        st.divider()
        st.markdown("### ⚡ Electrode 2")
        st.markdown(f"""
        | Metric | Value |
        |--------|-------|
        | V_RMS | {metrics_w2['v_rms']:.0f} V |
        | I_RMS | {metrics_w2['i_rms']*1e3:.2f} mA |
        | V_peak | {metrics_w2['v_peak']:.0f} V |
        | I_peak | {metrics_w2['i_peak']*1e3:.2f} mA |
        | **Power** | **{metrics_w2['avg_power_rectified']:.2f} W** |
        | P_peak | {metrics_w2['p_peak']:.2f} W |
        | Energy/cyc | {metrics_w2['energy_per_cycle']*1e6:.1f} µJ |
        | PF | {metrics_w2['power_factor']:.3f} |
        """)
    
    # Export
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        export_df = pd.DataFrame({
            'Time_W1_us': t_w1, 'W1_V': v1, 'W1_mA': i1*1e3, 'W1_P': metrics_w1['power_rectified'],
            'Time_W2_us': t_w2, 'W2_V': v2, 'W2_mA': i2*1e3, 'W2_P': metrics_w2['power_rectified']
        })
        st.download_button("📥 CSV", export_df.to_csv(index=False), "data.csv", "text/csv")
    
    with col2:
        st.download_button("📊 HTML Plot", fig.to_html(), "plot.html", "text/html")
    
    # Publication Plot
    st.divider()
    st.subheader("🎨 Publication Dual-Axis I-V Plots")
    
    with st.expander("📐 Customize & Preview", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            pub_w = st.number_input("Width (in)", value=7, min_value=4, max_value=20)
            pub_h = st.number_input("Height (in)", value=5, min_value=3, max_value=15)
            pub_dpi = st.selectbox("DPI", [150, 300, 600], index=1)
        with col2:
            font_sz = st.number_input("Font Size", value=12, min_value=8, max_value=24)
            pub_lw = st.number_input("Line Width", value=2.0, min_value=0.5, max_value=5.0, step=0.5)
            marker_sz = st.number_input("Marker Size", value=0, min_value=0, max_value=10)
        with col3:
            leg_loc = st.selectbox("Legend", ['best', 'upper right', 'upper left', 'lower right', 'lower left'], index=1)
            grid_a = st.slider("Grid Alpha", 0.0, 1.0, 0.3, 0.1)
            minor_g = st.checkbox("Minor Grid", False)
        
        if st.button("👁️ Preview & Download", type="primary"):
            with st.spinner("Generating..."):
                fig_pub, (ax1, ax2) = plt.subplots(1, 2, figsize=(pub_w, pub_h))
                
                # W1
                ax1_v = ax1
                ax1_v.set_xlabel('Time (µs)', fontsize=font_sz)
                ax1_v.set_ylabel('Voltage (V)', color='tab:red', fontsize=font_sz)
                l1 = ax1_v.plot(t_w1, v1, 'tab:red', linewidth=pub_lw, 
                               marker='o' if marker_sz > 0 else '', markersize=marker_sz, label='Voltage')
                ax1_v.tick_params(axis='y', labelcolor='tab:red', labelsize=font_sz*0.9)
                ax1_v.tick_params(axis='x', labelsize=font_sz*0.9)
                
                ax1_i = ax1.twinx()
                ax1_i.set_ylabel('Current (mA)', color='tab:orange', fontsize=font_sz)
                l2 = ax1_i.plot(t_w1, i1*1e3, 'tab:orange', linewidth=pub_lw, linestyle='--',
                               marker='s' if marker_sz > 0 else '', markersize=marker_sz, label='Current')
                ax1_i.tick_params(axis='y', labelcolor='tab:orange', labelsize=font_sz*0.9)
                
                ax1.set_title('Electrode 1 (W1)', fontsize=font_sz*1.2, fontweight='bold')
                ax1.grid(True, alpha=grid_a)
                if minor_g:
                    ax1.minorticks_on()
                    ax1.grid(True, which='minor', alpha=grid_a/2)
                
                lines = l1 + l2
                ax1.legend(lines, [l.get_label() for l in lines], loc=leg_loc, fontsize=font_sz*0.9)
                
                # W2
                ax2_v = ax2
                ax2_v.set_xlabel('Time (µs)', fontsize=font_sz)
                ax2_v.set_ylabel('Voltage (V)', color='tab:blue', fontsize=font_sz)
                l3 = ax2_v.plot(t_w2, v2, 'tab:blue', linewidth=pub_lw,
                               marker='o' if marker_sz > 0 else '', markersize=marker_sz, label='Voltage')
                ax2_v.tick_params(axis='y', labelcolor='tab:blue', labelsize=font_sz*0.9)
                ax2_v.tick_params(axis='x', labelsize=font_sz*0.9)
                
                ax2_i = ax2.twinx()
                ax2_i.set_ylabel('Current (mA)', color='tab:cyan', fontsize=font_sz)
                l4 = ax2_i.plot(t_w2, i2*1e3, 'tab:cyan', linewidth=pub_lw, linestyle='--',
                               marker='s' if marker_sz > 0 else '', markersize=marker_sz, label='Current')
                ax2_i.tick_params(axis='y', labelcolor='tab:cyan', labelsize=font_sz*0.9)
                
                ax2.set_title('Electrode 2 (W2)', fontsize=font_sz*1.2, fontweight='bold')
                ax2.grid(True, alpha=grid_a)
                if minor_g:
                    ax2.minorticks_on()
                    ax2.grid(True, which='minor', alpha=grid_a/2)
                
                lines = l3 + l4
                ax2.legend(lines, [l.get_label() for l in lines], loc=leg_loc, fontsize=font_sz*0.9)
                
                plt.tight_layout()
                
                st.pyplot(fig_pub)
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=pub_dpi, bbox_inches='tight')
                plt.close()
                buf.seek(0)
                
                st.download_button("📥 Download PNG", buf.getvalue(), 
                                  f"publication_IV_{pub_dpi}dpi.png", "image/png", type="primary")
                st.success(f"✅ {pub_w}×{pub_h} in @ {pub_dpi} DPI")

else:
    st.info("👈 Upload all 4 CSV files to begin")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🚀 Features
        - 8-panel comprehensive analysis
        - Rectified vs signed power
        - Dual Lissajous figures
        - Power factor analysis
        - Energy per cycle
        """)
    with col2:
        st.markdown("""
        ### 📊 Publication Plots
        - Dual-axis I-V plots
        - One per electrode
        - Live preview
        - High-res export (300-600 DPI)
        - Fully customizable
        """)

st.divider()

# Copyright and citation footer
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>
        <p style='margin: 0; font-size: 14px;'><strong>Enhanced I-V Analysis Tool</strong></p>
        <p style='margin: 5px 0; font-size: 12px;'>© 2024 P. Srikar. All rights reserved.</p>
        <p style='margin: 5px 0; font-size: 11px; color: #666;'>
            <strong>Please cite when using this tool in publications:</strong><br>
            Srikar, P. (2024). Enhanced Discharge I-V Analysis Tool.<br>
            <em>GitHub repository: https://github.com/YOUR_USERNAME/discharge-iv-analyzer</em>
        </p>
        <p style='margin: 5px 0; font-size: 10px; color: #888;'>
            Licensed under MIT License | Comprehensive discharge characterization
        </p>
    </div>
    """, unsafe_allow_html=True)
