# =========================
# Imports and Data Loading
# =========================

# Import required libraries for data handling, visualization, and Dash app
import json
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Load India geojson for map visualizations (state boundaries)
with open("india.json", encoding="utf-8") as f:
    india_geo = json.load(f)

# =========================
# State and Population Data
# =========================

# Build mappings between state names and their geojson filenames, dropdown options, and reverse lookup
# This enables flexible handling of state names and file access for map visualizations
state_file_map = {}
state_dropdown_options = []
reverse_state_lookup = {}
for feature in india_geo['features']:
    props = feature.get('properties', {})
    state_name = props.get('st_nm') or props.get('name')
    if state_name:
        key = state_name.lower().replace(" ", "_").replace("-", "_")
        state_file_map[key] = f"{key}.geojson"
        state_dropdown_options.append({"label": state_name, "value": key})
        reverse_state_lookup[state_name] = key

# Hardcoded population data for each state (used for coloring the India map)
# Replace with actual values as needed for more accuracy
population_data = {
    'uttar_pradesh': 199812341,
    'maharashtra': 112374333,
    'bihar': 104099452,
    'west_bengal': 91276115,
    'madhya_pradesh': 72626809,
    'tamil_nadu': 72147030,
    'rajasthan': 68548437,
    'karnataka': 61095297,
    'gujarat': 60439692,
    'andhra_pradesh': 49386799,
    'odisha': 41974218,
    'telangana': 35193978,
    'kerala': 33406061,
    'jharkhand': 32988134,
    'assam': 31205576,
    'punjab': 27743338,
    'chhattisgarh': 25545198,
    'haryana': 25351462,
    'delhi': 16787941,
    'jammu_and_kashmir': 12267032,
    'uttarakhand': 10086292,
    'himachal_pradesh': 6864602,
    'tripura': 3673917,
    'meghalaya': 2966889,
    'manipur': 2855794,
    'nagaland': 1978502,
    'goa': 1458545,
    'arunachal_pradesh': 1383727,
    'mizoram': 1097206,
    'sikkim': 610577,
    'chandigarh': 1055450
    # Add more as needed
}

# =========================
# Attribute and Label Maps
# =========================

# ATTRIBUTE_MAP defines the main attribute categories and their subcategories for analysis
# Used for dropdowns and to select columns from the data for visualizations
ATTRIBUTE_MAP = {
    "Population": ["Male", "Female"],
    "Literacy": ["Male_Literate", "Female_Literate"],
    "Category (Caste)": ["Male_SC", "Female_SC", "Male_ST", "Female_ST"],
    "Employment": [
        "Workers", "Male_Workers", "Female_Workers", "Main_Workers", "Marginal_Workers",
        "Non_Workers", "Cultivator_Workers", "Agricultural_Workers",
        "Household_Workers", "Other_Workers"
    ],
    "Religion": [
        "Hindus", "Muslims", "Sikhs", "Jains", "Buddhists", "Others_Religions", "Religion_Not_Stated"
    ],
    "Household Access": [
        "LPG_or_PNG_Households", "Housholds_with_Electric_Lighting", "Households_with_Internet",
        "Households_with_Computer", "Rural_Households", "Urban_Households", "Households"
    ],
    "Education": [
        "Below_Primary_Education", "Primary_Education", "Middle_Education",
        "Secondary_Education", "Higher_Education", "Graduate_Education",
        "Other_Education", "Literate_Education", "Illiterate_Education", "Total_Education"
    ],
    "Age Group": ["Age_Group_0_29", "Age_Group_30_49", "Age_Group_50", "Age not stated"],
    "Assets": [
        "Households_with_Bicycle", "Households_with_Car_Jeep_Van",
        "Households_with_Scooter_Motorcycle_Moped", "Households_with_Telephone_Mobile_Phone_Landline_only",
        "Households_with_Telephone_Mobile_Phone_Mobile_only", "Households_with_Television",
        "Households_with_Telephone_Mobile_Phone", "Households_with_Telephone_Mobile_Phone_Both",
        "Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car",
        "Ownership_Owned_Households", "Ownership_Rented_Households"
    ],
    "Washroom & Drinking Facilities": [
        "Type_of_latrine_facility_Pit_latrine_Households", "Type_of_latrine_facility_Other_latrine_Households",
        "Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households",
        "Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households",
        "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households",
        "Main_source_of_drinking_water_Un_covered_well_Households", "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households",
        "Main_source_of_drinking_water_Spring_Households", "Main_source_of_drinking_water_River_Canal_Households",
        "Main_source_of_drinking_water_Other_sources_Households", "Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households",
        "Location_of_drinking_water_source_Near_the_premises_Households", "Location_of_drinking_water_source_Within_the_premises_Households",
        "Main_source_of_drinking_water_Tank_Pond_Lake_Households", "Main_source_of_drinking_water_Tapwater_Households",
        "Main_source_of_drinking_water_Tubewell_Borehole_Households", "Location_of_drinking_water_source_Away_Households"
    ],
    "Power Parity": [
        "Power_Parity_Less_than_Rs_45000", "Power_Parity_Rs_45000_90000", "Power_Parity_Rs_90000_150000",
        "Power_Parity_Rs_45000_150000", "Power_Parity_Rs_150000_240000", "Power_Parity_Rs_240000_330000",
        "Power_Parity_Rs_150000_330000", "Power_Parity_Rs_330000_425000", "Power_Parity_Rs_425000_545000",
        "Power_Parity_Rs_330000_545000", "Power_Parity_Above_Rs_545000", "Total_Power_Parity"
    ]
}

