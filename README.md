# ERP Data Accuracy Analysis

## Project Description
The aim of this project to show the impact of incorrect unit measurements in ERP systems and how correcting these discrepancies leads to a **26% reduction in financial discrepancies**. 

### Key Features:
- **Versatility and adaptability**: No vulnerable or critical business data, only random data according to entered parameters.
- **Error Detection**: Identifies incorrect unit measurements in ERP to ensure accuracy.
- **Visualization & Finansial Reporting**: Provides clear visual insights and reports on the impact of incorrect data.
  
![BOM Analysis](BOM_Analysis.png)

## Technologies Used
- **SQLite** - Database management
- **Python** - Data processing and analysis
- **Pandas** - Data manipulation
- **Matplotlib** - Data visualization
- **OpenPyXL** - Excel data handling

## Data Processing Workflow
1. **Database Creation & Data Population**
   - Simulates material usage in production.
   - Introduces intentional data inconsistencies.
2. **Data Analysis & Correction**
   - Identifies incorrect unit measurements.
   - Converts erroneous values to correct units.
3. **Financial Discrepancy Calculation**
   - Compares incorrect vs. corrected material usage.
   - Calculates the financial difference.
4. **Visualization & Reporting**
   - Generates reports and visual insights into discrepancies.
   
## Results & Impact
- **Incorrect unit measurements led to overestimated material costs.**
- **Adjusting values resulted in a 26% reduction in discrepancies.**
- **Clear visual representations of incorrect vs. correct cost analysis.**

## How to Run the Project
1. Clone this repository:
   ```sh
   git clone https://github.com/vsflcn/ERP-Data-Accuracy-Analysis.git
   ```
2. Install Python from official site:
   ```
   https://www.python.org/
   ```
4. Install required dependencies:
   ```sh
   pip install pandas matplotlib openpyxl sqlite3
   ```
5. Run the first script to create database (create_database folder):
   ```sh
   python create_db.py
   ```
6. With new .csv file run the following analysis script:
   ```sh
   python analysis.py
   ```
7. Check the generated reports and visualizations.

## Contribution
Feel free to contribute by improving this data analysis!

## License
This project is licensed under the MIT License.


