# Beautiful India Demographic Dashboard
# Using only percentage data for fair comparison

# ===========================================
# IMPORTS AND LIBRARIES
# ===========================================

import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

# ===========================================
# DATA LOADING AND FILTERING
# ===========================================

print("🚀 Loading data files...")

# Load India GeoJSON for state boundaries
try:
    with open("india.json", encoding="utf-8") as f:
        india_geo = json.load(f)
    print("✅ India GeoJSON loaded successfully")
except Exception as e:
    print(f"❌ Error loading india.json: {e}")

# Load State-wise aggregated data (only percentage columns)
try:
    state_data_full = pd.read_csv('statewiseaggregated.csv')
    # Filter only percentage columns (ending with '_pct') + essential columns
    essential_cols = ['State name', 'District code', 'Population']
    pct_cols = [col for col in state_data_full.columns if col.endswith('_pct')]
    state_data = state_data_full[essential_cols + pct_cols]
    print(f"✅ State data loaded: {len(state_data)} rows, {len(pct_cols)} percentage columns")
except Exception as e:
    print(f"❌ Error loading statewiseaggregated.csv: {e}")

# Load District-wise data (only percentage columns with % symbol)
try:
    district_data_full = pd.read_csv('districtwise_data_percentages11_incsv.csv')
    # Filter only percentage columns (containing '%' symbol) + essential columns
    essential_cols_district = ['State name', 'District name']
    pct_cols_district = [col for col in district_data_full.columns if '%' in str(col)]
    district_data = district_data_full[essential_cols_district + pct_cols_district]
    print(f"✅ District data loaded: {len(district_data)} rows, {len(pct_cols_district)} percentage columns")
except Exception as e:
    print(f"❌ Error loading districtwise_data_percentages11_incsv.csv: {e}")

# ===========================================
# STATE-GEOJSON FILE MAPPING
# ===========================================

# Create mapping for state names to their geojson files
state_file_map = {}
state_dropdown_options = []

# Direct mapping from CSV state names (uppercase) to GeoJSON filenames
csv_to_geojson_mapping = {
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
    # Note: Some states don't have GeoJSON files available:
    # ANDAMAN AND NICOBAR ISLANDS, CHANDIGARH, DADRA AND NAGAR HAVELI, 
    # DAMAN AND DIU, JHARKHAND, LAKSHADWEEP, NCT OF DELHI, PONDICHERRY
}

try:
    # Check which GeoJSON files actually exist and create mappings
    for csv_state_name, geojson_file in csv_to_geojson_mapping.items():
        if os.path.exists(geojson_file):
            state_file_map[csv_state_name] = geojson_file
            state_dropdown_options.append({"label": csv_state_name, "value": csv_state_name})
        else:
            print(f"⚠️ GeoJSON file missing: {geojson_file} for {csv_state_name}")
    
    print(f"✅ State-GeoJSON mapping created: {len(state_file_map)} states available")
    print(f"📁 Available state files: {list(state_file_map.keys())[:5]}...")
except Exception as e:
    print(f"❌ Error creating state mappings: {e}")

# ===========================================
# DATA CATEGORIES AND ATTRIBUTES
# ===========================================

# Define attribute categories based on available percentage columns
def categorize_attributes():
    """Categorize percentage columns into logical groups"""
    
    categories = {
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

ATTRIBUTE_CATEGORIES = categorize_attributes()

print("✅ Data categorization completed:")
for category, attrs in ATTRIBUTE_CATEGORIES.items():
    print(f"   {category}: {len(attrs)} attributes")

# ===========================================
# UTILITY FUNCTIONS
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

print("\n🎨 Dashboard initialization completed!")
print("📊 Ready to create beautiful visualizations with percentage data only!")
print("=" * 60)

# ===========================================
# BEAUTIFUL UI STYLING & THEME
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
    'gradient_1': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'gradient_2': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'gradient_3': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'gradient_4': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'gradient_5': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
}

# Global font settings for beautiful typography
FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"

# ===========================================
# DASH APP INITIALIZATION
# ===========================================

app = dash.Dash(__name__)
app.title = "🇮🇳 India Demographics Dashboard"

