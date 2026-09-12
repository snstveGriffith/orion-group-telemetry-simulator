
# 🚀 Orion Group — Aerospace Telemetry Simulator

Proprietary flight telemetry simulation and analysis software developed for the aerospace engineering and defense division of **Orion Group**.

This project models the dynamic physics of a launch vehicle's first stage (rocket), calculating real-time variations in acceleration, velocity, and altitude based on continuous fuel mass consumption and motor thrust.

---

## 📌 Features

- **Real-Time Physics Simulation:** Powered by Newton's laws of motion and variable-mass dynamics ($a = \frac{Thrust}{Mass} - g$).
- **Automated Telemetry Calculation:** Step-by-step numerical integration ($\Delta t = 1s$) during the 89-second ascent profile.
- **Data Visualization:** Automatic generation and export of corporate flight telemetry panels (Altitude vs. Time and Velocity vs. Time).
- **Web Integration:** Direct image output formatted for corporate dashboard presentation.

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Data Processing:** NumPy
- **Data Visualization:** Matplotlib

---

## 📊 First-Stage Technical Specifications

- **Dry Mass:** 186,300 kg
- **Initial Fuel Mass:** 144,000 kg
- **Nominal Thrust:** 4,682,500 N
- **Burn Time:** 89 seconds
- **Mass Burn Rate:** ~1,618 kg/s

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com//OrionGroup_Aerospace.git](https://github.com/snstveGriffith/OrionGroup_Aerospace.git)
   cd OrionGroup_Aerospace

2. Create and activate a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate
   
3. Install dependencies:
   pip install matplotlib numpy
   
4. Run the simulator:
   python main.py
   

The generated plot will be automatically saved to graficos/telemetry_orion_flight.png.

⚠️ ****Disclaimer: This repository and its contents were created exclusively for an academic school project. "Orion Group" is a fictional entity designed for educational and demonstration purposes.****
