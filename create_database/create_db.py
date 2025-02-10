import sqlite3
import random

conn = sqlite3.connect('inventory_data.sqlite')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_index TEXT VARCHAR(12),
    material_name_en TEXT VARCHAR(30),
    material_name_pl TEXT VARCHAR(30),
    quantity REAL,
    unit TEXT,
    price_per_unit REAL,
    total_value REAL,
    product_code TEXT,
    production_month INTEGER,
    production_year INTEGER,
    usage_type TEXT
)
''')

material_index = {
    "AXR": ["Auxiliary Materials", "Materiały pomocnicze"],
    "BXE": ["Basic Equipment", "Podstawowy sprzęt"],
    "CMT": ["Coatings, Materials and Treatments", "Powłoki, materiały i środki"],
    "DPE": ["Design and Product Engineering", "Projektowanie i inżynieria produktów"]
}

axr_package_size = [1, 5, 10, 20, 24, 36, 48, 50, 100]
bxe_package_size = 1
cmt_package_size = [2.5, 15.0, 25.0, 50.0]
dpe_package_size = 1

products = {
    "PRD-001": 54,
    "PRD-002": 102,
    "PRD-003": 101,
}

production_plan = {
    "PRD-001": 10,
    "PRD-002": 25,
    "PRD-003": 30,
}

random.seed(42)
data = []
for year in [2024]:
    for month in range(1, 13):
        for product, bom_size in products.items():
            num_produced = production_plan[product]
            for _ in range(bom_size * num_produced):
                material_type = random.choice(list(material_index.keys()))
                material_id = f"{material_type}-{random.randint(100000, 999999)}"
                material_name_en, material_name_pl = material_index[material_type]
                price_per_unit = round(random.uniform(0.5, 50), 2) 
                
                if material_type == "AXR":
                    package = random.choice(axr_package_size)
                    if random.random() < 0.85:  # 85% chance for incorrect data
                        if package: 
                            quantity = round(package * random.uniform(1, 1), 1)
                            unit = "pcs"
                        else:
                            quantity = round(package / random.uniform(1, 1), 1)  
                            unit = "pcs"  
                    else: 
                        # Correct values should be between 0.1 and 1
                        quantity = round(random.uniform(0.1, 1), 2) 
                        unit = "unit"
                        price_per_unit = round(random.uniform(0.1, 50), 2) 
                        
                elif material_type == "BXE" or material_type == "DPE":
                    quantity = random.randint(1, 10) 
                    unit = "units" 
                elif material_type == "CMT":
                    quantity = round(random.choice(cmt_package_size)* random.uniform(0.1, 5), 2) 
                    unit = "units" 
                else:
                    quantity = 1 
                    unit = "units"
                
                total_value = round(quantity * price_per_unit, 2)
                
                data.append((material_id, material_name_pl, material_name_en, 
                             quantity, unit, price_per_unit, total_value,
                             product, month, year, "Main Production"))

cursor.executemany('''
INSERT INTO inventory_usage (material_index, material_name_en, material_name_pl, quantity, unit, price_per_unit, total_value, product_code, production_month, production_year, usage_type)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', data)

conn.commit()
conn.close()

print('Database successfully populated.')