# Add external CSS for better styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            /* Global Styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            /* Header Styles */
            .header-container {
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                padding: 1rem 2rem;
                position: sticky;
                top: 0;
                z-index: 1000;
            }
            
            .main-title {
                background: linear-gradient(45deg, #fff, #f0f9ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                color: transparent;
                font-size: 2.5rem !important;
                font-weight: 800 !important;
                text-align: center;
                margin: 0 !important;
                text-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .subtitle {
                color: rgba(255, 255, 255, 0.8) !important;
                text-align: center;
                font-size: 1.1rem !important;
                margin-top: 0.5rem;
                font-weight: 300;
            }
            
            /* Tab Styles */
            .tab-container {
                background: rgba(255, 255, 255, 0.95) !important;
                margin: 2rem;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                backdrop-filter: blur(20px);
            }
            
            .custom-tabs {
                display: flex !important;
                background: linear-gradient(90deg, #667eea, #764ba2) !important;
                padding: 0;
                border-radius: 20px 20px 0 0;
            }
            
            .custom-tab {
                flex: 1;
                padding: 1.5rem 2rem !important;
                color: rgba(255, 255, 255, 0.7) !important;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 600 !important;
                font-size: 1.1rem !important;
                border: none !important;
                background: transparent !important;
                position: relative;
                overflow: hidden;
            }
            
            .custom-tab:hover {
                color: white !important;
                background: rgba(255, 255, 255, 0.1) !important;
            }
            
            .custom-tab.active {
                color: white !important;
                background: rgba(255, 255, 255, 0.2) !important;
                box-shadow: inset 0 -4px 0 white;
            }
            
            /* Card Styles */
            .analysis-card {
                background: white !important;
                border-radius: 16px;
                padding: 2rem;
                margin: 1.5rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .analysis-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            }
            
            .card-header {
                display: flex !important;
                align-items: center;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid #f1f5f9;
            }
            
            .card-title {
                font-size: 1.5rem !important;
                font-weight: 700 !important;
                color: #1e293b !important;
                margin: 0 !important;
            }
            
            /* Control Panel Styles */
            .control-panel {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
                padding: 2rem;
                border-radius: 16px;
                margin: 1.5rem;
                box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
            }
            
            .control-group {
                margin-bottom: 1.5rem;
            }
            
            .control-label {
                color: white !important;
                font-weight: 600 !important;
                font-size: 1rem !important;
                margin-bottom: 0.5rem;
                display: block;
            }
            
            /* Dropdown Styles */
            .Select-control {
                border-radius: 12px !important;
                border: none !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
                background: white !important;
                min-height: 45px !important;
            }
            
            .Select-placeholder {
                color: #64748b !important;
                font-weight: 500 !important;
            }
            
            /* Chart Container Styles */
            .chart-container {
                background: white !important;
                border-radius: 16px;
                padding: 1rem;
                margin: 1rem 0;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            /* Grid Layout */
            .grid-container {
                display: grid !important;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 2rem;
                padding: 1rem;
            }
            
            .grid-item {
                background: white !important;
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                transition: transform 0.3s ease;
            }
            
            .grid-item:hover {
                transform: translateY(-5px);
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .main-title {
                    font-size: 2rem !important;
                }
                .custom-tab {
                    padding: 1rem !important;
                    font-size: 1rem !important;
                }
                .grid-container {
                    grid-template-columns: 1fr !important;
                    gap: 1rem;
                }
            }
            
            /* Animation Classes */
            .fade-in {
                animation: fadeIn 0.6s ease-in-out;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .slide-in {
                animation: slideIn 0.8s ease-in-out;
            }
            
            @keyframes slideIn {
                from { opacity: 0; transform: translateX(-30px); }
                to { opacity: 1; transform: translateX(0); }
            }
            
            /* District Table Styles */
            .table-row:hover {
                background-color: #f0f9ff !important;
                transform: translateX(2px);
                box-shadow: 0 2px 8px rgba(99, 102, 241, 0.1);
            }
            
            /* Search Input Focus */
            input[type="text"]:focus {
                border-color: #6366f1 !important;
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
            }
            
            /* Table Scroll Styling */
            .table-container::-webkit-scrollbar {
                width: 8px;
            }
            
            .table-container::-webkit-scrollbar-track {
                background: #f1f5f9;
                border-radius: 4px;
            }
            
            .table-container::-webkit-scrollbar-thumb {
                background: #cbd5e1;
                border-radius: 4px;
            }
            
            .table-container::-webkit-scrollbar-thumb:hover {
                background: #94a3b8;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ===========================================
# BEAUTIFUL UI LAYOUT
# ===========================================

app.layout = html.Div([
    
    # Header Section
    html.Div([
        html.H1("🇮🇳 India Demographics Explorer", className="main-title"),
        html.P("Interactive Analysis of State & District Level Demographics", className="subtitle")
    ], className="header-container"),
    
    # Main Content Container
    html.Div([
        
        # Tab Navigation
        html.Div([
            html.Button([
                html.Span("🗺️", style={'marginRight': '10px', 'fontSize': '1.3rem'}),
                "State Analysis"
            ], id="tab-state", className="custom-tab active", n_clicks=1),
            
            html.Button([
                html.Span("🏘️", style={'marginRight': '10px', 'fontSize': '1.3rem'}),
                "District Analysis"
            ], id="tab-district", className="custom-tab", n_clicks=0),
            
            html.Button([
                html.Span("📊", style={'marginRight': '10px', 'fontSize': '1.3rem'}),
                "Comparison"
            ], id="tab-comparison", className="custom-tab", n_clicks=0),
        ], className="custom-tabs"),
        
        # Tab Content
        html.Div(id="tab-content", className="fade-in"),
        
    ], className="tab-container"),
    
    # Hidden div to store tab state
    html.Div(id="active-tab", children="state", style={'display': 'none'})
    
], style={
    'background': COLORS['gradient_1'],
    'minHeight': '100vh',
    'fontFamily': FONT_FAMILY
})
# ===========================================
# TAB CONTENT LAYOUTS
# ===========================================

def create_state_analysis_layout():
    """Create the beautiful State Analysis tab layout"""
    return html.Div([
        
        # Control Panel
        html.Div([
            html.Div([
                html.Span("🎯", style={
                    'fontSize': '1.5rem',
                    'marginRight': '1rem',
                    'padding': '10px',
                    'background': COLORS['gradient_1'],
                    'borderRadius': '10px',
                    'color': 'white'
                }),
                html.H3("Analysis Controls", style={'margin': 0, 'color': 'white'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Div([
                    html.Label("📊 Select Category", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="category-dropdown",
                        options=[{"label": k, "value": k} for k in ATTRIBUTE_CATEGORIES.keys()],
                        placeholder="Choose a demographic category...",
                        style={'borderRadius': '12px'}
                    )
                ], style={'marginBottom': '1.5rem'}),
                
                html.Div([
                    html.Label("📈 Select Attribute", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="attribute-dropdown",
                        placeholder="First select a category...",
                        style={'borderRadius': '12px'}
                    )
                ], style={'marginBottom': '1.5rem'}),
            ])
            
        ], style={
            'background': COLORS['gradient_2'],
            'padding': '2rem',
            'borderRadius': '16px',
            'margin': '1.5rem',
            'boxShadow': '0 10px 30px rgba(240, 147, 251, 0.3)'
        }),
        
        # Charts Grid
        html.Div([
            
            # India Map Card
            html.Div([
                html.Div([
                    html.Span("🗺️", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_3'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("India Choropleth Map", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="india-map",
                        style={'height': '500px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # State Rankings Card
            html.Div([
                html.Div([
                    html.Span("🏆", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_2'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("State Rankings", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="state-rankings",
                        style={'height': '500px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
        # Additional Charts Row - First Set
        html.Div([
            
            # Box Plot Card
            html.Div([
                html.Div([
                    html.Span("📦", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_4'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Distribution Summary", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="box-plot",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # Pie Chart Card
            html.Div([
                html.Div([
                    html.Span("🥧", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_5'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Top 7 States", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="top-states-pie",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
        # Additional Charts Row - Second Set (NEW CARDS)
        html.Div([
            
            # Fifth Card
            html.Div([
                html.Div([
                    html.Span("�", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': 'linear-gradient(135deg, #ff9a56 0%, #ffad56 100%)',
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Key Insights", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    html.Div(id="insights-content", style={
                        'background': 'white', 
                        'borderRadius': '16px', 
                        'padding': '1.5rem', 
                        'margin': '1rem 0', 
                        'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)',
                        'minHeight': '350px'
                    })
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # Sixth Card
            html.Div([
                html.Div([
                    html.Span("⭐", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Correlation Heatmap", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="sixth-chart",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
    ])

def create_district_analysis_layout():
    """Create the beautiful District Analysis tab layout"""
    return html.Div([
        # District Analysis Header and Controls
        html.Div([
            html.Div([
                html.Span("🏘️", style={
                    'fontSize': '1.5rem',
                    'marginRight': '1rem',
                    'padding': '10px',
                    'background': COLORS['gradient_1'],
                    'borderRadius': '10px',
                    'color': 'white'
                }),
                html.H3("District Analysis Controls", style={'margin': 0, 'color': 'white'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Div([
                    html.Label("🗺️ Select State", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="district-state-dropdown",
                        placeholder="Choose a state to explore districts...",
                        style={'borderRadius': '12px'}
                    )
                ], style={'marginBottom': '1.5rem', 'marginRight': '1rem', 'flex': '1'}),
                
                html.Div([
                    html.Label("📊 Select District Attribute", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="district-attribute-dropdown",
                        placeholder="First select a state...",
                        style={'borderRadius': '12px'}
                    )
                ], style={'marginBottom': '1.5rem', 'flex': '1'}),
            ], style={'display': 'flex', 'gap': '1rem'})
            
        ], style={
            'background': COLORS['gradient_2'],
            'padding': '2rem',
            'borderRadius': '16px',
            'margin': '1.5rem',
            'boxShadow': '0 10px 30px rgba(240, 147, 251, 0.3)'
        }),
        
        # District Visualizations Grid
        html.Div([
            # District Choropleth Map
            html.Div([
                html.Div([
                    html.Span("🗺️", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_3'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("District Map", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="district-map",
                        style={'height': '500px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # District Rankings
            html.Div([
                html.Div([
                    html.Span("🏆", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_2'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("District Rankings", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="district-rankings",
                        style={'height': '500px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
        # Second Row of District Visualizations
        html.Div([
            # District Performance Matrix
            html.Div([
                html.Div([
                    html.Span("📊", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_4'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Performance Matrix", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="district-scatter",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # District Summary Table
            html.Div([
                html.Div([
                    html.Span("�", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("District Summary Table", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    # Search and Filter Controls
                    html.Div([
                        html.Div([
                            html.Label("🔍 Search Districts:", style={
                                'fontSize': '0.9rem',
                                'fontWeight': '600',
                                'color': '#4a5568',
                                'marginBottom': '0.5rem',
                                'display': 'block'
                            }),
                            dcc.Input(
                                id="district-search",
                                type="text",
                                placeholder="Type district name to search...",
                                style={
                                    'width': '100%',
                                    'padding': '10px 15px',
                                    'border': '2px solid #e2e8f0',
                                    'borderRadius': '8px',
                                    'fontSize': '14px',
                                    'outline': 'none',
                                    'transition': 'border-color 0.2s ease'
                                }
                            )
                        ], style={'flex': '1', 'marginRight': '1rem'}),
                        
                        html.Div([
                            html.Label("📊 Show Top:", style={
                                'fontSize': '0.9rem',
                                'fontWeight': '600',
                                'color': '#4a5568',
                                'marginBottom': '0.5rem',
                                'display': 'block'
                            }),
                            dcc.Dropdown(
                                id="district-table-limit",
                                options=[
                                    {"label": "Top 10", "value": 10},
                                    {"label": "Top 20", "value": 20},
                                    {"label": "Top 50", "value": 50},
                                    {"label": "All Districts", "value": 999}
                                ],
                                value=20,
                                style={'fontSize': '14px'}
                            )
                        ], style={'width': '150px'})
                    ], style={'display': 'flex', 'marginBottom': '1rem', 'alignItems': 'end'}),
                    
                    # Data Table Container
                    html.Div(id="district-summary-table", style={
                        'background': 'white', 
                        'borderRadius': '12px', 
                        'padding': '1rem', 
                        'margin': '1rem 0', 
                        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.1)',
                        'minHeight': '400px',
                        'maxHeight': '500px',
                        'overflowY': 'auto',
                        'border': '1px solid #e2e8f0'
                    })
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
    ])

def create_comparison_layout():
    """Create the beautiful Comparison tab layout"""
    return html.Div([
        html.H2("📊 Comparison Analysis", style={'textAlign': 'center', 'color': COLORS['primary']}),
        html.P("Coming soon...", style={'textAlign': 'center', 'color': COLORS['dark']})
    ])

print("🎨 Beautiful UI layout created successfully!")
print("💫 Color palette and modern design applied!")
print("✅ Using proper inline styles - CSS will work correctly!")

# ===========================================
# STATE NAME MAPPING FOR CHOROPLETH
# ===========================================

def create_state_name_mapping():
    """Create mapping between CSV state names and GeoJSON state names"""
    # Mapping from CSV names (uppercase) to GeoJSON names (title case)
    state_mapping = {
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
    return state_mapping

STATE_NAME_MAPPING = create_state_name_mapping()

print("✅ State name mapping created for choropleth visualization!")

# ===========================================
# DISTRICT DATA LOADING AND PROCESSING
# ===========================================

# Load district data
print("📊 Loading district-wise data...")
try:
    district_data = pd.read_csv('districtwise_data_percentages11_incsv.csv')
    print(f"✅ District data loaded successfully! Shape: {district_data.shape}")
    print(f"📈 Total districts: {len(district_data)}")
    print(f"🗺️ States covered: {district_data['State name'].nunique()}")
    print(f"📊 Attributes available: {len(district_data.columns)}")
    
    # Get percentage columns for district analysis
    district_percentage_cols = [col for col in district_data.columns if col.endswith('_%') and col != 'District code']
    print(f"📈 Percentage columns available: {len(district_percentage_cols)}")
    
except Exception as e:
    print(f"❌ Error loading district data: {e}")
    district_data = pd.DataFrame()
    district_percentage_cols = []

# Create district attribute categories
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

# Filter categories based on available columns
filtered_categories = {}
for category, attributes in DISTRICT_ATTRIBUTE_CATEGORIES.items():
    available_attrs = [attr for attr in attributes if attr in district_data.columns]
    if available_attrs:
        filtered_categories[category] = available_attrs

DISTRICT_ATTRIBUTE_CATEGORIES = filtered_categories
print(f"✅ District attribute categories created: {list(DISTRICT_ATTRIBUTE_CATEGORIES.keys())}")

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

print("✅ District data processing functions created!")

# ===========================================
# INSIGHTS GENERATION FUNCTIONS
# ===========================================

def generate_insights(selected_attribute):
    """Generate 5 key insights about India based on the selected attribute"""
    
    if not selected_attribute:
        return []
    
    try:
        # Prepare data for analysis
        insights_data = state_data[['State name', selected_attribute]].dropna()
        insights_data = insights_data.groupby('State name')[selected_attribute].mean().reset_index()
        
        # Calculate key statistics
        best_state = insights_data.loc[insights_data[selected_attribute].idxmax()]
        worst_state = insights_data.loc[insights_data[selected_attribute].idxmin()]
        national_avg = insights_data[selected_attribute].mean()
        performance_gap = best_state[selected_attribute] - worst_state[selected_attribute]
        above_avg_states = len(insights_data[insights_data[selected_attribute] > national_avg])
        total_states = len(insights_data)
        
        # Calculate additional stats
        top_25_percentile = insights_data[selected_attribute].quantile(0.75)
        top_performers = insights_data[insights_data[selected_attribute] >= top_25_percentile]
        std_dev = insights_data[selected_attribute].std()
        
        # Generate contextual insights based on attribute category
        attribute_lower = selected_attribute.lower()
        
        insights = []
        
        # Insight 1: Best Performer
        insights.append({
            'icon': '🏆',
            'title': 'Top Performer',
            'value': f"{best_state['State name']}",
            'detail': f"{best_state[selected_attribute]:.1f}%",
            'color': '#10b981'
        })
        
        # Insight 2: National Average
        insights.append({
            'icon': '🇮🇳',
            'title': 'National Average',
            'value': f"{national_avg:.1f}%",
            'detail': f"{above_avg_states}/{total_states} states above average",
            'color': '#3b82f6'
        })
        
        # Insight 3: Performance Gap
        insights.append({
            'icon': '📊',
            'title': 'Performance Gap',
            'value': f"{performance_gap:.1f}%",
            'detail': f"Between {best_state['State name']} and {worst_state['State name']}",
            'color': '#f59e0b'
        })
        
        # Insight 4: Context-specific insight
        if 'literacy' in attribute_lower or 'education' in attribute_lower:
            insights.append({
                'icon': '📚',
                'title': 'Education Focus',
                'value': f"{len(top_performers)} states",
                'detail': f"Achieve >75th percentile ({top_25_percentile:.1f}%)",
                'color': '#8b5cf6'
            })
        elif 'employment' in attribute_lower or 'worker' in attribute_lower:
            insights.append({
                'icon': '💼',
                'title': 'Employment Pattern',
                'value': f"±{std_dev:.1f}%",
                'detail': f"Standard deviation across states",
                'color': '#8b5cf6'
            })
        elif 'household' in attribute_lower or 'amenities' in attribute_lower:
            insights.append({
                'icon': '🏠',
                'title': 'Infrastructure',
                'value': f"{len(top_performers)} states",
                'detail': f"Lead in household amenities",
                'color': '#8b5cf6'
            })
        else:
            insights.append({
                'icon': '📈',
                'title': 'Variability',
                'value': f"{std_dev:.1f}%",
                'detail': f"Standard deviation indicates spread",
                'color': '#8b5cf6'
            })
        
        # Insight 5: Bottom performer with improvement potential
        insights.append({
            'icon': '🎯',
            'title': 'Improvement Potential',
            'value': f"{worst_state['State name']}",
            'detail': f"{worst_state[selected_attribute]:.1f}% - Has growth opportunity",
            'color': '#ef4444'
        })
        
        return insights
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        return []
        best_state = insights_data.loc[insights_data[selected_attribute].idxmax()]
        worst_state = insights_data.loc[insights_data[selected_attribute].idxmin()]
        national_avg = insights_data[selected_attribute].mean()
        performance_gap = best_state[selected_attribute] - worst_state[selected_attribute]
        above_avg_states = len(insights_data[insights_data[selected_attribute] > national_avg])
        total_states = len(insights_data)
        
        # Calculate additional stats
        top_25_percentile = insights_data[selected_attribute].quantile(0.75)
        top_performers = insights_data[insights_data[selected_attribute] >= top_25_percentile]
        std_dev = insights_data[selected_attribute].std()
        
        # Generate contextual insights based on attribute category
        attribute_lower = selected_attribute.lower()
        
        insights = []
        
        # Insight 1: Best Performer
        insights.append({
            'icon': '🏆',
            'title': 'Top Performer',
            'value': f"{best_state['State name']}",
            'detail': f"{best_state[selected_attribute]:.1f}%",
            'color': '#10b981'
        })
        
        # Insight 2: National Average
        insights.append({
            'icon': '🇮🇳',
            'title': 'National Average',
            'value': f"{national_avg:.1f}%",
            'detail': f"{above_avg_states}/{total_states} states above average",
            'color': '#3b82f6'
        })
        
        # Insight 3: Performance Gap
        insights.append({
            'icon': '📊',
            'title': 'Performance Gap',
            'value': f"{performance_gap:.1f}%",
            'detail': f"Between {best_state['State name']} and {worst_state['State name']}",
            'color': '#f59e0b'
        })
        
        # Insight 4: Context-specific insight
        if 'literacy' in attribute_lower or 'education' in attribute_lower:
            insights.append({
                'icon': '📚',
                'title': 'Education Focus',
                'value': f"{len(top_performers)} states",
                'detail': f"Achieve >75th percentile ({top_25_percentile:.1f}%)",
                'color': '#8b5cf6'
            })
        elif 'employment' in attribute_lower or 'worker' in attribute_lower:
            insights.append({
                'icon': '💼',
                'title': 'Employment Pattern',
                'value': f"±{std_dev:.1f}%",
                'detail': f"Standard deviation across states",
                'color': '#8b5cf6'
            })
        elif 'household' in attribute_lower or 'amenities' in attribute_lower:
            insights.append({
                'icon': '🏠',
                'title': 'Infrastructure',
                'value': f"{len(top_performers)} states",
                'detail': f"Lead in household amenities",
                'color': '#8b5cf6'
            })
        else:
            insights.append({
                'icon': '📈',
                'title': 'Variability',
                'value': f"{std_dev:.1f}%",
                'detail': f"Standard deviation indicates spread",
                'color': '#8b5cf6'
            })
        
        # Insight 5: Bottom performer with improvement potential
        insights.append({
            'icon': '🎯',
            'title': 'Improvement Potential',
            'value': f"{worst_state['State name']}",
            'detail': f"{worst_state[selected_attribute]:.1f}% - Has growth opportunity",
            'color': '#ef4444'
        })
        
        return insights
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        return []

def create_insights_layout(insights, selected_attribute):
    """Create beautiful HTML layout for insights"""
    
    if not insights:
        return html.Div([
            html.Div([
                html.H3("💡 Select an attribute to see key insights", 
                       style={'textAlign': 'center', 'color': '#64748b', 'margin': '2rem 0'})
            ])
        ])
    
    insight_cards = []
    
    for insight in insights:
        card = html.Div([
            html.Div([
                html.Span(insight['icon'], style={
                    'fontSize': '1.5rem',
                    'marginRight': '0.8rem'
                }),
                html.Div([
                    html.H4(insight['title'], style={
                        'margin': '0 0 0.5rem 0',
                        'fontSize': '0.9rem',
                        'fontWeight': '600',
                        'color': '#64748b',
                        'textTransform': 'uppercase',
                        'letterSpacing': '0.05em'
                    }),
                    html.Div(insight['value'], style={
                        'fontSize': '1.1rem',
                        'fontWeight': '700',
                        'color': insight['color'],
                        'marginBottom': '0.3rem'
                    }),
                    html.P(insight['detail'], style={
                        'fontSize': '0.8rem',
                        'color': '#6b7280',
                        'margin': '0',
                        'lineHeight': '1.4'
                    })
                ], style={'flex': '1'})
            ], style={
                'display': 'flex',
                'alignItems': 'flex-start',
                'padding': '1rem',
                'background': 'linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,250,252,0.9) 100%)',
                'borderRadius': '12px',
                'border': f'1px solid {insight["color"]}20',
                'transition': 'transform 0.2s ease, box-shadow 0.2s ease',
                'cursor': 'default'
            })
        ], style={
            'marginBottom': '0.8rem'
        })
        insight_cards.append(card)
    
    return html.Div([
        html.Div([
            html.H3(f"📊 Key Insights: {get_short_label(selected_attribute)}", 
                   style={
                       'color': '#2d3748',
                       'fontSize': '1.2rem',
                       'fontWeight': '700',
                       'marginBottom': '1.5rem',
                       'textAlign': 'center'
                   })
        ]),
        html.Div(insight_cards, style={
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '0.5rem'
        })
    ])

# Fifth Chart visualization callback - Insights Card
@app.callback(
    Output('insights-content', 'children'),
    [Input('attribute-dropdown', 'value')]
)
def update_insights_card(selected_attribute):
    """Create beautiful insights card with key statistics and observations"""
    
    if not selected_attribute:
        return html.Div([
            html.Div([
                html.Div("💡", style={
                    'fontSize': '3rem',
                    'textAlign': 'center',
                    'marginBottom': '1rem',
                    'opacity': '0.5'
                }),
                html.H3("Select an attribute to discover insights", style={
                    'textAlign': 'center',
                    'color': '#64748b',
                    'fontWeight': '500',
                    'margin': '0'
                }),
                html.P("Choose a category and attribute to see 5 key insights about India's demographic patterns!", style={
                    'textAlign': 'center',
                    'color': '#94a3b8',
                    'marginTop': '0.5rem'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'height': '300px'
            })
        ])
    
    # Generate insights
    insights = generate_insights(selected_attribute)
    
    # Create layout
    return create_insights_layout(insights, selected_attribute)

# ===========================================
# DISTRICT ANALYSIS CALLBACKS
# ===========================================

# District state dropdown callback
@app.callback(
    Output('district-state-dropdown', 'options'),
    [Input('tab-content', 'children')]
)
def update_district_state_dropdown(_):
    """Populate state dropdown for district analysis"""
    if district_data.empty:
        return []
    
    states = sorted(district_data['State name'].unique())
    return [{"label": state, "value": state} for state in states]

# District attribute dropdown callback
@app.callback(
    Output('district-attribute-dropdown', 'options'),
    [Input('district-state-dropdown', 'value')]
)
def update_district_attribute_dropdown(selected_state):
    """Update district attribute dropdown based on available data"""
    if not selected_state or district_data.empty:
        return []
    
    # Get all percentage columns available for the selected state
    state_data = district_data[district_data['State name'] == selected_state]
    available_cols = []
    
    for category, attributes in DISTRICT_ATTRIBUTE_CATEGORIES.items():
        for attr in attributes:
            if attr in state_data.columns and not state_data[attr].isna().all():
                available_cols.append({"label": f"{category}: {get_district_short_label(attr)}", "value": attr})
    
    return available_cols

# District map visualization callback
@app.callback(
    Output('district-map', 'figure'),
    [Input('district-state-dropdown', 'value'),
     Input('district-attribute-dropdown', 'value')]
)
def update_district_map(selected_state, selected_attribute):
    """Create beautiful district-level choropleth map using statewise GeoJSON files"""
    
    if not selected_state:
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="🗺️ District Map - Select a state to explore",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=500,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="Choose a state to see district-level choropleth map! 🗺️",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig
    
    try:
        # Check if we have GeoJSON file for the selected state
        if selected_state not in state_file_map:
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"❌ GeoJSON file not found for {selected_state}",
                title_x=0.5,
                height=500,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[
                    dict(
                        text=f"No district boundaries available for {selected_state}",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=14, color="#ef4444"),
                        showarrow=False
                    )
                ]
            )
            return error_fig
        
        # Load the state-specific GeoJSON file
        state_geojson_file = state_file_map[selected_state]
        with open(state_geojson_file, 'r', encoding='utf-8') as f:
            state_geo = json.load(f)
        
        # Filter district data for selected state
        state_districts = district_data[district_data['State name'] == selected_state].copy()
        
        if not selected_attribute or selected_attribute not in state_districts.columns:
            # Show default state map without data coloring
            default_fig = go.Figure(go.Choropleth(
                geojson=state_geo,
                locations=[],  # Empty locations for default map
                z=[],  # Empty values
                colorscale=[[0, '#e0f2fe'], [1, '#0369a1']],
                marker_line_color='white',
                marker_line_width=1,
                showscale=False
            ))
            
            default_fig.update_geos(
                showframe=False,
                showcoastlines=True,
                coastlinecolor="rgba(255,255,255,0.9)",
                coastlinewidth=1.2,
                projection_type='natural earth',
                fitbounds="geojson",
                bgcolor="rgba(0,0,0,0)"
            )
            
            default_fig.update_layout(
                title=f"🗺️ {selected_state} Districts - Select an attribute to see data",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                margin=dict(l=0, r=0, t=60, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY
            )
            return default_fig
        
        # Create district name mapping for choropleth
        district_names = []
        for feature in state_geo['features']:
            props = feature.get('properties', {})
            district_name = (props.get('district') or 
                           props.get('DISTRICT') or 
                           props.get('name') or 
                           props.get('NAME'))
            if district_name:
                district_names.append(district_name)
        
        # Prepare data for choropleth
        viz_data = state_districts[['District name', selected_attribute]].dropna()
        
        # Create beautiful district choropleth map
        district_map_fig = px.choropleth(
            viz_data,
            geojson=state_geo,
            locations='District name',
            color=selected_attribute,
            featureidkey='properties.district',  # This is correct based on GeoJSON structure
            title=f"🗺️ {selected_state} Districts: {get_district_short_label(selected_attribute)}",
            color_continuous_scale="RdYlBu_r",
            range_color=[viz_data[selected_attribute].min(), viz_data[selected_attribute].max()],
            hover_data=[selected_attribute],
            labels={selected_attribute: f"{get_district_short_label(selected_attribute)} (%)"}
        )
        
        # Configure map projection and styling
        district_map_fig.update_geos(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.9)",
            coastlinewidth=1.2,
            projection_type='natural earth',
            fitbounds="geojson",
            bgcolor="rgba(0,0,0,0)"
        )
        
        # Beautiful styling for district map
        district_map_fig.update_layout(
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#2d3748",
            height=500,
            margin=dict(l=0, r=0, t=60, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            coloraxis_colorbar=dict(
                title=f"{get_district_short_label(selected_attribute)} (%)",
                title_font_size=12,
                title_font_color="#4a5568",
                tickfont=dict(size=10, color="#6b7280"),
                bgcolor="rgba(248,250,252,0.8)",
                bordercolor="rgba(203,213,225,0.5)",
                borderwidth=1,
                len=0.7,
                thickness=15
            )
        )
        
        # Enhanced hover template
        district_map_fig.update_traces(
            hovertemplate="<b>%{location}</b><br>" +
                         f"{get_district_short_label(selected_attribute)}: %{{z:.1f}}%<br>" +
                         "<extra></extra>",
            marker_line_color="white",
            marker_line_width=1.2
        )
        
        return district_map_fig
        
    except Exception as e:
        print(f"Error in district map visualization: {e}")
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"❌ Error loading district map for {selected_state}",
            title_x=0.5,
            height=500,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f"Error: {str(e)[:50]}... Please check console for details.",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=14, color="#ef4444"),
                    showarrow=False
                )
            ]
        )
        return error_fig

# District rankings callback
@app.callback(
    Output('district-rankings', 'figure'),
    [Input('district-state-dropdown', 'value'),
     Input('district-attribute-dropdown', 'value')]
)
def update_district_rankings(selected_state, selected_attribute):
    """Create beautiful district rankings visualization"""
    
    if not selected_state:
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="🏆 District Rankings - Select a state to see rankings",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=500,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="Choose a state and attribute to see district rankings! 📊",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig
    
    try:
        # Filter data for selected state
        state_districts = district_data[district_data['State name'] == selected_state].copy()
        
        if selected_attribute and selected_attribute in state_districts.columns:
            # Sort districts by selected attribute
            rankings_data = state_districts.sort_values(selected_attribute, ascending=False)
            
            # Take top 15 districts for better visualization
            display_data = rankings_data.head(15)
            
            # Create color gradient based on performance
            colors = []
            max_val = display_data[selected_attribute].max()
            min_val = display_data[selected_attribute].min()
            
            for value in display_data[selected_attribute]:
                normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
                if normalized > 0.7:
                    colors.append('#10b981')  # Green for top performers
                elif normalized > 0.4:
                    colors.append('#f59e0b')  # Amber for middle
                else:
                    colors.append('#ef4444')  # Red for low performers
            
            # Create horizontal bar chart
            fig = go.Figure(data=[
                go.Bar(
                    y=display_data['District name'],
                    x=display_data[selected_attribute],
                    orientation='h',
                    marker=dict(
                        color=colors,
                        line=dict(color='rgba(255,255,255,0.8)', width=1)
                    ),
                    hovertemplate="<b>%{y}</b><br>" +
                                 f"{get_district_short_label(selected_attribute)}: %{{x:.1f}}%<br>" +
                                 "<extra></extra>",
                    text=display_data[selected_attribute].round(1),
                    textposition='outside',
                    textfont=dict(size=11, color='#374151')
                )
            ])
            
            fig.update_layout(
                title=f"🏆 District Rankings: {get_district_short_label(selected_attribute)} in {selected_state}",
                title_x=0.5,
                title_font_size=16,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                margin=dict(l=180, r=50, t=80, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY,
                xaxis=dict(
                    title=f"{get_district_short_label(selected_attribute)} (%)",
                    title_font_size=12,
                    title_font_weight="bold",
                    title_font_color="#4a5568",
                    tickfont=dict(size=10, color="#6b7280"),
                    gridcolor="rgba(203,213,225,0.5)",
                    gridwidth=1,
                    showgrid=True
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=10, color="#374151"),
                    showgrid=False,
                    categoryorder='total ascending'
                )
            )
            
        else:
            # Show population rankings if no attribute selected
            rankings_data = state_districts.sort_values('Population', ascending=False)
            display_data = rankings_data.head(15)
            
            fig = go.Figure(data=[
                go.Bar(
                    y=display_data['District name'],
                    x=display_data['Population'],
                    orientation='h',
                    marker=dict(color='#6366f1'),
                    hovertemplate="<b>%{y}</b><br>Population: %{x:,}<br><extra></extra>"
                )
            ])
            
            fig.update_layout(
                title=f"🏆 Districts by Population in {selected_state}",
                title_x=0.5,
                title_font_size=16,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                margin=dict(l=180, r=50, t=80, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY,
                xaxis=dict(title="Population"),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=10, color="#374151"),
                    categoryorder='total ascending'
                )
            )
        
        return fig
        
    except Exception as e:
        print(f"Error in district rankings: {e}")
        error_fig = go.Figure()
        error_fig.update_layout(
            title="❌ Error loading district rankings",
            title_x=0.5,
            height=500,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return error_fig

# District scatter plot callback
@app.callback(
    Output('district-scatter', 'figure'),
    [Input('district-state-dropdown', 'value'),
     Input('district-attribute-dropdown', 'value')]
)
def update_district_scatter(selected_state, selected_attribute):
    """Create district performance matrix scatter plot"""
    
    if not selected_state:
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="📊 Performance Matrix - Select a state to analyze",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="Choose a state to see district performance analysis! 📊",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig
    
    try:
        state_districts = district_data[district_data['State name'] == selected_state].copy()
        
        if selected_attribute and selected_attribute in state_districts.columns:
            # Create scatter plot with Population vs Selected Attribute
            fig = px.scatter(
                state_districts,
                x='Population',
                y=selected_attribute,
                size='Population',
                color=selected_attribute,
                hover_name='District name',
                title=f"📊 Population vs {get_district_short_label(selected_attribute)} in {selected_state}",
                color_continuous_scale="Viridis",
                size_max=30
            )
            
            fig.update_layout(
                title_x=0.5,
                title_font_size=16,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=400,
                margin=dict(l=50, r=50, t=80, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY,
                xaxis=dict(title="Population"),
                yaxis=dict(title=f"{get_district_short_label(selected_attribute)} (%)")
            )
            
        else:
            # Show literacy vs population if no specific attribute
            if 'Literate_%' in state_districts.columns:
                fig = px.scatter(
                    state_districts,
                    x='Population',
                    y='Literate_%',
                    size='Population',
                    color='Literate_%',
                    hover_name='District name',
                    title=f"📊 Population vs Literacy Rate in {selected_state}",
                    color_continuous_scale="Blues",
                    size_max=30
                )
                
                fig.update_layout(
                    title_x=0.5,
                    title_font_size=16,
                    title_font_weight="bold",
                    title_font_color="#2d3748",
                    height=400,
                    margin=dict(l=50, r=50, t=80, b=50),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(248,250,252,0.8)',
                    font_family=FONT_FAMILY,
                    xaxis=dict(title="Population"),
                    yaxis=dict(title="Literacy Rate (%)")
                )
            else:
                fig = go.Figure()
                fig.update_layout(
                    title=f"📊 District Data for {selected_state}",
                    title_x=0.5,
                    height=400,
                    template="plotly_white"
                )
        
        return fig
        
    except Exception as e:
        print(f"Error in district scatter: {e}")
        error_fig = go.Figure()
        error_fig.update_layout(
            title="❌ Error loading district analysis",
            title_x=0.5,
            height=400,
            template="plotly_white"
        )
        return error_fig

# District summary table callback
@app.callback(
    Output('district-summary-table', 'children'),
    [Input('district-state-dropdown', 'value'),
     Input('district-attribute-dropdown', 'value'),
     Input('district-search', 'value'),
     Input('district-table-limit', 'value')]
)
def update_district_summary_table(selected_state, selected_attribute, search_term, limit):
    """Create beautiful interactive district summary table"""
    
    if not selected_state:
        return html.Div([
            html.Div([
                html.Div("📋", style={
                    'fontSize': '4rem',
                    'textAlign': 'center',
                    'marginBottom': '1rem',
                    'opacity': '0.3',
                    'color': '#94a3b8'
                }),
                html.H3("Select a state to view district data table", style={
                    'textAlign': 'center',
                    'color': '#64748b',
                    'fontWeight': '500',
                    'margin': '0'
                }),
                html.P("Choose a state and attribute to see sortable district data!", style={
                    'textAlign': 'center',
                    'color': '#94a3b8',
                    'marginTop': '0.5rem'
                })
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'height': '300px'
            })
        ])
    
    try:
        # Filter data for selected state
        state_districts = district_data[district_data['State name'] == selected_state].copy()
        
        if state_districts.empty:
            return html.Div([
                html.H3("❌ No data available for this state", style={
                    'textAlign': 'center', 
                    'color': '#ef4444',
                    'margin': '2rem 0'
                })
            ])
        
        # Apply search filter if provided
        if search_term:
            search_mask = state_districts['District name'].str.contains(search_term, case=False, na=False)
            state_districts = state_districts[search_mask]
        
        # Select key columns for the table
        display_columns = ['District name']
        
        # Add selected attribute if available
        if selected_attribute and selected_attribute in state_districts.columns:
            display_columns.append(selected_attribute)
        
        # Add other important columns available in the data
        additional_cols = []
        for col in ['Population', 'Literate_%', 'Workers_%', 'Male_%', 'Female_%']:
            if col in state_districts.columns and col not in display_columns:
                additional_cols.append(col)
        
        # Limit additional columns to keep table manageable
        display_columns.extend(additional_cols[:5])
        
        # Filter and sort data
        table_data = state_districts[display_columns].copy()
        
        # Sort by selected attribute if available, otherwise by population
        if selected_attribute and selected_attribute in table_data.columns:
            table_data = table_data.sort_values(selected_attribute, ascending=False)
        elif 'Population' in table_data.columns:
            table_data = table_data.sort_values('Population', ascending=False)
        
        # Apply limit
        if limit and limit < len(table_data):
            table_data = table_data.head(limit)
        
        # Create table headers with beautiful styling
        table_headers = []
        for col in display_columns:
            if col == 'District name':
                header_text = "🏘️ District"
            elif col.endswith('_%'):
                header_text = f"📊 {get_district_short_label(col)}"
            elif col == 'Population':
                header_text = "👥 Population"
            else:
                header_text = col.replace('_', ' ').title()
            
            table_headers.append(
                html.Th(header_text, style={
                    'background': 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                    'color': 'white',
                    'padding': '12px 16px',
                    'textAlign': 'left',
                    'fontWeight': '600',
                    'fontSize': '14px',
                    'borderBottom': '2px solid #e2e8f0',
                    'position': 'sticky',
                    'top': '0',
                    'zIndex': '10'
                })
            )
        
        # Create table rows with beautiful styling and performance indicators
        table_rows = []
        for idx, (_, row) in enumerate(table_data.iterrows()):
            cells = []
            
            for col_idx, col in enumerate(display_columns):
                cell_value = row[col]
                
                # Format cell content based on column type
                if col == 'District name':
                    formatted_value = str(cell_value)
                    cell_style = {
                        'padding': '12px 16px',
                        'borderBottom': '1px solid #f1f5f9',
                        'fontWeight': '600',
                        'color': '#2d3748'
                    }
                elif col == 'Population':
                    formatted_value = f"{int(cell_value):,}" if pd.notna(cell_value) else "N/A"
                    cell_style = {
                        'padding': '12px 16px',
                        'borderBottom': '1px solid #f1f5f9',
                        'textAlign': 'right',
                        'fontFamily': 'monospace',
                        'color': '#4a5568'
                    }
                elif col.endswith('_%'):
                    if pd.notna(cell_value):
                        formatted_value = f"{float(cell_value):.1f}%"
                        # Color coding based on performance
                        if float(cell_value) >= 80:
                            color = '#10b981'  # Green for high
                            bg_color = '#ecfdf5'
                        elif float(cell_value) >= 60:
                            color = '#f59e0b'  # Amber for medium
                            bg_color = '#fffbeb'
                        else:
                            color = '#ef4444'  # Red for low
                            bg_color = '#fef2f2'
                    else:
                        formatted_value = "N/A"
                        color = '#94a3b8'
                        bg_color = '#f8fafc'
                    
                    cell_style = {
                        'padding': '12px 16px',
                        'borderBottom': '1px solid #f1f5f9',
                        'textAlign': 'right',
                        'fontWeight': '600',
                        'color': color,
                        'backgroundColor': bg_color,
                        'borderRadius': '6px',
                        'margin': '2px'
                    }
                else:
                    formatted_value = str(cell_value) if pd.notna(cell_value) else "N/A"
                    cell_style = {
                        'padding': '12px 16px',
                        'borderBottom': '1px solid #f1f5f9',
                        'color': '#4a5568'
                    }
                
                cells.append(html.Td(formatted_value, style=cell_style))
            
            # Alternate row colors for better readability
            row_style = {
                'backgroundColor': '#f8fafc' if idx % 2 == 0 else 'white',
                'transition': 'background-color 0.2s ease',
                'cursor': 'pointer'
            }
            
            table_rows.append(
                html.Tr(cells, style=row_style, className="table-row")
            )
        
        # Create the complete table
        data_table = html.Table([
            html.Thead(html.Tr(table_headers)),
            html.Tbody(table_rows)
        ], style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'fontSize': '14px',
            'fontFamily': FONT_FAMILY,
            'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
            'borderRadius': '8px',
            'overflow': 'hidden'
        })
        
        # Add summary statistics
        total_districts = len(table_data)
        if selected_attribute and selected_attribute in table_data.columns:
            avg_value = table_data[selected_attribute].mean()
            best_district = table_data.iloc[0]['District name']
            best_value = table_data.iloc[0][selected_attribute]
            
            summary_stats = html.Div([
                html.Div([
                    html.Span("📊", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                    html.Strong(f"Showing {total_districts} districts")
                ], style={'marginBottom': '0.5rem'}),
                
                html.Div([
                    html.Span("🏆", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                    html.Strong(f"Best: {best_district} ({best_value:.1f}%)")
                ], style={'marginBottom': '0.5rem'}),
                
                html.Div([
                    html.Span("📈", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                    html.Strong(f"Average: {avg_value:.1f}%")
                ])
            ], style={
                'background': 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
                'padding': '1rem',
                'borderRadius': '8px',
                'marginBottom': '1rem',
                'fontSize': '14px',
                'color': '#0369a1',
                'border': '1px solid #bae6fd'
            })
        else:
            summary_stats = html.Div([
                html.Div([
                    html.Span("📊", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                    html.Strong(f"Showing {total_districts} districts in {selected_state}")
                ])
            ], style={
                'background': 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
                'padding': '1rem',
                'borderRadius': '8px',
                'marginBottom': '1rem',
                'fontSize': '14px',
                'color': '#0369a1',
                'border': '1px solid #bae6fd'
            })
        
        return html.Div([
            summary_stats,
            data_table
        ])
        
    except Exception as e:
        print(f"Error creating district summary table: {e}")
        return html.Div([
            html.H3("❌ Error loading district table", style={
                'textAlign': 'center', 
                'color': '#ef4444',
                'margin': '2rem 0'
            }),
            html.P(f"Error: {str(e)}", style={
                'textAlign': 'center',
                'color': '#94a3b8',
                'fontSize': '12px'
            })
        ])

# District insights callback (REMOVED - replaced with summary table)
# The old update_district_insights callback has been replaced by update_district_summary_table

print("✅ District analysis callbacks created successfully!")

# ===========================================
# INTERACTIVE CALLBACKS
# ===========================================

# Tab switching callback
@app.callback(
    [Output('tab-content', 'children'),
     Output('active-tab', 'children'),
     Output('tab-state', 'className'),
     Output('tab-district', 'className'),
     Output('tab-comparison', 'className')],
    [Input('tab-state', 'n_clicks'),
     Input('tab-district', 'n_clicks'),
     Input('tab-comparison', 'n_clicks')]
)
def update_tab_content(state_clicks, district_clicks, comparison_clicks):
    """Handle tab switching with beautiful transitions"""
    ctx = callback_context
    
    if not ctx.triggered:
        return create_state_analysis_layout(), "state", "custom-tab active", "custom-tab", "custom-tab"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'tab-state':
        return (create_state_analysis_layout(), "state", 
                "custom-tab active", "custom-tab", "custom-tab")
    elif button_id == 'tab-district':
        return (create_district_analysis_layout(), "district",
                "custom-tab", "custom-tab active", "custom-tab")
    elif button_id == 'tab-comparison':
        return (create_comparison_layout(), "comparison",
                "custom-tab", "custom-tab", "custom-tab active")
    
    return create_state_analysis_layout(), "state", "custom-tab active", "custom-tab", "custom-tab"

# Category to attribute dropdown callback
@app.callback(
    Output('attribute-dropdown', 'options'),
    [Input('category-dropdown', 'value')]
)
def update_attribute_dropdown(selected_category):
    """Update attribute dropdown based on selected category"""
    if not selected_category:
        return []
    
    attributes = ATTRIBUTE_CATEGORIES.get(selected_category, [])
    return [{"label": get_short_label(attr), "value": attr} for attr in attributes]

# Main visualization callback for State Analysis - INDIA MAP ONLY
@app.callback(
    Output('india-map', 'figure'),
    [Input('attribute-dropdown', 'value')]
)
def update_india_map(selected_attribute):
    """Update India choropleth map based on selected attribute"""
    
    # Show default India map if no attribute selected
    if not selected_attribute:
        # Create a simple map showing all Indian states with uniform color
        try:
            # Create dummy data for all states to show boundaries
            state_names = []
            for feature in india_geo['features']:
                state_name = feature['properties'].get('name')
                if state_name:
                    state_names.append(state_name)
            
            # Create DataFrame with uniform values to show all states
            dummy_data = pd.DataFrame({
                'state': state_names,
                'value': [1] * len(state_names)  # All states get same value
            })
            
            # Create beautiful default map with gradient colors
            default_fig = px.choropleth(
                dummy_data,
                geojson=india_geo,
                locations='state',
                color='value',
                featureidkey='properties.name',
                title="🗺️ India Map - Select an attribute to see beautiful data visualization",
                color_continuous_scale=["#e0f2fe", "#0369a1", "#1e40af"],  # Beautiful blue gradient
                labels={'value': 'States'}
            )
            
            default_fig.update_geos(
                showframe=False,
                showcoastlines=True,
                coastlinecolor="rgba(255,255,255,0.9)",
                coastlinewidth=1.2,
                projection_type='natural earth',
                fitbounds="locations",
                bgcolor="rgba(0,0,0,0)"
            )
            
            default_fig.update_layout(
                title_x=0.5,
                title_font_size=20,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                margin=dict(l=0, r=0, t=60, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                coloraxis_showscale=False  # Hide color scale for default map
            )
            
            # Add beautiful state borders
            default_fig.update_traces(
                marker_line_color="rgba(255,255,255,0.9)",
                marker_line_width=1.2,
                hovertemplate="<b>%{location}</b><br>Click to explore data<extra></extra>"
            )
            
            return default_fig
            
        except Exception as e:
            print(f"Error creating default India map: {e}")
            # Fallback to simple figure
            fallback_fig = go.Figure()
            fallback_fig.update_layout(
                title="🗺️ India Map Loading...",
                title_x=0.5,
                title_font_size=18,
                height=500,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return fallback_fig
    
    try:
        # Prepare data for visualization
        viz_data = state_data[['State name', selected_attribute]].dropna()
        viz_data = viz_data.groupby('State name')[selected_attribute].mean().reset_index()
        
        # Map CSV state names to GeoJSON state names for choropleth
        viz_data['Mapped_State'] = viz_data['State name'].map(STATE_NAME_MAPPING)
        viz_data = viz_data.dropna(subset=['Mapped_State'])  # Remove states not in mapping
        
        # Beautiful India Choropleth Map with enhanced styling
        india_map_fig = px.choropleth(
            viz_data,
            geojson=india_geo,
            locations='Mapped_State',
            color=selected_attribute,
            featureidkey='properties.name',
            title=f"🗺️ {get_short_label(selected_attribute)} Across Indian States",
            color_continuous_scale="RdYlBu_r",  # Beautiful red-yellow-blue gradient (reversed)
            labels={selected_attribute: f"{get_short_label(selected_attribute)} (%)"},
            hover_name='State name',  # Show original state name on hover
            hover_data={selected_attribute: ':.1f', 'Mapped_State': False}
        )
        
        india_map_fig.update_geos(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.8)",
            coastlinewidth=1,
            projection_type='natural earth',
            fitbounds="locations",
            bgcolor="rgba(0,0,0,0)"
        )
        
        # Enhanced layout with beautiful styling
        india_map_fig.update_layout(
            title_x=0.5,
            title_font_size=20,
            title_font_weight="bold",
            title_font_color="#2d3748",
            height=500,
            margin=dict(l=0, r=0, t=60, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            coloraxis_colorbar=dict(
                title=f"{get_short_label(selected_attribute)} (%)",
                title_font_size=14,
                title_font_weight="bold",
                title_font_color="#2d3748",
                tickfont_size=11,
                tickfont_color="#4a5568",
                len=0.8,
                thickness=15,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1,
                x=1.02
            )
        )
        
        # Add beautiful hover template
        india_map_fig.update_traces(
            hovertemplate="<b>%{hovertext}</b><br>" +
                         f"{get_short_label(selected_attribute)}: %{{z:.1f}}%<br>" +
                         "<extra></extra>",
            marker_line_color="rgba(255,255,255,0.8)",
            marker_line_width=0.8
        )
        
        return india_map_fig
        
    except Exception as e:
        print(f"Error in the India map visualization: {e}")
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"❌ Error loading India map for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
            title_x=0.5,
            height=500,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return error_fig

# State Rankings visualization callback
@app.callback(
    Output('state-rankings', 'figure'),
    [Input('attribute-dropdown', 'value')]
)
def update_state_rankings(selected_attribute):
    """Create beautiful state rankings bar chart"""
    
    # Show placeholder if no attribute selected
    if not selected_attribute:
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="🏆 State Rankings - Select an attribute to see rankings",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=500,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="Choose a category and attribute to see beautiful state rankings! 📊",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig
    
    try:
        # Prepare data for rankings
        rankings_data = state_data[['State name', selected_attribute]].dropna()
        rankings_data = rankings_data.groupby('State name')[selected_attribute].mean().reset_index()
        rankings_data = rankings_data.sort_values(selected_attribute, ascending=False).reset_index(drop=True)
        
        # Take top 15 and bottom 5 states for better visualization
        if len(rankings_data) > 20:
            top_states = rankings_data.head(15)
            bottom_states = rankings_data.tail(5)
            display_data = pd.concat([top_states, bottom_states], ignore_index=True)
        else:
            display_data = rankings_data
        
        # Create beautiful color gradient based on ranking
        colors = []
        max_val = display_data[selected_attribute].max()
        min_val = display_data[selected_attribute].min()
        
        for value in display_data[selected_attribute]:
            # Normalize value between 0 and 1
            normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
            
            # Create color gradient from red (low) to green (high)
            if normalized > 0.7:
                colors.append('#10b981')  # Green for top performers
            elif normalized > 0.4:
                colors.append('#f59e0b')  # Amber for middle
            else:
                colors.append('#ef4444')  # Red for low performers
        
        # Create horizontal bar chart
        rankings_fig = go.Figure(data=[
            go.Bar(
                y=display_data['State name'],
                x=display_data[selected_attribute],
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(255,255,255,0.8)', width=1),
                    pattern=dict(
                        shape="", 
                        size=8, 
                        solidity=0.3
                    )
                ),
                hovertemplate="<b>%{y}</b><br>" +
                             f"{get_short_label(selected_attribute)}: %{{x:.1f}}%<br>" +
                             "<extra></extra>",
                text=display_data[selected_attribute].round(1),
                textposition='outside',
                textfont=dict(size=11, color='#374151')
            )
        ])
        
        # Beautiful styling for rankings chart
        rankings_fig.update_layout(
            title=f"🏆 State Rankings: {get_short_label(selected_attribute)}",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#2d3748",
            height=500,
            margin=dict(l=150, r=50, t=60, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(248,250,252,0.8)',
            font_family=FONT_FAMILY,
            xaxis=dict(
                title=f"{get_short_label(selected_attribute)} (%)",
                title_font_size=14,
                title_font_weight="bold",
                title_font_color="#4a5568",
                tickfont=dict(size=11, color="#6b7280"),
                gridcolor="rgba(203,213,225,0.5)",
                gridwidth=1,
                showgrid=True,
                zeroline=True,
                zerolinecolor="rgba(107,114,128,0.3)",
                zerolinewidth=2
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=11, color="#374151"),
                showgrid=False,
                categoryorder='total ascending'  # Order by value
            ),
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="rgba(0,0,0,0.1)",
                font_size=12,
                font_family=FONT_FAMILY
            )
        )
        
        # Add subtle background gradient
        rankings_fig.add_shape(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            fillcolor="rgba(248,250,252,0.3)",
            layer="below",
            line_width=0
        )
        
        return rankings_fig
        
    except Exception as e:
        print(f"Error in state rankings visualization: {e}")
        print(f"Selected attribute: {selected_attribute}")
        print(f"State data columns: {list(state_data.columns)[:10]}...")  # Print first 10 columns
        print(f"State data shape: {state_data.shape}")
        
        # Check if the column exists
        if selected_attribute in state_data.columns:
            print(f"Column exists. Sample data:")
            print(state_data[['State name', selected_attribute]].head())
        else:
            print(f"Column '{selected_attribute}' not found in state_data")
            
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"❌ Error loading rankings for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
            title_x=0.5,
            height=500,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f"Debug: {str(e)[:100]}...",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=14, color="#ef4444"),
                    showarrow=False
                )
            ]
        )
        return error_fig

# Box Plot Distribution visualization callback
@app.callback(
    Output('box-plot', 'figure'),
    [Input('attribute-dropdown', 'value')]
)
def update_box_plot(selected_attribute):
    """Create beautiful box plot for distribution analysis"""
    
    # Show placeholder if no attribute selected
    if not selected_attribute:
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="📦 Distribution Summary - Select an attribute to analyze",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="Choose a category and attribute to see distribution analysis! 📊",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig
    
    try:
        # Prepare data for box plot
        box_data = state_data[['State name', selected_attribute]].dropna()
        box_data = box_data.groupby('State name')[selected_attribute].mean().reset_index()
        
        # Create beautiful box plot
        box_fig = go.Figure()
        
        # Add the box plot
        box_fig.add_trace(go.Box(
            y=box_data[selected_attribute],
            name=get_short_label(selected_attribute),
            boxpoints='all',  # Show all points
            jitter=0.3,      # Spread points horizontally
            pointpos=-1.8,   # Position points to the left
            marker=dict(
                color='rgba(99, 102, 241, 0.6)',  # Primary color with transparency
                size=8,
                line=dict(color='rgba(99, 102, 241, 0.8)', width=1)
            ),
            line=dict(color='rgba(45, 55, 72, 0.8)', width=2),
            fillcolor='rgba(99, 102, 241, 0.1)',
            hoveron='boxes+points',
            hovertemplate="<b>%{y:.1f}%</b><extra></extra>"
        ))
        
        # Calculate statistics for annotations
        q1 = box_data[selected_attribute].quantile(0.25)
        median = box_data[selected_attribute].median()
        q3 = box_data[selected_attribute].quantile(0.75)
        mean_val = box_data[selected_attribute].mean()
        std_val = box_data[selected_attribute].std()
        
        # Beautiful styling for box plot
        box_fig.update_layout(
            title=f"📦 Distribution: {get_short_label(selected_attribute)}",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#2d3748",
            height=400,
            margin=dict(l=50, r=50, t=60, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(248,250,252,0.8)',
            font_family=FONT_FAMILY,
            showlegend=False,
            yaxis=dict(
                title=f"{get_short_label(selected_attribute)} (%)",
                title_font_size=14,
                title_font_weight="bold",
                title_font_color="#4a5568",
                tickfont=dict(size=11, color="#6b7280"),
                gridcolor="rgba(203,213,225,0.5)",
                gridwidth=1,
                showgrid=True,
                zeroline=False
            ),
            xaxis=dict(
                showgrid=False,
                showticklabels=False,
                zeroline=False
            )
        )
        
        # Add statistics annotations
        box_fig.add_annotation(
            xref="paper", yref="y",
            x=0.02, y=mean_val,
            text=f"Mean: {mean_val:.1f}%",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#10b981",
            font=dict(size=12, color="#059669", weight="bold"),
            bgcolor="rgba(240, 253, 244, 0.8)",
            bordercolor="#10b981",
            borderwidth=1
        )
        
        box_fig.add_annotation(
            xref="paper", yref="y",
            x=0.98, y=median,
            text=f"Median: {median:.1f}%",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#f59e0b",
            font=dict(size=12, color="#d97706", weight="bold"),
            bgcolor="rgba(254, 243, 199, 0.8)",
            bordercolor="#f59e0b",
            borderwidth=1
        )
        
        return box_fig
        
    except Exception as e:
        print(f"Error in box plot visualization: {e}")
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"❌ Error loading distribution for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
            title_x=0.5,
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f"Error: {str(e)[:50]}...",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=14, color="#ef4444"),
                    showarrow=False
                )
            ]
        )
        return error_fig

# Top States Pie Chart visualization callback
@app.callback(
    Output('top-states-pie', 'figure'),
    [Input('attribute-dropdown', 'value')]
)
def update_top_states_pie(selected_attribute):
    """Create beautiful pie chart showing top 7 performing states"""
    
    # Show placeholder if no attribute selected
    if not selected_attribute:
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="🥧 Top 7 States - Select an attribute to see leaders",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="Choose a category and attribute to see top performing states! 🏆",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig
    
    try:
        # Prepare data for pie chart
        pie_data = state_data[['State name', selected_attribute]].dropna()
        pie_data = pie_data.groupby('State name')[selected_attribute].mean().reset_index()
        
        # Get top 7 states
        top_states = pie_data.nlargest(7, selected_attribute)
        
        # Calculate "Others" category for remaining states
        remaining_states = pie_data[~pie_data['State name'].isin(top_states['State name'])]
        others_total = remaining_states[selected_attribute].sum() if len(remaining_states) > 0 else 0
        
        # Create beautiful color palette for pie chart
        colors = [
            '#6366f1',  # Primary indigo
            '#ec4899',  # Pink
            '#10b981',  # Emerald
            '#f59e0b',  # Amber
            '#ef4444',  # Red
            '#8b5cf6',  # Purple
            '#06b6d4',  # Cyan
            '#64748b'   # Gray for others
        ]
        
        # Prepare labels and values
        labels = top_states['State name'].tolist()
        values = top_states[selected_attribute].tolist()
        
        # Add "Others" if there are remaining states
        if others_total > 0:
            labels.append(f"Others ({len(remaining_states)} states)")
            values.append(others_total)
        
        # Create beautiful pie chart
        pie_fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,  # Create a donut chart
            marker=dict(
                colors=colors[:len(labels)],
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textposition='auto',
            textfont=dict(size=11, color='white', weight='bold'),
            hovertemplate="<b>%{label}</b><br>" +
                         f"{get_short_label(selected_attribute)}: %{{value:.1f}}%<br>" +
                         "Share: %{percent}<br>" +
                         "<extra></extra>",
            pull=[0.05 if i == 0 else 0 for i in range(len(labels))]  # Slightly separate the top state
        )])
        
        # Beautiful styling for pie chart
        pie_fig.update_layout(
            title=f"🥧 Top 7 States: {get_short_label(selected_attribute)}",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#2d3748",
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=10, color="#374151"),
                bgcolor="rgba(248,250,252,0.8)",
                bordercolor="rgba(203,213,225,0.5)",
                borderwidth=1
            )
        )
        
        # Add center annotation for donut chart
        total_avg = pie_data[selected_attribute].mean()
        pie_fig.add_annotation(
            text=f"<b>Avg</b><br>{total_avg:.1f}%",
            x=0.5, y=0.5,
            font=dict(size=16, color="#2d3748", weight="bold"),
            showarrow=False,
            align="center"
        )
        
        # Add subtle background
        pie_fig.add_shape(
            type="circle",
            xref="paper", yref="paper",
            x0=0.1, y0=0.1, x1=0.9, y1=0.9,
            fillcolor="rgba(248,250,252,0.3)",
            layer="below",
            line_width=0
        )
        
        return pie_fig
        
    except Exception as e:
        print(f"Error in pie chart visualization: {e}")
        error_fig = go.Figure()
        error_fig.update_layout(
            title=f"❌ Error loading top states for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
            title_x=0.5,
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f"Error: {str(e)[:50]}...",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=14, color="#ef4444"),
                    showarrow=False
                )
            ]
        )
        return error_fig

# Fifth Chart visualization callback (placeholder)
@app.callback(
    Output('fifth-chart', 'figure'),
    [Input('attribute-dropdown', 'value')]
)
def update_fifth_chart(selected_attribute):
    """Placeholder for fifth chart - awaiting specifications"""
    placeholder_fig = go.Figure()
    placeholder_fig.update_layout(
        title="📈 Fifth Visualization - Awaiting Your Instructions",
        title_x=0.5,
        title_font_size=18,
        title_font_weight="bold",
        title_font_color="#64748b",
        height=400,
        template="plotly_white",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family=FONT_FAMILY,
        annotations=[
            dict(
                text="Tell me what visualization you'd like here! 🎨",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                xanchor='center', yanchor='middle',
                font=dict(size=16, color="#94a3b8"),
                showarrow=False
            )
        ]
    )
    return placeholder_fig

# Sixth Chart visualization callback - Correlation Heatmap
@app.callback(
    Output('sixth-chart', 'figure'),
    [Input('attribute-dropdown', 'value')]
)
def update_correlation_heatmap(selected_attribute):
    """Create beautiful correlation heatmap showing relationships between demographic attributes"""
    
    # Show placeholder if no attribute selected
    if not selected_attribute:
        placeholder_fig = go.Figure()
        placeholder_fig.update_layout(
            title="🔥 Correlation Heatmap - Select an attribute to see relationships",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#64748b",
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            annotations=[
                dict(
                    text="Choose an attribute to see stunning correlation analysis! 🔥📊",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=16, color="#94a3b8"),
                    showarrow=False
                )
            ]
        )
        return placeholder_fig
    
    try:
        # Select key demographic metrics for correlation analysis
        correlation_metrics = [
            'Total_Literate_pct',
            'Worker_pct',
            'HouseholdAssets_Computer_pct',
            'HouseholdAssets_Internet_pct',
            'HouseholdAmenities_ElectricityConnection_pct',
            'HouseholdAmenities_CleanFuel_pct',
            'HouseholdAmenities_DrinkingWaterTreated_pct',
            'HouseholdAmenities_Flush_latrine_connected_to_piped_sewer_system_pct',
            'Total_Male_pct',
            'Total_Female_pct'
        ]
        
        # Filter available metrics based on what exists in the data
        available_metrics = [metric for metric in correlation_metrics if metric in state_data.columns]
        
        # If not enough metrics, add more from available columns
        if len(available_metrics) < 8:
            numeric_cols = [col for col in state_data.columns 
                          if col != 'State name' and state_data[col].dtype in ['float64', 'int64'] 
                          and col not in available_metrics]
            available_metrics.extend(numeric_cols[:12-len(available_metrics)])
        
        # Take 8-10 metrics for clean heatmap
        final_metrics = available_metrics[:10]
        
        # Ensure selected attribute is included
        if selected_attribute not in final_metrics:
            final_metrics = [selected_attribute] + final_metrics[:9]
        
        # Prepare correlation data
        corr_data = state_data[['State name'] + final_metrics].dropna()
        corr_data = corr_data.groupby('State name').mean().reset_index()
        
        # Calculate correlation matrix
        correlation_matrix = corr_data[final_metrics].corr()
        
        # Create short labels for better readability
        short_labels = [get_short_label(metric) for metric in final_metrics]
        
        # Create beautiful correlation heatmap
        heatmap_fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=short_labels,
            y=short_labels,
            colorscale=[
                [0, '#ef4444'],      # Strong negative correlation - Red
                [0.25, '#f97316'],   # Moderate negative - Orange  
                [0.4, '#fbbf24'],    # Weak negative - Yellow
                [0.5, '#f8fafc'],    # No correlation - Light gray
                [0.6, '#a7f3d0'],    # Weak positive - Light green
                [0.75, '#34d399'],   # Moderate positive - Green
                [1, '#059669']       # Strong positive - Dark green
            ],
            zmid=0,  # Center colorscale at 0
            zmin=-1,
            zmax=1,
            hoverongaps=False,
            hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>" +
                         "Correlation: %{z:.3f}<br>" +
                         "<extra></extra>",
            showscale=True,
            colorbar=dict(
                title="Correlation<br>Coefficient",
                title_font_size=12,
                title_font_weight="bold",
                title_font_color="#2d3748",
                tickfont=dict(size=10, color="#4a5568"),
                len=0.8,
                thickness=15,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="rgba(0,0,0,0.1)",
                borderwidth=1,
                x=1.02,
                tickvals=[-1, -0.5, 0, 0.5, 1],
                ticktext=['-1.0<br>Strong<br>Negative', '-0.5', '0.0<br>No<br>Relation', '+0.5', '+1.0<br>Strong<br>Positive']
            )
        ))
        
        # Add correlation values as text annotations
        annotations = []
        for i, row in enumerate(correlation_matrix.values):
            for j, value in enumerate(row):
                # Only show text for significant correlations or diagonal
                if abs(value) > 0.3 or i == j:
                    text_color = 'white' if abs(value) > 0.6 else '#2d3748'
                    annotations.append(
                        dict(
                            x=j, y=i,
                            text=f"{value:.2f}",
                            showarrow=False,
                            font=dict(
                                color=text_color,
                                size=10,
                                weight='bold'
                            )
                        )
                    )
        
        # Beautiful styling for heatmap
        heatmap_fig.update_layout(
            title=f"🔥 Correlation Analysis: {get_short_label(selected_attribute)} & Related Metrics",
            title_x=0.5,
            title_font_size=18,
            title_font_weight="bold",
            title_font_color="#2d3748",
            height=400,
            margin=dict(l=100, r=80, t=80, b=100),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_family=FONT_FAMILY,
            xaxis=dict(
                title="",
                tickfont=dict(size=10, color="#374151"),
                tickangle=45,
                side='bottom'
            ),
            yaxis=dict(
                title="",
                tickfont=dict(size=10, color="#374151"),
                autorange='reversed'  # Reverse to match matrix orientation
            ),
            annotations=annotations,
            hoverlabel=dict(
                bgcolor="white",
                bordercolor="rgba(0,0,0,0.1)",
                font_size=12,
                font_family=FONT_FAMILY
            )
        )
        
        # Add subtle border around heatmap
        heatmap_fig.add_shape(
            type="rect",
            xref="x", yref="y",
            x0=-0.5, y0=-0.5,
            x1=len(final_metrics)-0.5, y1=len(final_metrics)-0.5,
            line=dict(color="rgba(45,55,72,0.2)", width=2),
            fillcolor="rgba(0,0,0,0)"
        )
        
        return heatmap_fig
        
    except Exception as e:
        print(f"Error in correlation heatmap: {e}")
        error_fig = go.Figure()
        error_fig.update_layout(
            title="❌ Error loading correlation heatmap",
            title_x=0.5,
            height=400,
            template="plotly_white",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            annotations=[
                dict(
                    text=f"Error: {str(e)[:50]}...",
                    xref="paper", yref="paper",
                    x=0.5, y=0.5,
                    xanchor='center', yanchor='middle',
                    font=dict(size=14, color="#ef4444"),
                    showarrow=False
                )
            ]
        )
        return error_fig

print("🎯 Interactive callbacks added successfully!")
print("🗺️ India choropleth map functionality implemented!")
print("📊 All State Analysis charts are now interactive!")

# ===========================================
# RUN THE APP
# ===========================================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting India Demographics Dashboard...")
    print("🌐 Access your dashboard at: http://127.0.0.1:8080")
    print("🎨 Beautiful visualizations await!")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=8080)
