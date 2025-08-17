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
    'Male': 'M',
    'Female': 'F',
    'Male_Literate': 'M Lit',
    'Female_Literate': 'F Lit',
    'Male_SC': 'M SC',
    'Female_SC': 'F SC',
    'Male_ST': 'M ST',
    'Female_ST': 'F ST',
    'Workers': 'Workers',
    'Male_Workers': 'M Work',
    'Female_Workers': 'F Work',
    'Main_Workers': 'Main W',
    'Marginal_Workers': 'Marg W',
    'Non_Workers': 'Non W',
    'Cultivator_Workers': 'Cultiv',
    'Agricultural_Workers': 'Agri',
    'Household_Workers': 'HH Work',
    'Other_Workers': 'Other W',
    'Hindus': 'Hindu',
    'Muslims': 'Muslim',
    'Sikhs': 'Sikh',
    'Jains': 'Jain',
    'Buddhists': 'Buddh',
    'Others_Religions': 'Other Rel',
    'Religion_Not_Stated': 'Rel NS',
    'LPG_or_PNG_Households': 'LPG/PNG',
    'Housholds_with_Electric_Lighting': 'Elec',
    'Households_with_Internet': 'Internet',
    'Households_with_Computer': 'Computer',
    'Rural_Households': 'Rural',
    'Urban_Households': 'Urban',
    'Households': 'HH',
    'Below_Primary_Education': '<Prim',
    'Primary_Education': 'Prim',
    'Middle_Education': 'Mid',
    'Secondary_Education': 'Sec',
    'Higher_Education': 'High',
    'Graduate_Education': 'Grad',
    'Other_Education': 'Other Edu',
    'Literate_Education': 'Lit Edu',
    'Illiterate_Education': 'Illit Edu',
    'Total_Education': 'Tot Edu',
    'Age_Group_0_29': '0-29',
    'Age_Group_30_49': '30-49',
    'Age_Group_50': '50+',
    'Age not stated': 'Age NS',
    'Households_with_Bicycle': 'Bicycle',
    'Households_with_Car_Jeep_Van': 'Car/Jeep',
    'Households_with_Scooter_Motorcycle_Moped': '2Wheeler',
    'Households_with_Telephone_Mobile_Phone_Landline_only': 'Landline',
    'Households_with_Telephone_Mobile_Phone_Mobile_only': 'Mobile',
    'Households_with_Television': 'TV',
    'Households_with_Telephone_Mobile_Phone': 'Phone',
    'Households_with_Telephone_Mobile_Phone_Both': 'Both Ph',
    'Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car': 'All Assets',
    'Ownership_Owned_Households': 'Own HH',
    'Ownership_Rented_Households': 'Rent HH',
    'Type_of_latrine_facility_Pit_latrine_Households': 'Pit Lat',
    'Type_of_latrine_facility_Other_latrine_Households': 'Other Lat',
    'Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households': 'Night Soil',
    'Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households': 'Flush Lat',
    'Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households': 'Open Def',
    'Main_source_of_drinking_water_Un_covered_well_Households': 'Uncov Well',
    'Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households': 'Handpump',
    'Main_source_of_drinking_water_Spring_Households': 'Spring',
    'Main_source_of_drinking_water_River_Canal_Households': 'River',
    'Main_source_of_drinking_water_Other_sources_Households': 'Other Water',
    'Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households': 'All Water',
    'Location_of_drinking_water_source_Near_the_premises_Households': 'Water Near',
    'Location_of_drinking_water_source_Within_the_premises_Households': 'Water In',
    'Main_source_of_drinking_water_Tank_Pond_Lake_Households': 'Tank/Pond',
    'Main_source_of_drinking_water_Tapwater_Households': 'Tap',
    'Main_source_of_drinking_water_Tubewell_Borehole_Households': 'Tubewell',
    'Location_of_drinking_water_source_Away_Households': 'Water Away',
    'Power_Parity_Less_than_Rs_45000': '<45k',
    'Power_Parity_Rs_45000_90000': '45-90k',
    'Power_Parity_Rs_90000_150000': '90-150k',
    'Power_Parity_Rs_45000_150000': '45-150k',
    'Power_Parity_Rs_150000_240000': '150-240k',
    'Power_Parity_Rs_240000_330000': '240-330k',
    'Power_Parity_Rs_150000_330000': '150-330k',
    'Power_Parity_Rs_330000_425000': '330-425k',
    'Power_Parity_Rs_425000_545000': '425-545k',
    'Power_Parity_Rs_330000_545000': '330-545k',
    'Power_Parity_Above_Rs_545000': '>545k',
    'Total_Power_Parity': 'Tot PP',
}

def short_label(col):
    """
    Returns a short label for a given column name, removing '_pct' if present and using the short name map.
    """
    base = col[:-4] if col.endswith('_pct') else col
    return SUBCATEGORY_SHORT_NAMES.get(base, base)

# =========================
# Dash App Layout
# =========================

# Initialize Dash app and set the title
app = dash.Dash(__name__)
app.title = "India State Analytics Dashboard"

# =========================
# Custom CSS Styling
# =========================