# SUBCATEGORY_SHORT_NAMES provides short labels for subcategories for compact axis labels in charts
SUBCATEGORY_SHORT_NAMES = {
    'Male': 'M', 'Female': 'F', 'Male_Literate': 'M Lit', 'Female_Literate': 'F Lit',
    'Male_SC': 'M SC', 'Female_SC': 'F SC', 'Male_ST': 'M ST', 'Female_ST': 'F ST',
    'Workers': 'Workers', 'Male_Workers': 'M Work', 'Female_Workers': 'F Work',
    'Main_Workers': 'Main W', 'Marginal_Workers': 'Marg W', 'Non_Workers': 'Non W',
    'Cultivator_Workers': 'Cultiv', 'Agricultural_Workers': 'Agri', 'Household_Workers': 'HH Work',
    'Other_Workers': 'Other W', 'Hindus': 'Hindu', 'Muslims': 'Muslim', 'Sikhs': 'Sikh',
    'Jains': 'Jain', 'Buddhists': 'Buddh', 'Others_Religions': 'Other Rel',
    'Religion_Not_Stated': 'Rel NS', 'LPG_or_PNG_Households': 'LPG/PNG',
    'Housholds_with_Electric_Lighting': 'Elec', 'Households_with_Internet': 'Internet',
    'Households_with_Computer': 'Computer', 'Rural_Households': 'Rural',
    'Urban_Households': 'Urban', 'Households': 'HH'
}

def short_label(col):
    """
    Returns a short label for a given column name, removing '_pct' if present and using the short name map.
    """
    base = col[:-4] if col.endswith('_pct') else col
    return SUBCATEGORY_SHORT_NAMES.get(base, base)

# =========================
# Dash App Setup
# =========================

# Initialize Dash app with modern styling
app = dash.Dash(__name__)
app.title = "🇮🇳 India Analytics Dashboard"

# =========================
# Modern Layout with Beautiful Design
# =========================

