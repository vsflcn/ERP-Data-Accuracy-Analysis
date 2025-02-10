SELECT 
    id,
    material_index,
    material_name_en,
    material_name_pl,
    quantity,
    unit,
    price_per_unit,
    total_value,
    product_code
FROM inventory_usage
WHERE material_index LIKE 'AXR%' 
   OR material_index LIKE 'CM%' 
   OR material_index LIKE 'B%'
ORDER BY product_code, production_year, production_month;