# Modern gradient and styling
HEADER_STYLE = {
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'color': 'white',
    'padding': '20px 30px',
    'boxShadow': '0 4px 20px rgba(0,0,0,0.15)',
    'marginBottom': '0',
    'borderRadius': '0',
    'position': 'relative',
    'overflow': 'hidden'
}

CARD_STYLE = {
    'backgroundColor': 'white',
    'borderRadius': '16px',
    'boxShadow': '0 8px 32px rgba(0,0,0,0.12)',
    'border': '1px solid rgba(255,255,255,0.2)',
    'backdrop-filter': 'blur(10px)',
    'padding': '20px',
    'margin': '10px',
    'transition': 'all 0.3s ease',
    'position': 'relative'
}

KPI_CARD_STYLE = {
    'backgroundColor': 'rgba(255,255,255,0.95)',
    'borderRadius': '12px',
    'boxShadow': '0 4px 16px rgba(0,0,0,0.1)',
    'padding': '16px 20px',
    'margin': '0 10px',
    'textAlign': 'center',
    'minWidth': '150px',
    'backdrop-filter': 'blur(10px)',
    'border': '1px solid rgba(255,255,255,0.3)'
}

MODERN_BUTTON_STYLE = {
    'backgroundColor': '#6c5ce7',
    'color': 'white',
    'border': 'none',
    'borderRadius': '8px',
    'padding': '10px 20px',
    'fontSize': '14px',
    'fontWeight': '600',
    'cursor': 'pointer',
    'transition': 'all 0.3s ease',
    'boxShadow': '0 4px 16px rgba(108, 92, 231, 0.3)'
}

