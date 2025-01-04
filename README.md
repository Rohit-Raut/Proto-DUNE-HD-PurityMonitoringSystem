# Proto-DUNE-HD Purity Monitoring System

Welcome to the **Proto-DUNE-HD Purity Monitoring System** repository! This project focuses on analyzing ADC signals, calculating integrals, and monitoring purity within the Proto-DUNE-HD experimental framework. This tool was used for extracting the data from Proto-DUNE HD detector, cleaning the cosmic backgrounds, and analyzing the Bismuth Source.

This repository represents a collaborative effort between **CERN** and the **University of Texas at Arlington**.

---

## **Overview**

This repository provides:

- **Python scripts** for ADC data processing and analysis.
- **Raw and processed data files** for various test runs.
- **Visualization tools** to assist in data interpretation.
- Detailed CSV files that document ADC areas and integrals for multiple runs.

For simulation-related work, including Geant4 modeling, please refer to the separate simulation repository.

---

## **Repository Contents**

### **Key Files and Directories**

1. **`main.py`**
   - The main script orchestrating the ADC processing pipeline.

2. **`adc_processing/`**
   - Contains scripts for ADC-specific data analysis:
     - [`adc_area_calculation.py`](https://github.com/Rohit-Raut/Proto-DUNE-HD-PurityMonitoringSystem/blob/main/adc_processing/adc_area_calculation.py): A script for calculating ADC areas and integrals.

3. **Data Files**
   - Processed ADC area and integral data are stored in CSV files:
     - Examples: `T063800_adc_areas.csv`, `T063811_adc_integrals.csv`.

4. **Visualizations**
   - Includes graphical outputs like `Channel_Comp.png` for channel comparison.

5. **Supporting Files**
   - `README.md`: This README file.
   - `run_code.sh`: A shell script for running processing pipelines.

---

## **Setup and Usage**

### **Prerequisites**

Ensure the following tools and dependencies are installed:

- **Python 3.8** or later
- Required Python packages. Install them using:

  ```bash
  pip install -r requirements.txt
## Steps to Use

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/Rohit-Raut/Proto-DUNE-HD-PurityMonitoringSystem.git
