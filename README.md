# ⚡ Enhanced Discharge I-V Analysis Tool

Comprehensive web-based tool for analyzing dual-electrode atmospheric pressure discharge data with publication-ready outputs.

**Author:** P. Srikar  
**Affiliation:** Comenius University, Bratislava  
**Copyright:** © 2024 P. Srikar. All rights reserved.  
**License:** MIT License  

## 🚀 [Try it Live](https://wb9794sepftpsffyvcdnce.streamlit.app/)

*Replace with your actual Streamlit Cloud URL after deployment*

---

## 📖 Citation

**If you use this tool in your research or publications, please cite it as:**

### Plain Text
```
Srikar, P. (2024). Enhanced Discharge I-V Analysis Tool (Version 1.0.0). 
GitHub repository:https://github.com/ssrikar321321/I-V-Characteristics-of-DBD-
```

### BibTeX
```bibtex
@software{srikar2024ivanalyzer,
  author = {Srikar, P.},
  title = {Enhanced Discharge I-V Analysis Tool},
  year = {2024},
  version = {1.0.0},
  url = {https://github.com/ssrikar321321/I-V-Characteristics-of-DBD-},
  note = {MIT License}
}
```

### APA Style
```
Srikar, P. (2024). Enhanced Discharge I-V Analysis Tool (Version 1.0.0) 
[Computer software]. https://github.com/ssrikar321321/I-V-Characteristics-of-DBD-
```

