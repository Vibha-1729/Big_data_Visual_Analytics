# ===========================================
# CONFIGURATION SETTINGS
# ===========================================

# Color palette for beautiful dashboard
COLORS = {
    'primary': '#6366f1',      # Indigo
    'secondary': '#ec4899',    # Pink
    'success': '#10b981',      # Emerald
    'warning': '#f59e0b',      # Amber
    'danger': '#ef4444',       # Red
    'info': '#3b82f6',         # Blue
    'light': '#f8fafc',        # Light gray
    'dark': '#1e293b',         # Dark gray
    'background_light': '#f8fafc',  # Background light
    'gradient_1': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'gradient_2': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'gradient_3': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'gradient_4': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'gradient_5': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
}

# Global font settings for beautiful typography
FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

# Define attribute categories based on available percentage columns
ATTRIBUTE_CATEGORIES = {
    "🏠 Demographics": [],
    "📚 Education & Literacy": [],
    "💼 Employment": [],
    "🏛️ Social Categories": [],
    "🕊️ Religion": [],
    "🏡 Household Amenities": [],
    "💧 Water & Sanitation": [],
    "💰 Economic Indicators": [],
    "📊 Age Groups": []
}

# District attribute categories
DISTRICT_ATTRIBUTE_CATEGORIES = {
    "Demographics": [
        "Male_%", "Female_%", "Literate_%", "Age_Group_0_29_%", "Age_Group_30_49_%", "Age_Group_50_%"
    ],
    "Education": [
        "Literate_%", "Male_Literate_%", "Female_Literate_%", "Primary_Education_%", 
        "Secondary_Education_%", "Higher_Education_%", "Graduate_Education_%"
    ],
    "Employment": [
        "Workers_%", "Male_Workers_%", "Female_Workers_%", "Main_Workers_%", 
        "Marginal_Workers_%", "Cultivator_Workers_%", "Agricultural_Workers_%"
    ],
    "Infrastructure": [
        "LPG_or_PNG_Households_%", "Households_with_Internet_%", "Households_with_Computer_%",
        "Households_with_Television_%", "Households_with_Telephone_Mobile_Phone_%"
    ],
    "Sanitation": [
        "Type_of_latrine_facility_Pit_latrine_Households_%",
        "Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households_%",
        "Having_latrine_facility_within_the_premises_Total_Households_%"
    ],
    "Water Access": [
        "Main_source_of_drinking_water_Tapwater_Households_%",
        "Location_of_drinking_water_source_Within_the_premises_Households_%",
        "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households_%"
    ]
}

# State name mapping for choropleth visualization
STATE_NAME_MAPPING = {
    'ANDAMAN AND NICOBAR ISLANDS': 'Andaman and Nicobar',
    'ANDHRA PRADESH': 'Andhra Pradesh',
    'ARUNACHAL PRADESH': 'Arunachal Pradesh',
    'ASSAM': 'Assam',
    'BIHAR': 'Bihar',
    'CHANDIGARH': 'Chandigarh',
    'CHHATTISGARH': 'Chhattisgarh',
    'DADRA AND NAGAR HAVELI': 'Dādra and Nagar Haveli and Damān and Diu',
    'DAMAN AND DIU': 'Dādra and Nagar Haveli and Damān and Diu',
    'GOA': 'Goa',
    'GUJARAT': 'Gujarat',
    'HARYANA': 'Haryana',
    'HIMACHAL PRADESH': 'Himachal Pradesh',
    'JAMMU AND KASHMIR': 'Jammu and Kashmir',
    'JHARKHAND': 'Jharkhand',
    'KARNATAKA': 'Karnataka',
    'KERALA': 'Kerala',
    'LAKSHADWEEP': 'Lakshadweep',
    'MADHYA PRADESH': 'Madhya Pradesh',
    'MAHARASHTRA': 'Maharashtra',
    'MANIPUR': 'Manipur',
    'MEGHALAYA': 'Meghalaya',
    'MIZORAM': 'Mizoram',
    'NAGALAND': 'Nagaland',
    'NCT OF DELHI': 'Delhi',
    'ORISSA': 'Orissa',
    'PONDICHERRY': 'Puducherry',
    'PUNJAB': 'Punjab',
    'RAJASTHAN': 'Rajasthan',
    'SIKKIM': 'Sikkim',
    'TAMIL NADU': 'Tamil Nadu',
    'TRIPURA': 'Tripura',
    'UTTAR PRADESH': 'Uttar Pradesh',
    'UTTARAKHAND': 'Uttaranchal',
    'WEST BENGAL': 'West Bengal'
}

# CSV to GeoJSON mapping
CSV_TO_GEOJSON_MAPPING = {
    'ANDHRA PRADESH': 'andhra_pradesh.geojson',
    'ARUNACHAL PRADESH': 'arunachal_pradesh.geojson',
    'ASSAM': 'assam.geojson',
    'BIHAR': 'bihar.geojson',
    'CHHATTISGARH': 'chhattisgarh.geojson',
    'GOA': 'goa.geojson',
    'GUJARAT': 'gujarat.geojson',
    'HARYANA': 'haryana.geojson',
    'HIMACHAL PRADESH': 'himachal-pradesh.geojson',
    'JAMMU AND KASHMIR': 'jammu-and-kashmir.geojson',
    'KARNATAKA': 'karnataka.geojson',
    'KERALA': 'kerala.geojson',
    'MADHYA PRADESH': 'madhya_pradesh.geojson',
    'MAHARASHTRA': 'maharashtra.geojson',
    'MANIPUR': 'manipur.geojson',
    'MEGHALAYA': 'meghalaya.geojson',
    'MIZORAM': 'mizoram.geojson',
    'NAGALAND': 'nagaland.geojson',
    'ORISSA': 'odisha.geojson',
    'PUNJAB': 'punjab.geojson',
    'RAJASTHAN': 'rajasthan.geojson',
    'SIKKIM': 'sikkim.geojson',
    'TAMIL NADU': 'tamil_nadu.geojson',
    'TRIPURA': 'tripura.geojson',
    'UTTAR PRADESH': 'uttar_pradesh.geojson',
    'UTTARAKHAND': 'uttarakhand.geojson',
    'WEST BENGAL': 'west_bengal.geojson'
}