# Define the overall layout of the dashboard with modern design
app.layout = html.Div([
    # =========================
    # HEADER SECTION
    # =========================
    html.Div([
        # Header Background Decoration
        html.Div(style={
            'position': 'absolute',
            'top': '-50%',
            'right': '-20%',
            'width': '300px',
            'height': '300px',
            'background': 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
            'borderRadius': '50%'
        }),
        
        # Main Header Content
        html.Div([
            # Title and Subtitle
            html.Div([
                html.H1("🇮🇳 India Demographic Analytics", style={
                    'margin': '0',
                    'fontSize': '32px',
                    'fontWeight': '700',
                    'letterSpacing': '0.5px',
                    'background': 'linear-gradient(45deg, #ffffff, #f1f2f6)',
                    'webkitBackgroundClip': 'text',
                    'backgroundClip': 'text',
                    'webkitTextFillColor': 'transparent'
                }),
                html.P("Interactive State & District Data Visualization Platform", style={
                    'margin': '5px 0 0 0',
                    'fontSize': '16px',
                    'opacity': '0.9',
                    'fontWeight': '400',
                    'letterSpacing': '0.3px'
                })
            ], style={'flex': '1'}),
            
            # KPI Cards Row
            html.Div([
                html.Div([
                    html.Div("🏛️", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Div("36", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#6c5ce7'}),
                    html.Div("States & UTs", style={'fontSize': '12px', 'color': '#666', 'fontWeight': '500'})
                ], style=KPI_CARD_STYLE),
                
                html.Div([
                    html.Div("🏘️", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Div("750+", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#00b894'}),
                    html.Div("Districts", style={'fontSize': '12px', 'color': '#666', 'fontWeight': '500'})
                ], style=KPI_CARD_STYLE),
                
                html.Div([
                    html.Div("👥", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Div("1.4B+", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#e17055'}),
                    html.Div("Population", style={'fontSize': '12px', 'color': '#666', 'fontWeight': '500'})
                ], style=KPI_CARD_STYLE),
                
                html.Div([
                    html.Div("📊", style={'fontSize': '24px', 'marginBottom': '8px'}),
                    html.Div("12", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': '#fd79a8'}),
                    html.Div("Categories", style={'fontSize': '12px', 'color': '#666', 'fontWeight': '500'})
                ], style=KPI_CARD_STYLE)
            ], style={
                'display': 'flex',
                'justifyContent': 'flex-end',
                'alignItems': 'center',
                'gap': '0'
            })
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'position': 'relative',
            'zIndex': '2'
        })
    ], style=HEADER_STYLE),
    
    # =========================
    # MAIN CONTENT AREA
    # =========================
    html.Div([
        # Control Panel Card (Full Width)
        html.Div([
            html.Div([
                html.Div("🎯 Analysis Controls", style={
                    'fontSize': '18px',
                    'fontWeight': '600',
                    'color': '#2d3436',
                    'marginBottom': '16px',
                    'display': 'flex',
                    'alignItems': 'center'
                }),
                
                # Enhanced Dropdowns Row
                html.Div([
                    html.Div([
                        html.Label("Select State", style={
                            'fontSize': '12px',
                            'fontWeight': '600',
                            'color': '#636e72',
                            'marginBottom': '6px',
                            'display': 'block'
                        }),
                        dcc.Dropdown(
                            id='state-selector',
                            options=[{"label": "🏠 None", "value": ""}] + [
                                {"label": f"🏛️ {opt['label']}", "value": opt['value']} 
                                for opt in state_dropdown_options
                            ],
                            value="",
                            placeholder="Choose a state to analyze...",
                            style={
                                "fontSize": "14px",
                                "height": "45px",
                                "borderRadius": "8px",
                                "border": "2px solid #ddd",
                                "fontWeight": "500"
                            }
                        )
                    ], style={'width': '30%', 'marginRight': '5%'}),
                    
                    html.Div([
                        html.Label("Analysis Category", style={
                            'fontSize': '12px',
                            'fontWeight': '600',
                            'color': '#636e72',
                            'marginBottom': '6px',
                            'display': 'block'
                        }),
                        dcc.Dropdown(
                            id='attribute-category-dropdown',
                            options=[{"label": f"📊 {k}", "value": k} for k in ATTRIBUTE_MAP.keys()],
                            placeholder="Select data category...",
                            style={
                                "fontSize": "14px",
                                "height": "45px",
                                "borderRadius": "8px",
                                "border": "2px solid #ddd",
                                "fontWeight": "500"
                            }
                        )
                    ], style={'width': '30%', 'marginRight': '5%'}),
                    
                    html.Div([
                        html.Label("Detailed Analysis", style={
                            'fontSize': '12px',
                            'fontWeight': '600',
                            'color': '#636e72',
                            'marginBottom': '6px',
                            'display': 'block'
                        }),
                        dcc.Dropdown(
                            id='subcategory-dropdown',
                            placeholder="Select subcategory for detailed view...",
                            style={
                                'fontSize': '14px',
                                'height': '45px',
                                'borderRadius': '8px',
                                'border': '2px solid #ddd'
                            }
                        )
                    ], style={'width': '30%'})
                ], style={'display': 'flex', 'marginBottom': '20px'})
            ], style={'padding': '0'})
        ], style={**CARD_STYLE, 'marginBottom': '15px', 'padding': '24px'}),
        
        # TOP ROW: India Map + Category Analysis
        html.Div([
            # --- LEFT: India Map ---
            html.Div([
                html.Div([
                    html.Div("�️ India Overview Map", style={
                        'fontSize': '18px',
                        'fontWeight': '600',
                        'color': '#2d3436',
                        'marginBottom': '16px',
                        'textAlign': 'center'
                    }),
                    dcc.Graph(
                        id='india-map', 
                        style={
                            'height': '55vh', 
                            'width': '100%'
                        },
                        config={
                            'displayModeBar': False,
                            'scrollZoom': False,
                            'doubleClick': False,
                            'showTips': False
                        }
                    )
                ])
            ], style={**CARD_STYLE, 'width': '48%', 'display': 'inline-block', 'marginRight': '2%', 'verticalAlign': 'top'}),

            # --- RIGHT: Category Analysis ---
            html.Div([
                html.Div([
                    html.Div("📈 Category Breakdown", style={
                        'fontSize': '18px',
                        'fontWeight': '600',
                        'color': '#2d3436',
                        'marginBottom': '16px',
                        'textAlign': 'center'
                    }),
                    dcc.Graph(
                        id='district-bar', 
                        config={'displayModeBar': False}, 
                        style={'height': '60vh', 'width': '100%'}
                    )
                ])
            ], style={**CARD_STYLE, 'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'marginBottom': '15px'}),

        # --- ANALYTICS ROW ---
        html.Div([
            
        # --- ANALYTICS ROW ---
        html.Div([
            # Analytics Row (Box Plot + District Map)
            html.Div([
                # Box Plot Card
                html.Div([
                    html.Div("📊 Statistical Summary", style={
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'color': '#2d3436',
                        'marginBottom': '12px',
                        'textAlign': 'center'
                    }),
                    dcc.Graph(
                        id='box-whisker', 
                        style={'height': '26vh', 'width': '100%'}
                    )
                ], style={**CARD_STYLE, 'width': '48%', 'marginRight': '2%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                # District Map Card
                html.Div([
                    html.Div("🎯 District Highlights", style={
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'color': '#2d3436',
                        'marginBottom': '12px',
                        'textAlign': 'center'
                    }),
                    dcc.Graph(
                        id='state-district-map', 
                        style={'height': '26vh', 'width': '100%'},
                        config={
                            'displayModeBar': False,
                            'scrollZoom': False,
                            'doubleClick': False
                        }
                    )
                ], style={**CARD_STYLE, 'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ], style={'marginBottom': '15px'}),
            
            # Correlation and Pie Charts Row
            html.Div([
                # Correlation Controls Card
                html.Div([
                    html.Div("🔗 Correlation Analysis", style={
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'color': '#2d3436',
                        'marginBottom': '12px',
                        'textAlign': 'center'
                    }),
                    html.Div([
                        dcc.Dropdown(
                            id='correlation-attribute-dropdown',
                            options=[{"label": f"📊 {k}", "value": k} for k in ATTRIBUTE_MAP.keys()],
                            placeholder="Select attribute...",
                            style={
                                'fontSize': '13px',
                                'height': '35px',
                                'marginBottom': '8px',
                                'borderRadius': '6px'
                            }
                        ),
                        dcc.Dropdown(
                            id='correlation-subcategory-dropdown',
                            placeholder="Select subcategory...",
                            style={
                                'fontSize': '13px',
                                'height': '35px',
                                'borderRadius': '6px'
                            }
                        )
                    ])
                ], style={**CARD_STYLE, 'width': '28%', 'marginRight': '2%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                
                # Pie Charts Card
                html.Div([
                    html.Div("🥧 Top & Bottom Performers", style={
                        'fontSize': '16px',
                        'fontWeight': '600',
                        'color': '#2d3436',
                        'marginBottom': '12px',
                        'textAlign': 'center'
                    }),
                    html.Div([
                        dcc.Graph(id='top5-pie', style={
                            'display': 'inline-block', 
                            'width': '48%', 
                            'height': '22vh', 
                            'marginRight': '2%'
                        }),
                        dcc.Graph(id='bottom5-pie', style={
                            'display': 'inline-block', 
                            'width': '48%', 
                            'height': '22vh'
                        })
                    ])
                ], style={**CARD_STYLE, 'width': '68%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ], style={'marginBottom': '15px'}),
            
            # Correlation Scatter Plot Card
            html.Div([
                html.Div("🎯 Relationship Analysis", style={
                    'fontSize': '18px',
                    'fontWeight': '600',
                    'color': '#2d3436',
                    'marginBottom': '16px',
                    'textAlign': 'center'
                }),
                dcc.Graph(
                    id='correlation-scatter', 
                    style={'height': '26vh', 'width': '100%', 'marginBottom': '16px'}
                ),
                # Enhanced Correlation Indicator
                html.Div([
                    html.Span(id='correlation-indicator', style={
                        'display': 'inline-block',
                        'width': '20px',
                        'height': '20px',
                        'borderRadius': '50%',
                        'marginRight': '12px',
                        'verticalAlign': 'middle',
                        'border': '2px solid #ddd',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.15)'
                    }),
                    html.Span(id='correlation-indicator-label', style={
                        'fontWeight': '700',
                        'fontSize': '14px',
                        'verticalAlign': 'middle',
                        'marginRight': '12px',
                        'color': '#2d3436'
                    }),
                    html.Span(id='correlation-description', style={
                        'fontSize': '13px',
                        'color': '#636e72',
                        'backgroundColor': '#f8f9fa',
                        'borderRadius': '8px',
                        'padding': '10px 16px',
                        'boxShadow': '0 2px 8px rgba(0,0,0,0.08)',
                        'display': 'inline-block',
                        'width': 'calc(100% - 140px)',
                        'lineHeight': '1.4'
                    })
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'width': '100%',
                    'padding': '12px 0'
                })
            ], style={**CARD_STYLE, 'marginBottom': '15px'})
        ])
    ], style={
        'padding': '20px 30px',
        'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        'minHeight': '100vh'
    })
])
], style={
    'fontFamily': '"Inter", "Segoe UI", "Roboto", sans-serif',
    'margin': '0',
    'padding': '0',
    'backgroundColor': '#f8f9fa'
})

# =========================
# India Map Callback
# =========================

@app.callback(
    Output("india-map", "figure"),
    [Input("india-map", "id"), Input("state-selector", "value")]
)
def draw_india_map(_, selected_state):
    """
    Draws the main India map. If a state is selected, highlights it with a pop-out effect and colors it by population.
    All other states are colored with a very light green. If no state is selected, all states are colored by population.
    """
    locations = []
    pops = []
    color_vals = []
    selected_color = '#b10026'  # dark red for selected
    faded_color = '#e6f4ea'     # very light green for others
    for f in india_geo['features']:
        props = f.get('properties', {})
        state = props.get('st_nm') or props.get('name')
        if state:
            key = state.lower().replace(" ", "_").replace("-", "_")
            locations.append(state)
            pops.append(population_data.get(key, 0))
            if selected_state and key == selected_state:
                color_vals.append(selected_color)
            elif selected_state:
                color_vals.append(faded_color)
            else:
                color_vals.append(None)  # Use default color scale if nothing selected

    if selected_state:
        # Custom coloring: selected state dark, others faded
        fig = px.choropleth_mapbox(
            geojson=india_geo,
            locations=locations,
            featureidkey="properties.st_nm" if 'st_nm' in india_geo['features'][0]['properties'] else "properties.name",
            color=[1 if (selected_state and key == selected_state) else 0 for key in [s.lower().replace(" ", "_").replace("-", "_") for s in locations]],
            color_continuous_scale=[faded_color, selected_color],
            range_color=(0, 1),
            mapbox_style="white-bg",
            center={"lat": 20.5937, "lon": 78.9629},
            zoom=4.2,
            opacity=1.0,
            labels={'color': 'Selected'}
        )
    else:
        # Default: color all states by population
        fig = px.choropleth_mapbox(
            geojson=india_geo,
            locations=locations,
            featureidkey="properties.st_nm" if 'st_nm' in india_geo['features'][0]['properties'] else "properties.name",
            color=pops,
            color_continuous_scale="YlOrRd",
            mapbox_style="white-bg",
            center={"lat": 20.5937, "lon": 78.9629},
            zoom=4.2,
            opacity=1.0,
            labels={'color': 'Population'}
        )
    fig.update_traces(
        hovertemplate="%{location}<extra></extra>"
    )
    fig.update_layout(
        clickmode='event+select',
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor='white',
        plot_bgcolor='white',
        autosize=True,
        coloraxis_colorbar=dict(
            title="Population" if not selected_state else "Selected",
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=0.02,
            thickness=12,
            len=0.6
        )
    )
    return fig

# =========================
# Plotly Font Settings
# =========================

# Updated modern font settings for all Plotly charts
PLOTLY_FONT = dict(
    family='"Inter", "Segoe UI", "Roboto", "Helvetica Neue", sans-serif', 
    size=13, 
    color="#2d3436"
)

# Modern color palettes
MODERN_COLORS = {
    'primary': '#6c5ce7',
    'secondary': '#00b894', 
    'accent': '#fd79a8',
    'warning': '#fdcb6e',
    'success': '#00b894',
    'info': '#74b9ff',
    'gradient': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
}

# =========================
# District Bar Chart Callback
# =========================

@app.callback(
    Output('district-bar', 'figure'),
    [Input('state-selector', 'value'), Input('attribute-category-dropdown', 'value')]
)
def update_district_bar(selected_state, selected_category):
    """
    Draws a bar chart showing the breakdown of the selected attribute category's subcategories for the selected state.
    Uses a gradient color palette and log scale if values vary widely.
    """
    if not selected_state or not selected_category:
        return go.Figure()
    df = pd.read_csv('districtwise_data_percentages.csv')
    # Find the state name from the selected key
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
    y_vals = list(bar_data.values())
    x_labels = [short_label(cat) for cat in bar_data.keys()]
    use_log = False
    if len(y_vals) > 0 and max(y_vals) > 0 and min(y_vals) > 0:
        if max(y_vals) / min(y_vals) > 50:
            use_log = True
    # Enhanced gradient color palette for bars
    colors = MODERN_COLORS['gradient'][:len(x_labels)] if len(x_labels) > 1 else [MODERN_COLORS['primary']]
    
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=y_vals,
        marker=dict(
            color=colors,
            line=dict(width=0),
            opacity=0.95,
        ),
        text=[f'{v:.1f}' for v in y_vals],
        textposition='outside' if max(y_vals) > 0 else 'inside',
        textfont=dict(color='white', weight='bold', size=12),
        width=0.8,
        hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>',
    ))
    
    fig.update_layout(
        title=dict(
            text=f"📊 {selected_category} Analysis in {state_name}",
            font=dict(size=16, weight='bold', color=MODERN_COLORS['primary']),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=dict(text="Categories", font=PLOTLY_FONT),
        yaxis_title=dict(
            text="Percentage %" if any('_pct' in c for c in subcats_pct) else "Count",
            font=PLOTLY_FONT
        ),
        plot_bgcolor='rgba(248,249,250,0.8)',
        paper_bgcolor='white',
        font=PLOTLY_FONT,
        margin=dict(l=40, r=20, t=60, b=40),
        yaxis_type='log' if use_log else 'linear',
        yaxis=dict(
            rangemode='tozero',
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)',
            zerolinecolor='rgba(200,200,200,0.4)',
            tickfont=PLOTLY_FONT
        ),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(size=11, color=PLOTLY_FONT['color']),
            automargin=True,
            showgrid=False
        ),
        bargap=0.3,
        showlegend=False,
        hovermode='x unified'
    )
    return fig

# =========================
# Box-Whisker Plot Callback
# =========================

@app.callback(
    Output('box-whisker', 'figure'),
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_box_whisker_new(selected_state, selected_subcat):
    """
    Draws a box-whisker plot for the selected subcategory across all districts in the selected state.
    Shows distribution, outliers, and mean for the chosen metric.
    """
    from dash.exceptions import PreventUpdate
    if not selected_state or not selected_subcat:
        raise PreventUpdate
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        # Get state name for lookup
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            return go.Figure()
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        if col not in df_state.columns:
            return go.Figure()
        df_state = df_state[['District name', col]].dropna()
        # Enhanced box-whisker plot for district values
        fig = go.Figure(go.Box(
            y=df_state[col],
            boxpoints='all',
            jitter=0.5,
            pointpos=0,
            name='Districts',
            boxmean=True,
            marker=dict(
                color=MODERN_COLORS['primary'],
                size=8,
                line=dict(width=2, color='white')
            ),
            line_color=MODERN_COLORS['primary'],
            fillcolor=f"rgba({int(MODERN_COLORS['primary'][1:3], 16)}, {int(MODERN_COLORS['primary'][3:5], 16)}, {int(MODERN_COLORS['primary'][5:7], 16)}, 0.2)",
            customdata=df_state['District name'],
            hovertemplate='<b>%{customdata}</b><br>📈 Value: %{y:.2f}<extra></extra>',
        ))
        
        fig.update_layout(
            title=dict(
                text=f"📊 {short_label(selected_subcat)} Distribution in {state_name}",
                font=dict(size=14, weight='bold', color=MODERN_COLORS['primary']),
                x=0.5,
                xanchor='center'
            ),
            yaxis_title=dict(
                text="Percentage %" if '_pct' in col else "Count",
                font=PLOTLY_FONT
            ),
            plot_bgcolor='rgba(248,249,250,0.8)',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=40, r=20, t=50, b=30),
            showlegend=False,
            height=220,
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(200,200,200,0.2)',
                zeroline=False,
                tickfont=PLOTLY_FONT
            ),
            xaxis=dict(showgrid=False, tickfont=PLOTLY_FONT)
        )
        return fig
    except Exception as e:
        print("Box-whisker error:", e)
        return go.Figure()

# =========================
# Top/Bottom 5 Pie Charts Callback
# =========================

@app.callback(
    Output('top5-pie', 'figure'),
    Output('bottom5-pie', 'figure'),
    [Input('state-selector', 'value'),
     Input('subcategory-dropdown', 'value')]
)
def update_pie_charts(selected_state, selected_subcat):
    """
    Draws two pie charts: one for the top 5 and one for the bottom 5 districts in the selected state,
    based on the selected subcategory. Uses pastel color palettes for visual clarity.
    """
    if not selected_state or not selected_subcat:
        return go.Figure(), go.Figure()
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            return go.Figure(), go.Figure()
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        if col not in df_state.columns:
            return go.Figure(), go.Figure()
        df_state = df_state[['District name', col]].dropna()
        df_state = df_state.sort_values(by=col, ascending=False)
        top5 = df_state.head(5)
        bottom5 = df_state.tail(5)
        # Modern gradient colors for pie charts
        top_colors = ['#00b894', '#00cec9', '#6c5ce7', '#74b9ff', '#fd79a8']
        bottom_colors = ['#e17055', '#d63031', '#e84393', '#fdcb6e', '#fd79a8']
        
        # Top 5 pie chart with modern styling
        top_fig = go.Figure(go.Pie(
            labels=top5['District name'],
            values=top5[col],
            hole=0.4,
            marker=dict(
                colors=top_colors,
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=10, color='white', weight='bold'),
            pull=[0.05, 0.02, 0.02, 0.02, 0.02],
            hovertemplate='<b>%{label}</b><br>📈 Value: %{value:.2f}<br>Share: %{percent}<extra></extra>'
        ))
        top_fig.update_layout(
            title=dict(
                text='🏆 Top 5 Districts',
                font=dict(size=14, weight='bold', color=MODERN_COLORS['success']),
                x=0.5,
                xanchor='center'
            ),
            margin=dict(l=10, r=10, t=50, b=10),
            showlegend=False,
            height=220,
            font=PLOTLY_FONT,
            annotations=[dict(
                text='TOP 5', 
                x=0.5, y=0.5, 
                font=dict(size=16, weight='bold', color=MODERN_COLORS['success']), 
                showarrow=False
            )],
            paper_bgcolor='white',
        )
        
        # Bottom 5 pie chart with modern styling
        bottom_fig = go.Figure(go.Pie(
            labels=bottom5['District name'],
            values=bottom5[col],
            hole=0.4,
            marker=dict(
                colors=bottom_colors,
                line=dict(color='white', width=3)
            ),
            textinfo='label+percent',
            textfont=dict(size=10, color='white', weight='bold'),
            pull=[0.05, 0.02, 0.02, 0.02, 0.02],
            hovertemplate='<b>%{label}</b><br>📉 Value: %{value:.2f}<br>Share: %{percent}<extra></extra>'
        ))
        bottom_fig.update_layout(
            title=dict(
                text='📉 Bottom 5 Districts',
                font=dict(size=14, weight='bold', color=MODERN_COLORS['accent']),
                x=0.5,
                xanchor='center'
            ),
            margin=dict(l=10, r=10, t=50, b=10),
            showlegend=False,
            height=220,
            font=PLOTLY_FONT,
            annotations=[dict(
                text='BOTTOM 5', 
                x=0.5, y=0.5, 
                font=dict(size=16, weight='bold', color=MODERN_COLORS['accent']), 
                showarrow=False
            )],
            paper_bgcolor='white',
        )
        return top_fig, bottom_fig
    except Exception:
        return go.Figure(), go.Figure()

# =========================
# Subcategory Dropdown Options Callback
# =========================

@app.callback(
    Output('subcategory-dropdown', 'options'),
    [Input('attribute-category-dropdown', 'value')]
)
def update_subcategory_options(selected_category):
    """
    Updates the subcategory dropdown options based on the selected attribute category.
    """
    if not selected_category:
        return []
    subcats = ATTRIBUTE_MAP.get(selected_category, [])
    # Log/print the subcategories for demonstration
    print("Available subcategories:", subcats)
    return [{"label": short_label(c), "value": c} for c in subcats]

# =========================
# Correlation Subcategory Dropdown Callback
# =========================

@app.callback(
    Output('correlation-subcategory-dropdown', 'options'),
    [Input('correlation-attribute-dropdown', 'value')]
)
def update_correlation_subcategory_options(selected_corr_category):
    """
    Updates the correlation subcategory dropdown options based on the selected correlation attribute category.
    """
    if not selected_corr_category:
        return []
    subcats = ATTRIBUTE_MAP.get(selected_corr_category, [])
    return [{"label": short_label(c), "value": c} for c in subcats]

# =========================
# State District Map Callback
# =========================

from dash.exceptions import PreventUpdate

@app.callback(
    Output('state-district-map', 'figure'),
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_state_district_map(selected_state, selected_subcat):
    """
    Draws a map of the selected state, coloring each district by the selected subcategory.
    Top 5 districts are colored green, bottom 5 red, others blue. Used for quick visual comparison.
    """
    if not selected_state or not selected_subcat:
        raise PreventUpdate
    try:
        # Load state geojson for district boundaries
        filename = state_file_map.get(selected_state)
        if not filename:
            return go.Figure()
        with open(filename, encoding="utf-8") as f:
            state_geo = json.load(f)
        # Load data
        df = pd.read_csv('districtwise_data_percentages.csv')
        # Get state name for lookup
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            return go.Figure()
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        if col not in df_state.columns:
            return go.Figure()
        # Prepare district values and sort for top/bottom 5
        df_state = df_state[['District name', col]].dropna()
        df_state = df_state.sort_values(by=col, ascending=False)
        top5 = set(df_state.head(5)['District name'])
        bottom5 = set(df_state.tail(5)['District name'])
        # Color mapping for each district
        color_map = {}
        for d in df_state['District name']:
            if d in top5:
                color_map[d] = '#43aa8b'  # green
            elif d in bottom5:
                color_map[d] = '#f94144'  # red
            else:
                color_map[d] = '#277da1'  # blue
        # Get map center for zoom
        all_coords = []
        for feature in state_geo['features']:
            geom_type = feature['geometry']['type']
            coords = feature['geometry']['coordinates']
            if geom_type == 'Polygon':
                all_coords.extend(coords[0])
            elif geom_type == 'MultiPolygon':
                for polygon in coords:
                    all_coords.extend(polygon[0])
        if all_coords:
            lats = [c[1] for c in all_coords]
            lons = [c[0] for c in all_coords]
            center_lat = sum(lats) / len(lats)
            center_lon = sum(lons) / len(lons)
        else:
            center_lat, center_lon = 23, 80
        # Draw polygons for each district, colored by rank
        fig = go.Figure()
        for feature in state_geo['features']:
            props = feature.get('properties', {})
            district = props.get('district') or props.get('DISTRICT') or props.get('District')
            if not district:
                continue
            color = color_map.get(district, '#277da1')
            geom = feature['geometry']
            if geom['type'] == 'Polygon':
                for coords in geom['coordinates']:
                    lons, lats = zip(*coords)
                    fig.add_trace(go.Scattermapbox(
                        lon=lons, lat=lats,
                        mode='lines',
                        fill='toself',
                        fillcolor=color,
                        line=dict(width=1.5, color='white'),
                        name=district,
                        hoverinfo='text',
                        text=f"{district}: {col} = {df_state[df_state['District name']==district][col].values[0]:.2f}" if district in df_state['District name'].values else district,
                        showlegend=False
                    ))
            elif geom['type'] == 'MultiPolygon':
                for polygon in geom['coordinates']:
                    for coords in polygon:
                        lons, lats = zip(*coords)
                        fig.add_trace(go.Scattermapbox(
                            lon=lons, lat=lats,
                            mode='lines',
                            fill='toself',
                            fillcolor=color,
                            line=dict(width=1.5, color='white'),
                            name=district,
                            hoverinfo='text',
                            text=f"{district}: {col} = {df_state[df_state['District name']==district][col].values[0]:.2f}" if district in df_state['District name'].values else district,
                            showlegend=False
                        ))
        fig.update_layout(
            mapbox_style="carto-positron",
            mapbox_zoom=5.8,
            mapbox_center={"lat": center_lat, "lon": center_lon},
            margin={"r":5,"t":5,"l":5,"b":5},
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            hovermode='closest',
            autosize=True,
            height=None
        )
        return fig
    except Exception as e:
        print("District map error:", e)
        return go.Figure()

# =========================
# Correlation Scatter Plot Callback
# =========================


# Updated correlation scatter callback to match four outputs for indicator and description
@app.callback(
    Output('correlation-scatter', 'figure'),
    Output('correlation-indicator', 'style'),
    Output('correlation-indicator-label', 'children'),
    Output('correlation-description', 'children'),
    [Input('state-selector', 'value'),
     Input('subcategory-dropdown', 'value'),
     Input('correlation-attribute-dropdown', 'value'),
     Input('correlation-subcategory-dropdown', 'value')]
)
def update_correlation_scatter_v2(selected_state, selected_subcat, correlation_attr_cat, correlation_subcat):
    from dash.exceptions import PreventUpdate
    if not selected_state or not selected_subcat or not correlation_attr_cat or not correlation_subcat:
        # Default indicator and description
        indicator_style = {
            'display': 'inline-block',
            'width': '18px',
            'height': '18px',
            'borderRadius': '4px',
            'marginRight': '10px',
            'verticalAlign': 'middle',
            'border': '1.5px solid #bbb',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.07)',
            'backgroundColor': '#f8d7da'
        }
        return go.Figure(), indicator_style, "Unrelated", "Select a state and two attributes to see their relationship across districts."
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        # Get state name for lookup
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            indicator_style = {
                'display': 'inline-block',
                'width': '18px',
                'height': '18px',
                'borderRadius': '4px',
                'marginRight': '10px',
                'verticalAlign': 'middle',
                'border': '1.5px solid #bbb',
                'boxShadow': '0 1px 4px rgba(0,0,0,0.07)',
                'backgroundColor': '#f8d7da'
            }
            return go.Figure(), indicator_style, "Unrelated", "No data for this state."
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        x_col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        y_col = correlation_subcat + '_pct' if (correlation_subcat + '_pct') in df_state.columns else correlation_subcat
        if x_col not in df_state.columns or y_col not in df_state.columns:
            indicator_style = {
                'display': 'inline-block',
                'width': '18px',
                'height': '18px',
                'borderRadius': '4px',
                'marginRight': '10px',
                'verticalAlign': 'middle',
                'border': '1.5px solid #bbb',
                'boxShadow': '0 1px 4px rgba(0,0,0,0.07)',
                'backgroundColor': '#f8d7da'
            }
            return go.Figure(), indicator_style, "Unrelated", "Selected attributes not available for this state."
        df_state = df_state[['District name', x_col, y_col]].dropna()
        if len(df_state) < 2:
            corr_val = None
        else:
            corr_val = np.corrcoef(df_state[x_col], df_state[y_col])[0, 1]
        # Scatter plot for district values (no text labels)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_state[x_col],
            y=df_state[y_col],
            mode='markers',
            marker=dict(
                size=13,
                color=df_state[x_col],
                colorscale='Viridis',
                line=dict(width=1, color='#277da1'),
                opacity=0.85,
            ),
            hovertemplate='X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>',
            showlegend=False
        ))
        # Add best-fit line if enough points
        if len(df_state) >= 2:
            x_vals = df_state[x_col].values
            y_vals = df_state[y_col].values
            m, c = np.polyfit(x_vals, y_vals, 1)
            x_line = np.array([x_vals.min(), x_vals.max()])
            y_line = m * x_line + c
            fig.add_trace(go.Scatter(
                x=x_line,
                y=y_line,
                mode='lines',
                line=dict(color='black', width=2, dash='dash'),
                name='Best Fit',
                hoverinfo='skip',
                showlegend=False
            ))
        fig.update_layout(
            title=f"Correlation: {short_label(selected_subcat)} vs {short_label(correlation_subcat)} in {state_name}",
            xaxis_title=short_label(selected_subcat),
            yaxis_title=short_label(correlation_subcat),
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=30, r=10, t=40, b=30),
            height=220,
        )
        desc = f"Each point represents a district in {state_name}. The X-axis shows the value for '{short_label(selected_subcat)}', and the Y-axis shows the value for '{short_label(correlation_subcat)}'. If the points form a clear pattern (like a line), the two attributes are related. If the points are scattered randomly, the attributes are likely unrelated."
        # Indicator box logic (color and label based on correlation strength)
        if corr_val is not None:
            desc += f"<br/><b>Correlation coefficient (r):</b> {corr_val:.2f}. "
            abs_r = abs(corr_val)
            if abs_r < 0.2:
                color = '#f94144'
                label = 'Unrelated'
            elif abs_r > 0.7:
                color = '#43aa8b'
                label = 'Strongly related'
            else:
                color = '#f9c846'
                label = 'Somewhat related'
            indicator_style = {
                'display': 'inline-block',
                'width': '18px',
                'height': '18px',
                'borderRadius': '4px',
                'marginRight': '10px',
                'verticalAlign': 'middle',
                'border': '1.5px solid #bbb',
                'boxShadow': '0 1px 4px rgba(0,0,0,0.07)',
                'backgroundColor': color
            }
        else:
            indicator_style = {
                'display': 'inline-block',
                'width': '18px',
                'height': '18px',
                'borderRadius': '4px',
                'marginRight': '10px',
                'verticalAlign': 'middle',
                'border': '1.5px solid #bbb',
                'boxShadow': '0 1px 4px rgba(0,0,0,0.07)',
                'backgroundColor': '#f8d7da'
            }
            label = 'Unrelated'
        return fig, indicator_style, label, desc
    except Exception as e:
        print("Correlation scatter error:", e)
        indicator_style = {
            'display': 'inline-block',
            'width': '18px',
            'height': '18px',
            'borderRadius': '4px',
            'marginRight': '10px',
            'verticalAlign': 'middle',
            'border': '1.5px solid #bbb',
            'boxShadow': '0 1px 4px rgba(0,0,0,0.07)',
            'backgroundColor': '#f8d7da'
        }
        return go.Figure(), indicator_style, "Unrelated", "Unable to display correlation."


# =========================
# Main Entrypoint
# =========================

if __name__ == "__main__":
    # Run the Dash app in debug mode, default localhost only
    app.run(debug=True, port=8051)