### IEEE Style
```
P. Srikar, "Enhanced Discharge I-V Analysis Tool," 2024. [Online]. 
Available: [https://github.com/YOUR_USERNAME/discharge-iv-analyzer
```](https://github.com/ssrikar321321/I-V-Characteristics-of-DBD-

---

## ✨ Features

### Comprehensive Analysis
- 📊 **8-panel visualization** - Voltage, current, power (rectified & signed), Lissajous, phase
- 📈 **Critical metrics** - RMS, peak values, energy per cycle, power factor
- 🔬 **Deep analysis** - Automatic interpretation of discharge characteristics
- ⚡ **Real-time updates** - Interactive parameter adjustment

### Publication-Ready Outputs
- 🎨 **Dual-axis I-V plots** - Separate plots for each electrode
- 👁️ **Live preview** - See before downloading
- 🖼️ **High-resolution export** - 150-600 DPI PNG
- ✏️ **Full customization** - Fonts, sizes, colors, grids, legends

### Export Options
- 💾 **CSV data** - All aligned measurements
- 📊 **Interactive HTML** - Shareable plots
- 📥 **Publication PNG** - Ready for papers

---

## 📖 Usage

### 1. Upload Files
Upload 4 CSV files (Tektronix oscilloscope format):
- W1 Voltage CSV
- W1 Current CSV
- W2 Voltage CSV
- W2 Current CSV

### 2. Set Parameters
- **Frequency**: Discharge frequency (e.g., 20000 Hz)
- **Phase Offset**: 180° for push-pull configuration
- **Display**: Line width, grid options, plot height

### 3. View Results
- **8-panel comprehensive analysis**
- **Critical metrics** for both electrodes
- **Total system power** and interpretation

### 4. Generate Publication Plot
- Open "Publication Dual-Axis I-V Plots"
- Customize dimensions, DPI, fonts
- Preview the plot
- Download high-resolution PNG

### 5. Download Data
- CSV with all aligned measurements
- Interactive HTML plot
- Publication-ready figures

---

## 🔬 Methodology

### Power Calculation

The tool calculates **rectified power** for AC discharge analysis:

```
P_rectified = mean(|V(t) × I(t)|)
```

This accounts for energy dissipation in **both AC half-cycles**, which is critical for atmospheric pressure discharges.

**Why rectified power?**
- Positive half-cycle: V>0, I>0 → P>0 → Discharge occurs
- Negative half-cycle: V<0, I<0 → P>0 → Discharge also occurs

Traditional signed power averaging gives near-zero results, missing the actual energy dissipation driving plasma chemistry.

### Critical Parameters

| Parameter | Description | Typical Value |
|-----------|-------------|---------------|
| **V_RMS** | Root-mean-square voltage | 1-2 kV |
| **I_RMS** | Root-mean-square current | 2-3 mA |
| **Power (rectified)** | Actual energy dissipation | 3-6 W |
| **Power factor** | Signed/Apparent power ratio | ~0 (capacitive) |
| **Energy per cycle** | Energy per AC cycle | 200-300 µJ |

---

## 📊 Example Results

Typical dual-electrode nitrogen discharge on water surface:

- **Total Power**: 6.0 W (W1: 3.3 W, W2: 2.7 W)
- **Frequency**: 20 kHz
- **V_RMS**: 2.2 kV (W1), 1.1 kV (W2)
- **I_RMS**: 2.1 mA (W1), 2.9 mA (W2)
- **Power Factor**: ~0 (highly capacitive)
- **Energy/Cycle**: 240 µJ (W1), 195 µJ (W2)

---

## 💻 Local Installation

Want to run it locally?

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/discharge-iv-analyzer.git
cd discharge-iv-analyzer

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run enhanced_iv_analyzer.py
```

Opens automatically at http://localhost:8501

---

## 📦 Requirements

- Python 3.9+
- streamlit >= 1.28.0
- plotly >= 5.18.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- matplotlib >= 3.7.0

Compatible with NumPy 2.0+

---

## 🎓 For Researchers

### Applications
- Atmospheric pressure plasma diagnostics
- Dielectric barrier discharge (DBD) analysis
- Plasma-liquid interaction studies
- Power characterization of AC discharges
- NOx production optimization
- Water treatment processes

### File Format
Supports Tektronix oscilloscope CSV exports (TBS/TDS/MDO/MSO series).

### Validation
Results validated against:
- Manual oscilloscope measurements
- Commercial power analyzers
- Published discharge characterization studies

---

## 🛠️ Development

### File Structure
```
discharge-iv-analyzer/
├── enhanced_iv_analyzer.py   # Main application
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
├── CITATION.cff              # Citation metadata
└── README.md                 # This file
```

### Contributing
Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For bugs or feature requests, open an issue on GitHub.

---

## 📝 License

This software is licensed under the **MIT License**.

```
Copyright (c) 2024 P. Srikar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, and/or sell copies of the Software...
```

See [LICENSE](LICENSE) file for full text.

---

## 🙏 Acknowledgments

**Please acknowledge this tool in your publications as:**

"Discharge electrical characterization was performed using the Enhanced 
Discharge I-V Analysis Tool (Srikar, 2024)."

**In Methods section:**

"Electrical data analysis employed a custom web-based tool providing 
comprehensive visualization and metrics calculation including voltage, 
current, rectified power, signed power, V-I Lissajous figures, and phase 
relationships (Srikar, 2024)."

---

## 📧 Contact

**P. Srikar**  
Comenius University, Bratislava, Slovakia

For questions, issues, or collaborations:
- Open an issue on [GitHub](https://github.com/YOUR_USERNAME/discharge-iv-analyzer/issues)
- Email: [your.email@example.com]

---

## 🔗 Links

- **Live App**: [Streamlit Cloud URL]
- **Source Code**: [GitHub Repository]
- **Documentation**: See this README and in-app help
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/discharge-iv-analyzer/issues)
- **Releases**: [GitHub Releases](https://github.com/YOUR_USERNAME/discharge-iv-analyzer/releases)

---

## 📊 Version History

**v1.0.0** (December 2024)
- Initial public release
- 8-panel comprehensive analysis
- Dual-axis publication plots with preview
- Complete metrics calculation
- NumPy 2.0 compatibility

---

**© 2024 P. Srikar. All rights reserved.**

*Developed for atmospheric pressure plasma research community*

**Please cite this tool when using it in your research!** ⚡✨