app.layout = html.Div([
    # Beautiful Header with gradient background and KPI stats
    html.Div([
        html.Div([
            html.H1("🇮🇳 India Demographic Analytics Dashboard", 
                    style={'margin': '0', 'color': 'white', 'fontSize': '32px', 'fontWeight': '700', 'textShadow': '0 2px 4px rgba(0,0,0,0.3)'}),
            html.P("Interactive State & District Data Visualization Platform", 
                   style={'margin': '10px 0 0 0', 'color': 'rgba(255,255,255,0.9)', 'fontSize': '18px'})
        ], style={'textAlign': 'center', 'marginBottom': '30px'}),
        
        # KPI Cards Row
        html.Div([
            html.Div([
                html.H3("28", style={'margin': '0', 'color': 'white', 'fontSize': '24px', 'fontWeight': 'bold'}),
                html.P("States", style={'margin': '5px 0 0 0', 'color': 'rgba(255,255,255,0.8)', 'fontSize': '14px'})
            ], style={
                'backgroundColor': 'rgba(255,255,255,0.15)',
                'padding': '15px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'backdropFilter': 'blur(10px)',
                'border': '1px solid rgba(255,255,255,0.2)',
                'width': '18%',
                'display': 'inline-block',
                'margin': '0 1%'
            }),
            html.Div([
                html.H3("700+", style={'margin': '0', 'color': 'white', 'fontSize': '24px', 'fontWeight': 'bold'}),
                html.P("Districts", style={'margin': '5px 0 0 0', 'color': 'rgba(255,255,255,0.8)', 'fontSize': '14px'})
            ], style={
                'backgroundColor': 'rgba(255,255,255,0.15)',
                'padding': '15px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'backdropFilter': 'blur(10px)',
                'border': '1px solid rgba(255,255,255,0.2)',
                'width': '18%',
                'display': 'inline-block',
                'margin': '0 1%'
            }),
            html.Div([
                html.H3("1.4B", style={'margin': '0', 'color': 'white', 'fontSize': '24px', 'fontWeight': 'bold'}),
                html.P("Population", style={'margin': '5px 0 0 0', 'color': 'rgba(255,255,255,0.8)', 'fontSize': '14px'})
            ], style={
                'backgroundColor': 'rgba(255,255,255,0.15)',
                'padding': '15px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'backdropFilter': 'blur(10px)',
                'border': '1px solid rgba(255,255,255,0.2)',
                'width': '18%',
                'display': 'inline-block',
                'margin': '0 1%'
            }),
            html.Div([
                html.H3("50+", style={'margin': '0', 'color': 'white', 'fontSize': '24px', 'fontWeight': 'bold'}),
                html.P("Metrics", style={'margin': '5px 0 0 0', 'color': 'rgba(255,255,255,0.8)', 'fontSize': '14px'})
            ], style={
                'backgroundColor': 'rgba(255,255,255,0.15)',
                'padding': '15px',
                'borderRadius': '12px',
                'textAlign': 'center',
                'backdropFilter': 'blur(10px)',
                'border': '1px solid rgba(255,255,255,0.2)',
                'width': '18%',
                'display': 'inline-block',
                'margin': '0 1%'
            })
        ], style={'textAlign': 'center'})
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'padding': '40px',
        'boxShadow': '0 8px 32px rgba(0,0,0,0.15)'
    }),
    
    # Control Panel - Full Width for Better Organization
    html.Div([
        html.Div([
            html.H3("🎯 Analysis Controls", style={
                'color': '#2d3436', 
                'marginBottom': '25px', 
                'textAlign': 'center',
                'fontSize': '22px',
                'fontWeight': '600'
            }),
            
            # Controls in organized grid
            html.Div([
                # Primary Controls Row - Fixed with proper subcategory dropdown
                html.Div([
                    html.Div([
                        html.Label("📍 Select State", style={'fontWeight': '600', 'color': '#636e72', 'display': 'block', 'marginBottom': '8px'}),
                        dcc.Dropdown(
                            id='state-selector',
                            options=[{"label": "🏠 None", "value": ""}] + [
                                {"label": f"🏛️ {opt['label']}", "value": opt['value']} 
                                for opt in state_dropdown_options
                            ],
                            value="",
                            placeholder="🗺️ Choose a state to analyze...",
                            style={'fontSize': '15px'}
                        )
                    ], style={'width': '32%', 'display': 'inline-block', 'marginRight': '2%'}),
                    
                    html.Div([
                        html.Label("📊 Data Category", style={'fontWeight': '600', 'color': '#636e72', 'display': 'block', 'marginBottom': '8px'}),
                        dcc.Dropdown(
                            id='attribute-category-dropdown',
                            options=[{"label": f"📈 {k}", "value": k} for k in ATTRIBUTE_MAP.keys()],
                            placeholder="📊 Select data category...",
                            style={'fontSize': '15px'}
                        )
                    ], style={'width': '32%', 'display': 'inline-block', 'marginRight': '2%'}),
                    
                    html.Div([
                        html.Label("🔍 Subcategory", style={'fontWeight': '600', 'color': '#636e72', 'display': 'block', 'marginBottom': '8px'}),
                        dcc.Dropdown(
                            id='subcategory-dropdown',
                            placeholder="🔍 Select subcategory...",
                            style={'fontSize': '15px'}
                        )
                    ], style={'width': '32%', 'display': 'inline-block'})
                ], style={'marginBottom': '25px'}),
                
                # Beautiful Feature Cards Row - Filling vacant space
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div("👥", style={'fontSize': '28px', 'marginBottom': '8px'}),
                            html.H4("Demographics", style={'margin': '0', 'color': '#2d3436', 'fontSize': '14px', 'fontWeight': '600'}),
                            html.P("Population insights", style={'margin': '5px 0 0 0', 'color': '#636e72', 'fontSize': '12px'})
                        ], style={
                            'backgroundColor': 'rgba(102, 126, 234, 0.08)',
                            'padding': '20px 15px',
                            'borderRadius': '15px',
                            'textAlign': 'center',
                            'border': '1px solid rgba(102, 126, 234, 0.15)',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer',
                            'boxShadow': '0 4px 15px rgba(102, 126, 234, 0.1)'
                        })
                    ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2.5%'}),
                    
                    html.Div([
                        html.Div([
                            html.Div("📊", style={'fontSize': '28px', 'marginBottom': '8px'}),
                            html.H4("Analytics", style={'margin': '0', 'color': '#2d3436', 'fontSize': '14px', 'fontWeight': '600'}),
                            html.P("Deep insights", style={'margin': '5px 0 0 0', 'color': '#636e72', 'fontSize': '12px'})
                        ], style={
                            'backgroundColor': 'rgba(0, 184, 148, 0.08)',
                            'padding': '20px 15px',
                            'borderRadius': '15px',
                            'textAlign': 'center',
                            'border': '1px solid rgba(0, 184, 148, 0.15)',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer',
                            'boxShadow': '0 4px 15px rgba(0, 184, 148, 0.1)'
                        })
                    ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2.5%'}),
                    
                    html.Div([
                        html.Div([
                            html.Div("🗺️", style={'fontSize': '28px', 'marginBottom': '8px'}),
                            html.H4("Maps", style={'margin': '0', 'color': '#2d3436', 'fontSize': '14px', 'fontWeight': '600'}),
                            html.P("Geographic view", style={'margin': '5px 0 0 0', 'color': '#636e72', 'fontSize': '12px'})
                        ], style={
                            'backgroundColor': 'rgba(253, 121, 168, 0.08)',
                            'padding': '20px 15px',
                            'borderRadius': '15px',
                            'textAlign': 'center',
                            'border': '1px solid rgba(253, 121, 168, 0.15)',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer',
                            'boxShadow': '0 4px 15px rgba(253, 121, 168, 0.1)'
                        })
                    ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2.5%'}),
                    
                    html.Div([
                        html.Div([
                            html.Div("🔗", style={'fontSize': '28px', 'marginBottom': '8px'}),
                            html.H4("Correlations", style={'margin': '0', 'color': '#2d3436', 'fontSize': '14px', 'fontWeight': '600'}),
                            html.P("Relationships", style={'margin': '5px 0 0 0', 'color': '#636e72', 'fontSize': '12px'})
                        ], style={
                            'backgroundColor': 'rgba(108, 92, 231, 0.08)',
                            'padding': '20px 15px',
                            'borderRadius': '15px',
                            'textAlign': 'center',
                            'border': '1px solid rgba(108, 92, 231, 0.15)',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer',
                            'boxShadow': '0 4px 15px rgba(108, 92, 231, 0.1)'
                        })
                    ], style={'width': '18%', 'display': 'inline-block', 'marginRight': '2.5%'}),
                    
                    html.Div([
                        html.Div([
                            html.Div("🏆", style={'fontSize': '28px', 'marginBottom': '8px'}),
                            html.H4("Rankings", style={'margin': '0', 'color': '#2d3436', 'fontSize': '14px', 'fontWeight': '600'}),
                            html.P("Top districts", style={'margin': '5px 0 0 0', 'color': '#636e72', 'fontSize': '12px'})
                        ], style={
                            'backgroundColor': 'rgba(253, 203, 110, 0.08)',
                            'padding': '20px 15px',
                            'borderRadius': '15px',
                            'textAlign': 'center',
                            'border': '1px solid rgba(253, 203, 110, 0.15)',
                            'transition': 'all 0.3s ease',
                            'cursor': 'pointer',
                            'boxShadow': '0 4px 15px rgba(253, 203, 110, 0.1)'
                        })
                    ], style={'width': '18%', 'display': 'inline-block'})
                ], style={'textAlign': 'center'})
            ])
        ], style={
            'backgroundColor': 'white',
            'padding': '35px',
            'borderRadius': '20px',
            'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
            'border': '1px solid rgba(116, 185, 255, 0.1)'
        })
    ], style={
        'padding': '30px 40px 20px 40px',
        'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
    }),
    
    # Main Analytics Grid - Organized Layout
    html.Div([
        # Top Row - Map and Primary Chart
        html.Div([
            # Map Section
            html.Div([
                html.H3("🗺️ Geographic Overview", style={
                    'color': '#2d3436', 
                    'textAlign': 'center', 
                    'marginBottom': '20px',
                    'fontSize': '18px',
                    'fontWeight': '600'
                }),
                dcc.Graph(id='india-map', style={'height': '65vh'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '20px',
                'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
                'width': '48%',
                'display': 'inline-block',
                'marginRight': '2%',
                'border': '1px solid rgba(116, 185, 255, 0.1)'
            }),
            
            # Category Analysis
            html.Div([
                html.H3("📈 Category Analysis", style={
                    'color': '#2d3436', 
                    'textAlign': 'center', 
                    'marginBottom': '20px',
                    'fontSize': '18px',
                    'fontWeight': '600'
                }),
                dcc.Graph(id='district-bar', config={'displayModeBar': False}, style={'height': '65vh'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '20px',
                'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
                'width': '48%',
                'display': 'inline-block',
                'marginLeft': '2%',
                'border': '1px solid rgba(116, 185, 255, 0.1)'
            })
        ], style={'marginBottom': '30px'}),
        
        # Middle Row - Statistical Analysis
        html.Div([
            # Box Plot
            html.Div([
                html.H4("📊 Statistical Distribution", style={
                    'color': '#2d3436', 
                    'textAlign': 'center', 
                    'marginBottom': '15px',
                    'fontSize': '16px',
                    'fontWeight': '600'
                }),
                dcc.Graph(id='box-whisker', style={'height': '35vh'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '20px',
                'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
                'width': '48%',
                'display': 'inline-block',
                'marginRight': '2%',
                'border': '1px solid rgba(116, 185, 255, 0.1)'
            }),
            
            # District Map
            html.Div([
                html.H4("🎯 District Performance", style={
                    'color': '#2d3436', 
                    'textAlign': 'center', 
                    'marginBottom': '15px',
                    'fontSize': '16px',
                    'fontWeight': '600'
                }),
                dcc.Graph(id='state-district-map', style={'height': '35vh'})
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '20px',
                'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
                'width': '48%',
                'display': 'inline-block',
                'marginLeft': '2%',
                'border': '1px solid rgba(116, 185, 255, 0.1)'
            })
        ], style={'marginBottom': '30px'}),
        
        # Bottom Row - Comparison Analysis
        html.Div([
            # Pie Charts Section
            html.Div([
                html.H4("🏆 Performance Rankings", style={
                    'color': '#2d3436', 
                    'textAlign': 'center', 
                    'marginBottom': '20px',
                    'fontSize': '16px',
                    'fontWeight': '600'
                }),
                html.Div([
                    dcc.Graph(id='top5-pie', style={'width': '48%', 'display': 'inline-block', 'height': '30vh'}),
                    dcc.Graph(id='bottom5-pie', style={'width': '48%', 'display': 'inline-block', 'height': '30vh', 'marginLeft': '4%'})
                ])
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '20px',
                'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
                'width': '60%',
                'display': 'inline-block',
                'marginRight': '2%',
                'border': '1px solid rgba(116, 185, 255, 0.1)'
            }),
            
            # Correlation Controls
            html.Div([
                html.H4("🔗 Correlation Setup", style={
                    'color': '#2d3436', 
                    'textAlign': 'center', 
                    'marginBottom': '20px',
                    'fontSize': '16px',
                    'fontWeight': '600'
                }),
                html.Div([
                    html.Label("Second Attribute", style={'fontWeight': '600', 'color': '#636e72', 'display': 'block', 'marginBottom': '8px'}),
                    dcc.Dropdown(
                        id='correlation-attribute-dropdown',
                        options=[{"label": f"📊 {k}", "value": k} for k in ATTRIBUTE_MAP.keys()],
                        placeholder="Select attribute...",
                        style={'fontSize': '14px', 'marginBottom': '15px'}
                    ),
                    html.Label("Subcategory", style={'fontWeight': '600', 'color': '#636e72', 'display': 'block', 'marginBottom': '8px'}),
                    dcc.Dropdown(
                        id='correlation-subcategory-dropdown',
                        placeholder="Select subcategory...",
                        style={'fontSize': '14px'}
                    )
                ])
            ], style={
                'backgroundColor': 'white',
                'padding': '25px',
                'borderRadius': '20px',
                'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
                'width': '36%',
                'display': 'inline-block',
                'marginLeft': '2%',
                'border': '1px solid rgba(116, 185, 255, 0.1)'
            })
        ], style={'marginBottom': '30px'}),
        
        # Final Row - Correlation Results
        html.Div([
            html.H3("🎯 Correlation Analysis Results", style={
                'color': '#2d3436', 
                'textAlign': 'center', 
                'marginBottom': '20px',
                'fontSize': '18px',
                'fontWeight': '600'
            }),
            dcc.Graph(id='correlation-scatter', style={'height': '40vh'}),
            html.Div([
                html.Span(id='correlation-indicator', style={
                    'width': '20px', 
                    'height': '20px', 
                    'borderRadius': '50%', 
                    'display': 'inline-block', 
                    'marginRight': '10px',
                    'border': '2px solid #ddd'
                }),
                html.Span(id='correlation-indicator-label', style={
                    'fontWeight': 'bold', 
                    'marginRight': '15px',
                    'fontSize': '16px',
                    'color': '#2d3436'
                }),
                html.Span(id='correlation-description', style={
                    'color': '#636e72',
                    'fontSize': '14px'
                })
            ], style={
                'textAlign': 'center', 
                'marginTop': '20px',
                'padding': '15px',
                'backgroundColor': 'rgba(116, 185, 255, 0.05)',
                'borderRadius': '10px'
            })
        ], style={
            'backgroundColor': 'white',
            'padding': '30px',
            'borderRadius': '20px',
            'boxShadow': '0 12px 40px rgba(0,0,0,0.08)',
            'border': '1px solid rgba(116, 185, 255, 0.1)'
        })
    ], style={
        'padding': '20px 40px 40px 40px',
        'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        'minHeight': '100vh'
    }),
    
    # Beautiful Footer Section
    html.Div([
        html.Div([
            html.Div([
                html.H4("📊 Dashboard Features", style={'color': 'white', 'marginBottom': '15px', 'fontSize': '16px'}),
                html.P("• Interactive choropleth maps", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("• Statistical distribution analysis", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("• Correlation analysis tools", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("• Performance rankings", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'})
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            html.Div([
                html.H4("🇮🇳 Data Coverage", style={'color': 'white', 'marginBottom': '15px', 'fontSize': '16px'}),
                html.P("• 28 States & 8 Union Territories", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("• 700+ Districts", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("• 50+ Demographic metrics", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("• Real-time visualization", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'})
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '0 5%'}),
            
            html.Div([
                html.H4("⚡ Quick Guide", style={'color': 'white', 'marginBottom': '15px', 'fontSize': '16px'}),
                html.P("1. Select a state from dropdown", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("2. Choose data category", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("3. Pick subcategory for analysis", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'}),
                html.P("4. Explore interactive charts", style={'color': 'rgba(255,255,255,0.8)', 'margin': '5px 0', 'fontSize': '13px'})
            ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'textAlign': 'left', 'maxWidth': '1200px', 'margin': '0 auto'}),
        
        html.Hr(style={'border': '1px solid rgba(255,255,255,0.2)', 'margin': '30px 0'}),
        
        html.Div([
            html.P("🇮🇳 India Demographic Analytics Dashboard | Built with Dash & Plotly", 
                   style={'margin': '0', 'color': 'rgba(255,255,255,0.7)', 'fontSize': '14px'}),
            html.P("Interactive data visualization for demographic insights across Indian states and districts", 
                   style={'margin': '5px 0 0 0', 'color': 'rgba(255,255,255,0.6)', 'fontSize': '12px'})
        ], style={'textAlign': 'center'})
    ], style={
        'background': 'linear-gradient(135deg, #2d3436 0%, #636e72 100%)',
        'padding': '40px',
        'marginTop': '30px'
    })
], style={
    'fontFamily': '"Inter", "Segoe UI", "Roboto", sans-serif',
    'margin': '0',
    'backgroundColor': '#f8f9fa'
})

# =========================
# Plotly Styling
# =========================

PLOTLY_FONT = dict(family='"Inter", "Segoe UI", "Roboto", sans-serif', size=13, color="#2d3436")
MODERN_COLORS = {
    'primary': '#6c5ce7',
    'secondary': '#00b894', 
    'accent': '#fd79a8',
    'gradient': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
}

# =========================
# All Callback Functions
# =========================

@app.callback(
    Output("india-map", "figure"),
    [Input("india-map", "id"), Input("state-selector", "value")]
)
def draw_india_map(_, selected_state):
    locations = []
    pops = []
    
    for f in india_geo['features']:
        props = f.get('properties', {})
        state = props.get('st_nm') or props.get('name')
        if state:
            key = state.lower().replace(" ", "_").replace("-", "_")
            locations.append(state)
            pops.append(population_data.get(key, 0))

    if selected_state:
        color_vals = [1 if (selected_state and key == selected_state) else 0 
                     for key in [s.lower().replace(" ", "_").replace("-", "_") for s in locations]]
        fig = px.choropleth_mapbox(
            geojson=india_geo,
            locations=locations,
            featureidkey="properties.st_nm" if 'st_nm' in india_geo['features'][0]['properties'] else "properties.name",
            color=color_vals,
            color_continuous_scale=['#e6f4ea', '#b10026'],
            range_color=(0, 1),
            mapbox_style="white-bg",
            center={"lat": 22.9734, "lon": 78.6569},
            zoom=3.8,
            opacity=1.0
        )
    else:
        fig = px.choropleth_mapbox(
            geojson=india_geo,
            locations=locations,
            featureidkey="properties.st_nm" if 'st_nm' in india_geo['features'][0]['properties'] else "properties.name",
            color=pops,
            color_continuous_scale="YlOrRd",
            mapbox_style="white-bg",
            center={"lat": 22.9734, "lon": 78.6569},
            zoom=3.8,
            opacity=1.0
        )
    
    fig.update_traces(hovertemplate="%{location}<extra></extra>")
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='white',
        font=PLOTLY_FONT
    )
    return fig

@app.callback(
    Output('district-bar', 'figure'),
    [Input('state-selector', 'value'), Input('attribute-category-dropdown', 'value')]
)
def update_district_bar(selected_state, selected_category):
    if not selected_state or not selected_category:
        return go.Figure().update_layout(
            title="📊 Select a state and category to view data",
            font=PLOTLY_FONT,
            paper_bgcolor='white'
        )
    
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        
        if not state_name:
            return go.Figure()
            
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        subcats = ATTRIBUTE_MAP.get(selected_category, [])
        subcats_pct = [c + '_pct' if c + '_pct' in df_state.columns else c for c in subcats]
        bar_data = {cat: df_state[cat].sum() for cat in subcats_pct if cat in df_state.columns}
        
        x_labels = [short_label(cat) for cat in bar_data.keys()]
        y_vals = list(bar_data.values())
        
        colors = MODERN_COLORS['gradient'][:len(x_labels)] if len(x_labels) > 1 else [MODERN_COLORS['primary']]
        
        fig = go.Figure(go.Bar(
            x=x_labels,
            y=y_vals,
            marker=dict(color=colors, opacity=0.9),
            text=[f'{v:.1f}' for v in y_vals],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"📊 {selected_category} in {state_name}",
            xaxis_title="Categories",
            yaxis_title="Percentage %" if any('_pct' in c for c in subcats_pct) else "Count",
            plot_bgcolor='rgba(248,249,250,0.8)',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=40, r=20, t=60, b=40),
            showlegend=False
        )
        return fig
    except:
        return go.Figure()

@app.callback(
    Output('subcategory-dropdown', 'options'),
    [Input('attribute-category-dropdown', 'value')]
)
def update_subcategory_options(selected_category):
    if not selected_category:
        return []
    subcats = ATTRIBUTE_MAP.get(selected_category, [])
    return [{"label": f"📊 {short_label(c)}", "value": c} for c in subcats]

@app.callback(
    Output('correlation-subcategory-dropdown', 'options'),
    [Input('correlation-attribute-dropdown', 'value')]
)
def update_correlation_subcategory_options(selected_corr_category):
    if not selected_corr_category:
        return []
    subcats = ATTRIBUTE_MAP.get(selected_corr_category, [])
    return [{"label": f"📊 {short_label(c)}", "value": c} for c in subcats]

@app.callback(
    Output('box-whisker', 'figure'),
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_box_whisker(selected_state, selected_subcat):
    if not selected_state or not selected_subcat:
        return go.Figure().update_layout(
            title="📊 Select state and subcategory",
            font=PLOTLY_FONT,
            paper_bgcolor='white'
        )
    
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        df_state = df_state[['District name', col]].dropna()
        
        fig = go.Figure(go.Box(
            y=df_state[col],
            boxpoints='all',
            jitter=0.5,
            name='Districts',
            boxmean=True,
            marker_color=MODERN_COLORS['primary'],
            customdata=df_state['District name'],
            hovertemplate='<b>%{customdata}</b><br>📈 Value: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"📊 {short_label(selected_subcat)} Distribution",
            yaxis_title="Value",
            plot_bgcolor='rgba(248,249,250,0.8)',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            showlegend=False
        )
        return fig
    except:
        return go.Figure()

@app.callback(
    [Output('top5-pie', 'figure'), Output('bottom5-pie', 'figure')],
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_pie_charts(selected_state, selected_subcat):
    if not selected_state or not selected_subcat:
        empty_fig = go.Figure().update_layout(
            title="Select data to view",
            font=PLOTLY_FONT,
            paper_bgcolor='white'
        )
        return empty_fig, empty_fig
    
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        df_state = df_state[['District name', col]].dropna().sort_values(by=col, ascending=False)
        
        top5 = df_state.head(5)
        bottom5 = df_state.tail(5)
        
        # Top 5 pie chart
        top_fig = go.Figure(go.Pie(
            labels=top5['District name'],
            values=top5[col],
            hole=0.4,
            marker=dict(colors=['#00b894', '#00cec9', '#6c5ce7', '#74b9ff', '#fd79a8']),
            hovertemplate='<b>%{label}</b><br>📈 Value: %{value:.2f}<extra></extra>'
        ))
        top_fig.update_layout(
            title='🏆 Top 5',
            font=PLOTLY_FONT,
            showlegend=False,
            paper_bgcolor='white',
            annotations=[dict(text='TOP 5', x=0.5, y=0.5, font=dict(size=14, color='#00b894'), showarrow=False)]
        )
        
        # Bottom 5 pie chart
        bottom_fig = go.Figure(go.Pie(
            labels=bottom5['District name'],
            values=bottom5[col],
            hole=0.4,
            marker=dict(colors=['#e17055', '#d63031', '#e84393', '#fdcb6e', '#fd79a8']),
            hovertemplate='<b>%{label}</b><br>📉 Value: %{value:.2f}<extra></extra>'
        ))
        bottom_fig.update_layout(
            title='📉 Bottom 5',
            font=PLOTLY_FONT,
            showlegend=False,
            paper_bgcolor='white',
            annotations=[dict(text='BOTTOM 5', x=0.5, y=0.5, font=dict(size=14, color='#e17055'), showarrow=False)]
        )
        
        return top_fig, bottom_fig
    except:
        empty_fig = go.Figure()
        return empty_fig, empty_fig

@app.callback(
    Output('state-district-map', 'figure'),
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_state_district_map(selected_state, selected_subcat):
    if not selected_state or not selected_subcat:
        return go.Figure().update_layout(
            title="🗺️ Select state and subcategory",
            font=PLOTLY_FONT,
            paper_bgcolor='white'
        )
    
    try:
        filename = state_file_map.get(selected_state)
        if not filename:
            return go.Figure()
            
        with open(filename, encoding="utf-8") as f:
            state_geo = json.load(f)
            
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        df_state = df_state[['District name', col]].dropna().sort_values(by=col, ascending=False)
        
        top5 = set(df_state.head(5)['District name'])
        bottom5 = set(df_state.tail(5)['District name'])
        
        # Simple district map visualization
        fig = go.Figure()
        
        # Get map center
        all_coords = []
        for feature in state_geo['features']:
            coords = feature['geometry']['coordinates']
            if feature['geometry']['type'] == 'Polygon':
                all_coords.extend(coords[0])
            elif feature['geometry']['type'] == 'MultiPolygon':
                for polygon in coords:
                    all_coords.extend(polygon[0])
        
        if all_coords:
            lats = [c[1] for c in all_coords]
            lons = [c[0] for c in all_coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
        else:
            center_lat, center_lon = 23, 80
        
        # Add district polygons
        for feature in state_geo['features']:
            props = feature.get('properties', {})
            district = props.get('district') or props.get('DISTRICT') or props.get('District')
            if not district:
                continue
                
            color = '#00b894' if district in top5 else '#e17055' if district in bottom5 else '#74b9ff'
            
            geom = feature['geometry']
            if geom['type'] == 'Polygon':
                for coords in geom['coordinates']:
                    lons, lats = zip(*coords)
                    fig.add_trace(go.Scattermapbox(
                        lon=lons, lat=lats,
                        mode='lines',
                        fill='toself',
                        fillcolor=color,
                        line=dict(width=1, color='white'),
                        name=district,
                        hovertemplate=f'<b>{district}</b><extra></extra>',
                        showlegend=False
                    ))
        
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=5.5,
            mapbox_center={"lat": center_lat, "lon": center_lon},
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='white',
            font=PLOTLY_FONT
        )
        return fig
    except:
        return go.Figure()

@app.callback(
    [Output('correlation-scatter', 'figure'),
     Output('correlation-indicator', 'style'),
     Output('correlation-indicator-label', 'children'),
     Output('correlation-description', 'children')],
    [Input('state-selector', 'value'),
     Input('subcategory-dropdown', 'value'),
     Input('correlation-attribute-dropdown', 'value'),
     Input('correlation-subcategory-dropdown', 'value')]
)
def update_correlation_scatter(selected_state, selected_subcat, correlation_attr_cat, correlation_subcat):
    if not all([selected_state, selected_subcat, correlation_attr_cat, correlation_subcat]):
        return (go.Figure().update_layout(title="🎯 Select all parameters for correlation analysis", font=PLOTLY_FONT, paper_bgcolor='white'),
                {'width': '20px', 'height': '20px', 'borderRadius': '50%', 'display': 'inline-block', 'marginRight': '10px', 'backgroundColor': '#ddd'},
                "No Data", "Select all parameters to see correlation analysis")
    
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        x_col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        y_col = correlation_subcat + '_pct' if (correlation_subcat + '_pct') in df_state.columns else correlation_subcat
        
        df_state = df_state[['District name', x_col, y_col]].dropna()
        
        if len(df_state) < 2:
            corr_val = None
        else:
            corr_val = np.corrcoef(df_state[x_col], df_state[y_col])[0, 1]
        
        # Scatter plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_state[x_col],
            y=df_state[y_col],
            mode='markers',
            marker=dict(size=12, color=MODERN_COLORS['primary'], opacity=0.8),
            customdata=df_state['District name'],
            hovertemplate='<b>%{customdata}</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>',
            showlegend=False
        ))
        
        # Add trend line if correlation exists
        if len(df_state) >= 2 and corr_val is not None:
            x_vals, y_vals = df_state[x_col].values, df_state[y_col].values
            m, c = np.polyfit(x_vals, y_vals, 1)
            x_line = np.array([x_vals.min(), x_vals.max()])
            y_line = m * x_line + c
            fig.add_trace(go.Scatter(
                x=x_line, y=y_line,
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                showlegend=False
            ))
        
        fig.update_layout(
            title=f"🎯 {short_label(selected_subcat)} vs {short_label(correlation_subcat)}",
            xaxis_title=short_label(selected_subcat),
            yaxis_title=short_label(correlation_subcat),
            plot_bgcolor='rgba(248,249,250,0.8)',
            paper_bgcolor='white',
            font=PLOTLY_FONT
        )
        
        # Correlation indicator
        if corr_val is not None:
            abs_r = abs(corr_val)
            if abs_r < 0.3:
                color, label = '#e17055', 'Weak'
            elif abs_r > 0.7:
                color, label = '#00b894', 'Strong'
            else:
                color, label = '#fdcb6e', 'Medium'
            
            indicator_style = {
                'width': '20px', 'height': '20px', 'borderRadius': '50%',
                'display': 'inline-block', 'marginRight': '10px',
                'backgroundColor': color, 'border': '2px solid white',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.15)'
            }
            description = f"Correlation coefficient: {corr_val:.3f} - {label} relationship between the two attributes"
        else:
            indicator_style = {'width': '20px', 'height': '20px', 'borderRadius': '50%', 'display': 'inline-block', 'marginRight': '10px', 'backgroundColor': '#ddd'}
            label, description = "No Data", "Insufficient data for correlation analysis"
        
        return fig, indicator_style, label, description
    except:
        return (go.Figure(), 
                {'width': '20px', 'height': '20px', 'borderRadius': '50%', 'display': 'inline-block', 'marginRight': '10px', 'backgroundColor': '#ddd'},
                "Error", "Unable to calculate correlation")

# =========================
# Run the App
# =========================

if __name__ == "__main__":
    app.run(debug=True, port=8052)
