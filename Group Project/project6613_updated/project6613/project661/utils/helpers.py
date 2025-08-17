# ===========================================
# UTILITY HELPER FUNCTIONS
# ===========================================

def get_short_label(column_name):
    """Convert long column names to short, readable labels"""
    # Remove '_pct' suffix and '%' symbols
    clean_name = column_name.replace('_pct', '').replace('%', '').strip()
    
    # Create shorter, more readable labels
    label_map = {
        'Male_Literate': 'Male Literacy',
        'Female_Literate': 'Female Literacy',
        'Male_Workers': 'Male Employment',
        'Female_Workers': 'Female Employment',
        'Rural_Households': 'Rural Areas',
        'Urban_Households': 'Urban Areas',
        'LPG_or_PNG_Households': 'LPG/PNG Access',
        'Housholds_with_Electric_Lighting': 'Electricity',
        'Households_with_Internet': 'Internet',
        'Households_with_Computer': 'Computer',
        'Households_with_Scooter_Motorcycle_Moped': 'Scooter/Motorcycle',
        'Power_Parity_Less_than_Rs_45000': '<₹45k Income',
        'Power_Parity_Above_Rs_545000': '>₹545k Income'
    }
    
    return label_map.get(clean_name, clean_name.replace('_', ' ').title())

def get_district_short_label(attribute):
    """Get short, readable label for district attributes"""
    if not attribute:
        return ""
    
    # Remove _% suffix and common prefixes
    clean_attr = attribute.replace('_%', '').replace('_', ' ')
    clean_attr = clean_attr.replace('Households with ', '').replace('Main source of drinking water ', '')
    clean_attr = clean_attr.replace('Location of drinking water source ', '').replace('Type of latrine facility ', '')
    
    # Create short labels
    short_labels = {
        'Male': 'Male Population',
        'Female': 'Female Population', 
        'Literate': 'Literacy Rate',
        'Male Literate': 'Male Literacy',
        'Female Literate': 'Female Literacy',
        'Workers': 'Employment Rate',
        'Male Workers': 'Male Employment',
        'Female Workers': 'Female Employment',
        'Primary Education': 'Primary Education',
        'Secondary Education': 'Secondary Education',
        'Higher Education': 'Higher Education',
        'Graduate Education': 'Graduate Education',
        'LPG or PNG Households': 'Clean Cooking Fuel',
        'Internet': 'Internet Access',
        'Computer': 'Computer Access',
        'Television': 'Television Access',
        'Telephone Mobile Phone': 'Phone Access',
        'Tapwater Households': 'Tap Water Access',
        'Within the premises Households': 'Water Within Premises',
        'Flush pour flush latrine connected to other system Households': 'Flush Toilets',
        'Having latrine facility within the premises Total Households': 'Toilet Facilities'
    }
    
    return short_labels.get(clean_attr, clean_attr[:25] + '...' if len(clean_attr) > 25 else clean_attr)
