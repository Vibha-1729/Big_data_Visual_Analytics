# ===========================================
# DATA LOADING AND PROCESSING
# ===========================================

import pandas as pd
import json
import os
from config.settings import (
    ATTRIBUTE_CATEGORIES, 
    DISTRICT_ATTRIBUTE_CATEGORIES, 
    CSV_TO_GEOJSON_MAPPING
)

# Global data variables
india_geo = None
state_data = None
district_data = None
state_file_map = {}
state_dropdown_options = []
pct_cols = []
district_percentage_cols = []

def load_geojson_data():
    """Load India GeoJSON for state boundaries"""
    global india_geo
    try:
        with open("C:\\Users\\Vibha Narayan\\OneDrive\\Desktop\\coding\\GitDemo\\CS661\\Group Project\\project6613_updated\\project6613\\project661\\india.json", encoding="utf-8") as f:
            india_geo = json.load(f)
        print("✅ India GeoJSON loaded successfully")
        return india_geo
    except Exception as e:
        print(f"❌ Error loading india.json: {e}")
        return {}

def load_state_data():
    """Load State-wise aggregated data (only percentage columns)"""
    global state_data, pct_cols
    try:
        state_data_full = pd.read_csv("C:\\Users\\Vibha Narayan\\OneDrive\\Desktop\\coding\\GitDemo\\CS661\\Group Project\\project6613_updated\\project6613\\project661\\statewiseaggregated.csv")
        # Filter only percentage columns (ending with '_pct') + essential columns
        essential_cols = ['State name', 'District code', 'Population']
        pct_cols = [col for col in state_data_full.columns if col.endswith('_pct')]
        state_data = state_data_full[essential_cols + pct_cols]
        print(f"✅ State data loaded: {len(state_data)} rows, {len(pct_cols)} percentage columns")
        return state_data
    except Exception as e:
        print(f"❌ Error loading statewiseaggregated.csv: {e}")
        state_data = pd.DataFrame()
        return state_data

def load_district_data():
    """Load District-wise data (only percentage columns with % symbol)"""
    global district_data, district_percentage_cols
    try:
        district_data_full = pd.read_csv("C:\\Users\\Vibha Narayan\\OneDrive\\Desktop\\coding\\GitDemo\\CS661\\Group Project\\project6613_updated\\project6613\\project661\\districtwise_data_percentages11_incsv.csv")
        # Filter only percentage columns (containing '%' symbol) + essential columns
        essential_cols_district = ['State name', 'District name']
        district_percentage_cols = [col for col in district_data_full.columns if '%' in str(col)]
        district_data = district_data_full[essential_cols_district + district_percentage_cols]
        print(f"✅ District data loaded: {len(district_data)} rows, {len(district_percentage_cols)} percentage columns")
        return district_data
    except Exception as e:
        print(f"❌ Error loading districtwise_data_percentages11_incsv.csv: {e}")
        district_data = pd.DataFrame()
        return district_data

def create_state_file_mapping():
    """Create mapping for state names to their geojson files"""
    global state_file_map, state_dropdown_options
    try:
        # Check which GeoJSON files actually exist and create mappings
        for csv_state_name, geojson_file in CSV_TO_GEOJSON_MAPPING.items():
            if os.path.exists(geojson_file):
                state_file_map[csv_state_name] = geojson_file
                state_dropdown_options.append({"label": csv_state_name, "value": csv_state_name})
            else:
                print(f"⚠️ GeoJSON file missing: {geojson_file} for {csv_state_name}")
        
        print(f"✅ State-GeoJSON mapping created: {len(state_file_map)} states available")
        return state_file_map
    except Exception as e:
        print(f"❌ Error creating state mappings: {e}")
        return {}

def categorize_attributes():
    """Categorize percentage columns into logical groups"""
    global pct_cols
    
    categories = ATTRIBUTE_CATEGORIES.copy()
    
    # Categorize state data columns
    for col in pct_cols:
        col_lower = col.lower()
        if any(x in col_lower for x in ['male', 'female']):
            categories["🏠 Demographics"].append(col)
        elif any(x in col_lower for x in ['literate', 'education', 'primary', 'secondary', 'graduate']):
            categories["📚 Education & Literacy"].append(col)
        elif any(x in col_lower for x in ['worker', 'employment', 'cultivator', 'agricultural']):
            categories["💼 Employment"].append(col)
        elif any(x in col_lower for x in ['sc', 'st', 'caste']):
            categories["🏛️ Social Categories"].append(col)
        elif any(x in col_lower for x in ['hindu', 'muslim', 'christian', 'sikh', 'buddhist', 'jain', 'religion']):
            categories["🕊️ Religion"].append(col)
        elif any(x in col_lower for x in ['household', 'lpg', 'electric', 'internet', 'computer', 'bicycle', 'car', 'tv', 'telephone']):
            categories["🏡 Household Amenities"].append(col)
        elif any(x in col_lower for x in ['water', 'latrine', 'drinking']):
            categories["💧 Water & Sanitation"].append(col)
        elif any(x in col_lower for x in ['power_parity', 'rs_']):
            categories["💰 Economic Indicators"].append(col)
        elif any(x in col_lower for x in ['age_group']):
            categories["📊 Age Groups"].append(col)
    
    # Remove empty categories
    categories = {k: v for k, v in categories.items() if v}
    return categories

def filter_district_categories():
    """Filter district categories based on available columns"""
    global district_data
    
    filtered_categories = {}
    for category, attributes in DISTRICT_ATTRIBUTE_CATEGORIES.items():
        available_attrs = [attr for attr in attributes if attr in district_data.columns]
        if available_attrs:
            filtered_categories[category] = available_attrs
    
    return filtered_categories

def load_all_data():
    """Load all required data files"""
    print("🚀 Loading data files...")
    india_geo = load_geojson_data()
    state_data = load_state_data()
    district_data = load_district_data()
    state_file_map = create_state_file_mapping()
    if india_geo and not isinstance(india_geo, bool):
        print("✅ All data loaded successfully!")
        print("📊 Ready to create beautiful visualizations!")
    else:
        print("⚠️ Some data files failed to load")
    return india_geo

# Export data access functions
def get_india_geo():
    return india_geo

def get_state_data():
    return state_data

def get_district_data():
    return district_data

def get_state_file_map():
    return state_file_map

def get_state_dropdown_options():
    return state_dropdown_options

def get_pct_cols():
    return pct_cols

def get_district_percentage_cols():
    return district_percentage_cols
