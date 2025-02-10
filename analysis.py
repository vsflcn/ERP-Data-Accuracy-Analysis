import random
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import openpyxl

random.seed(42)

# Load and clean data
df_24 = pd.read_csv("materials.csv", low_memory=False)
df_24.dropna(inplace=True)

class BillOfMaterials24:
    def __init__(self, data):
        self.data = data

    def get_data(self):
        return self.data

bom_24 = BillOfMaterials24(df_24)

class IncorrectValuesReport:
    def __init__(self, data):
        self.data = data

    def incorrect_sum_axr_pcs(self):
        filtered_incorrect_data = self.data[
            (self.data["material_index"].str.startswith("AXR")) 
            & (self.data["unit"] == "pcs")]
        total_pcs = (filtered_incorrect_data["quantity"] * filtered_incorrect_data["price_per_unit"]).sum()
        return total_pcs


class CorrectValuesReport:
    def __init__(self, data):
        self.data = data
        
    def correct_sum_axr_pcs(self):
    # Conversion of pcs
        filtered_data_pcs = self.data[
        (self.data["material_index"].str.startswith("AXR")) & (self.data["unit"] == "pcs")]
    
        axr_package_size = [1, 5, 10, 20, 24, 36, 48, 50, 100]
    
        total_converted_units = 0
    
        if not filtered_data_pcs.empty:
            for _, row in filtered_data_pcs.iterrows():
                package = random.choice(axr_package_size) 
                quantity_in_units = row["quantity"] / package
            
                total_converted_units += quantity_in_units * row["price_per_unit"]

        return total_converted_units
    

    def total_sum_units(self):
        filtered_data_unit= self.data[
            (self.data["material_index"].str.startswith("AXR")) & (self.data["unit"] == "unit")
        ]
        total_pcs = (filtered_data_unit["quantity"] * filtered_data_unit["price_per_unit"]).sum()
        return total_pcs
    
    def total_sum_bxe(self):
        filtered_data= self.data[self.data["material_index"].str.startswith("BXE")]
        total_bxe = (filtered_data["quantity"] * filtered_data["price_per_unit"]).sum()
        return total_bxe
    
    def total_sum_cmt(self):
        filtered_data= self.data[self.data["material_index"].str.startswith("CMT")]
        total_cmt = (filtered_data["quantity"] * filtered_data["price_per_unit"]).sum()
        return total_cmt
    
    def total_sum_dpe(self):
        filtered_data= self.data[self.data["material_index"].str.startswith("DPE")]
        total_dpe = (filtered_data["quantity"] * filtered_data["price_per_unit"]).sum()
        return total_dpe

    def total_bom_sum(self):
        filtered_data = self.data[
            (self.data["material_index"].str.startswith(("BXE", "CMT", "DPE")))
        ]
        total_sum = (filtered_data["quantity"] * filtered_data["price_per_unit"]).sum()
        return total_sum

incorrect = IncorrectValuesReport(bom_24.get_data())
correct = CorrectValuesReport(bom_24.get_data())

total_bxe = correct.total_sum_bxe()
total_cmt = correct.total_sum_cmt()
total_dpe = correct.total_sum_cmt()

incorrect_axr_pcs = incorrect.incorrect_sum_axr_pcs() 
correct_axr_pcs = correct.correct_sum_axr_pcs()
total_axr_unit = correct.total_sum_units()
print (f"Total amount of AXR usage in PCS is {incorrect_axr_pcs:,.2f} EUR.")
print (f"Total amount of AXR usage in UNITS is {correct_axr_pcs:,.2f} EUR.")

incorrect_sum_axr = incorrect_axr_pcs + total_axr_unit 
correct_sum_axr = correct_axr_pcs + total_axr_unit 
percentage_sum_difference = (correct_sum_axr - incorrect_sum_axr) / incorrect_sum_axr * 100
print(f"Correct amount of AXR materials is {correct_sum_axr:,.2f} EUR. Difference according incorrect amount is {percentage_sum_difference:,.2f}%")

incorrect_total = correct.total_bom_sum() + incorrect_sum_axr 
correct_total = correct.total_bom_sum() + correct_sum_axr 
difference = correct_total - incorrect_total
percentage_difference = (difference / incorrect_total) * 100
print(f"Correct Total amount of BOM usage is {correct_total:,.2f} EUR.")
print(f"Total BOM difference with according incorrect amount is {percentage_difference:,.2f}%")



#Visualisation

fig, axs = plt.subplots(1, 2, figsize=(10, 3), gridspec_kw={'wspace': 1.0})

summary_text = f"""
Total AXR usage in PCS:
{incorrect_axr_pcs:,.2f} EUR

Total AXR usage in UNITS:
{total_axr_unit:,.2f} EUR

Difference
between correct 
and incorrect usage:
{percentage_sum_difference:.2f}%

Total Correct BOM: 
{correct_total:,.2f} EUR

BOM difference 
between correct 
and incorrect values:
{percentage_difference:.2f}%
"""

fig.text(0.5, 0.9, summary_text, ha="center", fontsize=8, bbox=dict(facecolor="white", alpha=0.1), va="top")

bar_colors = ["#B39EB5", "#9EADC8", "#FF9999", "#FFB266", "#FFD966", "#66CDAA", "#66B2FF", "#C49CDE", "#FF99CC", "#A56969"]
pie_colors = bar_colors
final_bar_colors = ["#FFB266", "#FFD966"]

labels = ["BXE", "CMT", "DPE", "AXR-incorrect", "AXR-correct"]
values = [total_bxe, total_cmt, total_dpe, incorrect_sum_axr, correct_sum_axr]


axs[0].pie(values, labels=labels, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', colors=pie_colors, textprops={'fontsize': 7})
axs[0].set_title("Percentage Difference in Material Proportion", fontsize=10)

pos = axs[0].get_position()
axs[0].set_position([pos.x0 - 0.05, pos.y0, pos.width, pos.height])


axs[1].bar(["Incorrect", "Correct"], [incorrect_total, correct_total], color=final_bar_colors, width=0.3)
axs[1].set_title("Comparison of BOM Usage Totals 2024 (EUR)", fontsize=10)

for i, v in enumerate([incorrect_total, correct_total]):
    axs[1].text(i, v * 1.01, f"{v:,.2f}", ha="center", fontsize=6)

legend_labels = {
    "BXE": "Basic Exchange Equipment",
    "CMT": "Composite Material",
    "DPE": "Dynamic Processing Element",
    "AXR-incorrect": "AXR (Incorrect measurement)",
    "AXR-correct": "AXR (Correct measurement)"
}

legend_patches = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=bar_colors[i], markersize=5, label=f"{key}: {value}")
                  for i, (key, value) in enumerate(legend_labels.items())]

fig.legend(handles=legend_patches, loc="lower left", ncol=2, fontsize=5, frameon=False)

plt.savefig("BOM_Analysis.png", dpi=300, bbox_inches="tight")
plt.show()
