# =========================
# Imports and Data Loading
# =========================

import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import json

# Load India geojson for map visualizations (state boundaries)
with open("india.json", encoding="utf-8") as f:
    india_geo = json.load(f)

# =========================
# State and Population Data
# =========================

# Build mappings between state names and their geojson filenames, dropdown options, and reverse lookup
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

# Hardcoded population data for each state
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
}

# =========================
# Attribute and Label Maps
# =========================

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

# SUBCATEGORY_SHORT_NAMES provides short labels for subcategories
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
    # ... (truncated for brevity, include all mappings from original)
}

def short_label(col):
    """Returns a short label for a given column name."""
    base = col[:-4] if col.endswith('_pct') else col
    return SUBCATEGORY_SHORT_NAMES.get(base, base)

# =========================
# Styling
# =========================

SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': '0',
    'left': '0',
    'bottom': '0',
    'width': '320px',
    'padding': '20px',
    'backgroundColor': '#2c3e50',
    'color': 'white',
    'overflowY': 'auto',
    'zIndex': '1000',
    'boxShadow': '4px 0 20px rgba(0,0,0,0.15)',
    'transition': 'all 0.3s ease'
}

MAIN_CONTENT_STYLE = {
    'marginLeft': '340px',
    'padding': '20px',
    'backgroundColor': '#f8f9fa',
    'minHeight': '100vh'
}

SLIDER_SECTION_STYLE = {
    'backgroundColor': 'rgba(255,255,255,0.1)',
    'borderRadius': '12px',
    'padding': '20px',
    'marginBottom': '20px',
    'border': '1px solid rgba(255,255,255,0.2)'
}

CARD_STYLE = {
    'backgroundColor': 'white',
    'borderRadius': '16px',
    'boxShadow': '0 8px 32px rgba(0,0,0,0.12)',
    'padding': '20px',
    'margin': '15px 0',
    'border': '1px solid rgba(255,255,255,0.2)'
}

PLOTLY_FONT = dict(family='"Inter", sans-serif', size=13, color="#2d3436")

MODERN_COLORS = {
    'primary': '#6c5ce7',
    'secondary': '#00b894',
    'accent': '#fd79a8',
    'gradient': ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe']
}

# =========================
# Dash App Layout
# =========================

app = dash.Dash(__name__)
app.title = "India Analytics Dashboard - Slider Layout"

app.layout = html.Div([
    # ======= COLLAPSIBLE SIDEBAR =======
    html.Div([
        # Header
        html.Div([
            html.H3("🇮🇳 India Analytics", style={
                'color': 'white',
                'margin': '0 0 10px 0',
                'fontSize': '22px',
                'fontWeight': '700'
            }),
            html.P("Interactive Dashboard", style={
                'margin': '0',
                'opacity': '0.8',
                'fontSize': '14px'
            })
        ], style={'marginBottom': '30px', 'textAlign': 'center'}),
        
        # ===== SLIDER PANEL 1: DATA CONTROLS =====
        html.Div([
            html.Div([
                html.H4("🎯 Data Controls", style={
                    'color': '#ecf0f1',
                    'margin': '0 0 15px 0',
                    'fontSize': '16px',
                    'fontWeight': '600'
                }),
                
                # State Selector
                html.Div([
                    html.Label("Select State:", style={
                        'color': '#bdc3c7',
                        'fontSize': '12px',
                        'fontWeight': '500',
                        'marginBottom': '5px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='state-selector',
                        options=[{"label": "🏠 None", "value": ""}] + [
                            {"label": f"🏛️ {opt['label']}", "value": opt['value']} 
                            for opt in state_dropdown_options
                        ],
                        value="",
                        placeholder="Choose state...",
                        style={
                            'fontSize': '13px',
                            'color': '#2c3e50',
                            'marginBottom': '15px'
                        }
                    )
                ]),
                
                # Category Dropdown
                html.Div([
                    html.Label("Analysis Category:", style={
                        'color': '#bdc3c7',
                        'fontSize': '12px',
                        'fontWeight': '500',
                        'marginBottom': '5px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='attribute-category-dropdown',
                        options=[{"label": f"📊 {k}", "value": k} for k in ATTRIBUTE_MAP.keys()],
                        placeholder="Select category...",
                        style={
                            'fontSize': '13px',
                            'color': '#2c3e50',
                            'marginBottom': '15px'
                        }
                    )
                ]),
                
                # Subcategory Dropdown
                html.Div([
                    html.Label("Detailed View:", style={
                        'color': '#bdc3c7',
                        'fontSize': '12px',
                        'fontWeight': '500',
                        'marginBottom': '5px',
                        'display': 'block'
                    }),
                    dcc.Dropdown(
                        id='subcategory-dropdown',
                        placeholder="Select subcategory...",
                        style={
                            'fontSize': '13px',
                            'color': '#2c3e50'
                        }
                    )
                ])
            ])
        ], style=SLIDER_SECTION_STYLE),
        
        # ===== SLIDER PANEL 2: QUICK STATS =====
        html.Div([
            html.H4("📊 Quick Stats", style={
                'color': '#ecf0f1',
                'margin': '0 0 15px 0',
                'fontSize': '16px',
                'fontWeight': '600'
            }),
            
            # KPI Cards in Sidebar
            html.Div([
                html.Div([
                    html.Div("🏛️", style={'fontSize': '20px', 'marginBottom': '5px'}),
                    html.Div("36", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#3498db'}),
                    html.Div("States", style={'fontSize': '10px', 'opacity': '0.8'})
                ], style={
                    'textAlign': 'center',
                    'backgroundColor': 'rgba(255,255,255,0.1)',
                    'borderRadius': '8px',
                    'padding': '12px',
                    'marginBottom': '10px'
                }),
                
                html.Div([
                    html.Div("🏘️", style={'fontSize': '20px', 'marginBottom': '5px'}),
                    html.Div("750+", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#2ecc71'}),
                    html.Div("Districts", style={'fontSize': '10px', 'opacity': '0.8'})
                ], style={
                    'textAlign': 'center',
                    'backgroundColor': 'rgba(255,255,255,0.1)',
                    'borderRadius': '8px',
                    'padding': '12px',
                    'marginBottom': '10px'
                }),
                
                html.Div([
                    html.Div("👥", style={'fontSize': '20px', 'marginBottom': '5px'}),
                    html.Div("1.4B+", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#e74c3c'}),
                    html.Div("Population", style={'fontSize': '10px', 'opacity': '0.8'})
                ], style={
                    'textAlign': 'center',
                    'backgroundColor': 'rgba(255,255,255,0.1)',
                    'borderRadius': '8px',
                    'padding': '12px'
                })
            ])
        ], style=SLIDER_SECTION_STYLE),
        
        # ===== SLIDER PANEL 3: CORRELATION SETTINGS =====
        html.Div([
            html.H4("🔗 Correlation", style={
                'color': '#ecf0f1',
                'margin': '0 0 15px 0',
                'fontSize': '16px',
                'fontWeight': '600'
            }),
            
            html.Div([
                html.Label("Compare With:", style={
                    'color': '#bdc3c7',
                    'fontSize': '12px',
                    'fontWeight': '500',
                    'marginBottom': '5px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='correlation-attribute-dropdown',
                    options=[{"label": f"📊 {k}", "value": k} for k in ATTRIBUTE_MAP.keys()],
                    placeholder="Select attribute...",
                    style={
                        'fontSize': '13px',
                        'color': '#2c3e50',
                        'marginBottom': '10px'
                    }
                )
            ]),
            
            html.Div([
                html.Label("Subcategory:", style={
                    'color': '#bdc3c7',
                    'fontSize': '12px',
                    'fontWeight': '500',
                    'marginBottom': '5px',
                    'display': 'block'
                }),
                dcc.Dropdown(
                    id='correlation-subcategory-dropdown',
                    placeholder="Select subcategory...",
                    style={
                        'fontSize': '13px',
                        'color': '#2c3e50'
                    }
                )
            ])
        ], style=SLIDER_SECTION_STYLE)
        
    ], style=SIDEBAR_STYLE),
    
    # ======= MAIN CONTENT AREA =======
    html.Div([
        # Header Bar
        html.Div([
            html.H1("India Demographic Analytics Dashboard", style={
                'margin': '0',
                'fontSize': '28px',
                'fontWeight': '700',
                'color': '#2c3e50',
                'textAlign': 'center'
            }),
            html.P("Interactive State & District Data Visualization", style={
                'margin': '5px 0 0 0',
                'fontSize': '16px',
                'color': '#7f8c8d',
                'textAlign': 'center'
            })
        ], style={
            'backgroundColor': 'white',
            'borderRadius': '16px',
            'padding': '20px',
            'marginBottom': '20px',
            'boxShadow': '0 4px 20px rgba(0,0,0,0.1)'
        }),
        
        # Top Row: India Map + Arrow + District Map + Category Analysis
        html.Div([
            # India Map
            html.Div([
                html.Div([
                    html.H3("🗺️ India Overview", style={
                        'margin': '0 0 15px 0',
                        'fontSize': '18px',
                        'fontWeight': '600',
                        'color': '#2c3e50',
                        'textAlign': 'center'
                    }),
                    dcc.Graph(
                        id='india-map',
                        style={'height': '45vh', 'width': '100%'},
                        config={
                            'displayModeBar': True,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'autoScale2d', 'resetScale2d'],
                            'displaylogo': False,
                            'toImageButtonOptions': {
                                'format': 'png',
                                'filename': 'india_map',
                                'height': 500,
                                'width': 700,
                                'scale': 1
                            }
                        }
                    )
                ])
            ], style={**CARD_STYLE, 'width': '31%', 'display': 'inline-block', 'marginRight': '1%'}),
            
            # Arrow Connector (conditionally visible)
            html.Div([
                html.Div(id='map-arrow', children=[
                    html.Div("�️", style={
                        'fontSize': '20px',
                        'textAlign': 'center',
                        'marginBottom': '8px',
                        'color': '#3498db'
                    }),
                    html.Div("↓", style={
                        'fontSize': '24px',
                        'textAlign': 'center',
                        'color': '#e74c3c',
                        'fontWeight': 'bold',
                        'marginBottom': '5px'
                    }),
                    html.Div("→", style={
                        'fontSize': '28px',
                        'textAlign': 'center',
                        'color': '#e74c3c',
                        'fontWeight': 'bold',
                        'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'
                    }),
                    html.Div("↓", style={
                        'fontSize': '24px',
                        'textAlign': 'center',
                        'color': '#e74c3c',
                        'fontWeight': 'bold',
                        'marginTop': '5px'
                    }),
                    html.Div("📍", style={
                        'fontSize': '20px',
                        'textAlign': 'center',
                        'marginTop': '8px',
                        'color': '#27ae60'
                    })
                ], style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'height': '100%',
                    'backgroundColor': 'rgba(52, 152, 219, 0.15)',
                    'borderRadius': '12px',
                    'border': '2px dashed #3498db',
                    'boxShadow': 'inset 0 2px 4px rgba(0,0,0,0.1)'
                })
            ], style={'width': '3%', 'display': 'inline-block', 'marginRight': '1%', 'height': '45vh'}),
            
            # District Map (New)
            html.Div([
                html.Div([
                    html.H3(id='district-map-title', children="📍 Select a State", style={
                        'margin': '0 0 15px 0',
                        'fontSize': '18px',
                        'fontWeight': '600',
                        'color': '#7f8c8d',
                        'textAlign': 'center'
                    }),
                    dcc.Graph(
                        id='district-detail-map',
                        style={'height': '45vh', 'width': '100%'},
                        config={
                            'displayModeBar': True,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'autoScale2d', 'resetScale2d'],
                            'displaylogo': False
                        }
                    )
                ])
            ], style={**CARD_STYLE, 'width': '31%', 'display': 'inline-block', 'marginRight': '1%'}),
            
            # Category Analysis (Bar Chart) - Smaller
            html.Div([
                html.Div([
                    html.H3("📈 Category Analysis", style={
                        'margin': '0 0 15px 0',
                        'fontSize': '18px',
                        'fontWeight': '600',
                        'color': '#2c3e50',
                        'textAlign': 'center'
                    }),
                    dcc.Graph(
                        id='district-bar',
                        style={'height': '45vh', 'width': '100%'},
                        config={
                            'displayModeBar': False
                        }
                    )
                ])
            ], style={**CARD_STYLE, 'width': '31%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px'}),
        
        # Middle Row: Box Plot + District Map + Pie Charts
        html.Div([
            # Box Plot
            html.Div([
                html.H4("📊 Statistical Summary", style={
                    'margin': '0 0 10px 0',
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'color': '#2c3e50',
                    'textAlign': 'center'
                }),
                dcc.Graph(id='box-whisker', style={'height': '35vh'})
            ], style={**CARD_STYLE, 'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),
            
            # District Map (Larger)
            html.Div([
                html.H4("🎯 District Performance", style={
                    'margin': '0 0 10px 0',
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'color': '#2c3e50',
                    'textAlign': 'center'
                }),
                dcc.Graph(id='state-district-map', style={'height': '35vh'},
                         config={
                             'displayModeBar': True,
                             'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'autoScale2d', 'resetScale2d'],
                             'displaylogo': False
                         }),
                # Legend for district map
                html.Div([
                    html.Div([
                        html.Span("🟢", style={'fontSize': '14px', 'marginRight': '5px'}),
                        html.Span("Top 5 Districts", style={'fontSize': '12px', 'marginRight': '15px'})
                    ], style={'display': 'inline-block'}),
                    html.Div([
                        html.Span("🔴", style={'fontSize': '14px', 'marginRight': '5px'}),
                        html.Span("Bottom 5 Districts", style={'fontSize': '12px', 'marginRight': '15px'})
                    ], style={'display': 'inline-block'}),
                    html.Div([
                        html.Span("🔵", style={'fontSize': '14px', 'marginRight': '5px'}),
                        html.Span("Other Districts", style={'fontSize': '12px'})
                    ], style={'display': 'inline-block'})
                ], style={'textAlign': 'center', 'marginTop': '8px', 'fontSize': '12px', 'color': '#666'})
            ], style={**CARD_STYLE, 'width': '36%', 'display': 'inline-block', 'marginRight': '2%'}),
            
            # Pie Charts
            html.Div([
                html.H4("🥧 Top & Bottom", style={
                    'margin': '0 0 10px 0',
                    'fontSize': '16px',
                    'fontWeight': '600',
                    'color': '#2c3e50',
                    'textAlign': 'center'
                }),
                html.Div([
                    dcc.Graph(id='top5-pie', style={'height': '16vh', 'marginBottom': '5px'}),
                    dcc.Graph(id='bottom5-pie', style={'height': '16vh'})
                ])
            ], style={**CARD_STYLE, 'width': '30%', 'display': 'inline-block'})
        ], style={'marginBottom': '20px'}),
        
        # Bottom Row: Correlation Analysis
        html.Div([
            html.H3("🔗 Correlation Analysis", style={
                'margin': '0 0 15px 0',
                'fontSize': '18px',
                'fontWeight': '600',
                'color': '#2c3e50',
                'textAlign': 'center'
            }),
            dcc.Graph(id='correlation-scatter', style={'height': '40vh', 'marginBottom': '15px'}),
            
            # Correlation Indicator
            html.Div([
                html.Span(id='correlation-indicator', style={
                    'display': 'inline-block',
                    'width': '20px',
                    'height': '20px',
                    'borderRadius': '50%',
                    'marginRight': '12px',
                    'verticalAlign': 'middle'
                }),
                html.Span(id='correlation-indicator-label', style={
                    'fontWeight': '700',
                    'fontSize': '14px',
                    'verticalAlign': 'middle',
                    'marginRight': '12px'
                }),
                html.Span(id='correlation-description', style={
                    'fontSize': '13px',
                    'color': '#636e72',
                    'backgroundColor': '#f8f9fa',
                    'borderRadius': '8px',
                    'padding': '10px 16px',
                    'display': 'inline-block'
                })
            ], style={'textAlign': 'center', 'padding': '10px'})
        ], style=CARD_STYLE)
        
    ], style=MAIN_CONTENT_STYLE)
], style={
    'fontFamily': '"Inter", sans-serif',
    'backgroundColor': '#ecf0f1',
    'margin': '0',
    'padding': '0'
})

# =========================
# All Callbacks (copied from original with same logic)
# =========================

@app.callback(
    Output("india-map", "figure"),
    [Input("india-map", "id"), Input("state-selector", "value")]
)
def draw_india_map(_, selected_state):
    locations = []
    pops = []
    selected_color = '#b10026'
    faded_color = '#e6f4ea'
    
    for f in india_geo['features']:
        props = f.get('properties', {})
        state = props.get('st_nm') or props.get('name')
        if state:
            key = state.lower().replace(" ", "_").replace("-", "_")
            locations.append(state)
            pops.append(population_data.get(key, 0))

    if selected_state:
        color_vals = [selected_color if (key.lower().replace(" ", "_").replace("-", "_") == selected_state) else faded_color for key in locations]
        fig = px.choropleth_mapbox(
            geojson=india_geo,
            locations=locations,
            featureidkey="properties.st_nm" if 'st_nm' in india_geo['features'][0]['properties'] else "properties.name",
            color=[1 if (key.lower().replace(" ", "_").replace("-", "_") == selected_state) else 0 for key in locations],
            color_continuous_scale=[faded_color, selected_color],
            range_color=(0, 1),
            mapbox_style="white-bg",
            center={"lat": 20.0, "lon": 77.0},
            zoom=4.3,
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
            center={"lat": 20.0, "lon": 77.0},
            zoom=4.3,
            opacity=1.0
        )
    
    fig.update_traces(hovertemplate="%{location}<extra></extra>")
    fig.update_layout(
        clickmode='event+select',
        margin={"r":5,"t":5,"l":5,"b":5},
        paper_bgcolor='white',
        plot_bgcolor='white',
        autosize=True,
        height=None,
        coloraxis_colorbar=dict(
            title="Population" if not selected_state else "Selected",
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=0.01,
            thickness=8,
            len=0.4
        )
    )
    return fig

@app.callback(
    Output('district-bar', 'figure'),
    [Input('state-selector', 'value'), Input('attribute-category-dropdown', 'value')]
)
def update_district_bar(selected_state, selected_category):
    if not selected_state or not selected_category:
        return go.Figure()
    
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
    
    y_vals = list(bar_data.values())
    x_labels = [short_label(cat) for cat in bar_data.keys()]
    
    colors = MODERN_COLORS['gradient'][:len(x_labels)] if len(x_labels) > 1 else [MODERN_COLORS['primary']]
    
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=y_vals,
        marker=dict(color=colors, opacity=0.9),
        text=[f'{v:.1f}' for v in y_vals],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f"{selected_category} in {state_name}",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=PLOTLY_FONT,
        margin=dict(l=40, r=20, t=60, b=40)
    )
    return fig

@app.callback(
    Output('subcategory-dropdown', 'options'),
    [Input('attribute-category-dropdown', 'value')]
)
def update_subcategory_options(selected_category):
    if not selected_category:
        return []
    subcats = ATTRIBUTE_MAP.get(selected_category, [])
    return [{"label": short_label(c), "value": c} for c in subcats]

@app.callback(
    Output('correlation-subcategory-dropdown', 'options'),
    [Input('correlation-attribute-dropdown', 'value')]
)
def update_correlation_subcategory_options(selected_corr_category):
    if not selected_corr_category:
        return []
    subcats = ATTRIBUTE_MAP.get(selected_corr_category, [])
    return [{"label": short_label(c), "value": c} for c in subcats]

@app.callback(
    Output('box-whisker', 'figure'),
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_box_whisker(selected_state, selected_subcat):
    if not selected_state or not selected_subcat:
        return go.Figure()
    
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
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        if col not in df_state.columns:
            return go.Figure()
            
        df_state = df_state[['District name', col]].dropna()
        
        fig = go.Figure(go.Box(
            y=df_state[col],
            boxpoints='all',
            name='Districts',
            marker_color=MODERN_COLORS['primary']
        ))
        
        fig.update_layout(
            title=f"{short_label(selected_subcat)} Distribution",
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=40, r=20, t=50, b=30)
        )
        return fig
    except:
        return go.Figure()

@app.callback(
    Output('top5-pie', 'figure'),
    Output('bottom5-pie', 'figure'),
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_pie_charts(selected_state, selected_subcat):
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
            
        df_state = df_state[['District name', col]].dropna().sort_values(by=col, ascending=False)
        top5 = df_state.head(5)
        bottom5 = df_state.tail(5)
        
        top_fig = go.Figure(go.Pie(
            labels=top5['District name'],
            values=top5[col],
            hole=0.3,
            marker_colors=['#00b894', '#00cec9', '#6c5ce7', '#74b9ff', '#fd79a8']
        ))
        top_fig.update_layout(
            title='Top 5',
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False,
            font=PLOTLY_FONT
        )
        
        bottom_fig = go.Figure(go.Pie(
            labels=bottom5['District name'],
            values=bottom5[col],
            hole=0.3,
            marker_colors=['#e17055', '#d63031', '#e84393', '#fdcb6e', '#fd79a8']
        ))
        bottom_fig.update_layout(
            title='Bottom 5',
            margin=dict(l=10, r=10, t=30, b=10),
            showlegend=False,
            font=PLOTLY_FONT
        )
        
        return top_fig, bottom_fig
    except:
        return go.Figure(), go.Figure()

@app.callback(
    Output('state-district-map', 'figure'),
    [Input('state-selector', 'value'), Input('subcategory-dropdown', 'value')]
)
def update_state_district_map(selected_state, selected_subcat):
    if not selected_state or not selected_subcat:
        # Create informative placeholder when no selection
        fig = go.Figure()
        fig.add_annotation(
            text="📍 Select a state and subcategory<br>to view district-wise analysis<br><br>🎯 This map will show:<br>• Top 5 districts (Green)<br>• Bottom 5 districts (Red)<br>• Other districts (Blue)",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=12, color="#666"),
            align="center"
        )
        fig.update_layout(
            title="🗺️ District Performance Map",
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    try:
        # Load data first
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            return create_error_figure("State not found", selected_state)
            
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        if col not in df_state.columns:
            return create_error_figure("Data not available", selected_subcat)
            
        # Prepare district values and rankings
        df_state = df_state[['District name', col]].dropna()
        df_state = df_state.sort_values(by=col, ascending=False)
        
        if len(df_state) == 0:
            return create_error_figure("No data available", f"{selected_subcat} in {state_name}")
        
        # Create a bar chart as fallback if map fails
        top5 = df_state.head(5)
        bottom5 = df_state.tail(5)
        
        # Try to load and display the map
        filename = state_file_map.get(selected_state)
        if filename:
            try:
                with open(filename, encoding="utf-8") as f:
                    state_geo = json.load(f)
                return create_district_map(state_geo, df_state, col, state_name, selected_subcat)
            except Exception as map_error:
                print(f"Map loading failed: {map_error}")
                # Fallback to district performance chart
                return create_district_chart(df_state, col, state_name, selected_subcat)
        else:
            # No map file available, show chart
            return create_district_chart(df_state, col, state_name, selected_subcat)
            
    except Exception as e:
        print(f"District map error: {e}")
        return create_error_figure("Error loading data", str(e))

def create_error_figure(title, detail):
    """Create a standardized error figure with informative message"""
    fig = go.Figure()
    fig.add_annotation(
        text=f"⚠️ {title}<br><br>📊 {detail}<br><br>💡 Available analysis:<br>• Statistical summary (left)<br>• Top/Bottom charts (right)<br>• Correlation analysis (bottom)",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=11, color="#666"),
        align="center"
    )
    fig.update_layout(
        title="🗺️ District Analysis",
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        font=PLOTLY_FONT,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig

def create_district_chart(df_state, col, state_name, selected_subcat):
    """Create a horizontal bar chart showing district performance"""
    # Show top 10 and bottom 5 districts
    top10 = df_state.head(10)
    bottom5 = df_state.tail(5)
    display_data = pd.concat([top10, bottom5]).drop_duplicates()
    
    # Create colors: green for top 5, red for bottom 5, blue for others
    colors = []
    for i, district in enumerate(display_data['District name']):
        if i < 5:  # Top 5
            colors.append('#43aa8b')
        elif i >= len(display_data) - 5:  # Bottom 5
            colors.append('#f94144')
        else:  # Middle
            colors.append('#277da1')
    
    fig = go.Figure(go.Bar(
        y=display_data['District name'],
        x=display_data[col],
        orientation='h',
        marker=dict(color=colors),
        text=display_data[col].round(1),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Value: %{x:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"🏆 District Performance: {short_label(selected_subcat)} in {state_name}",
        xaxis_title=f"{short_label(selected_subcat)} Value",
        yaxis_title="Districts",
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=PLOTLY_FONT,
        margin=dict(l=150, r=20, t=50, b=20),
        height=350,
        yaxis=dict(autorange="reversed")  # Show highest at top
    )
    
    return fig

def create_district_map(state_geo, df_state, col, state_name, selected_subcat):
    """Create the actual district map visualization"""
    # Get top and bottom performers
    top5 = set(df_state.head(5)['District name'])
    bottom5 = set(df_state.tail(5)['District name'])
    
    # Color mapping for districts
    color_map = {}
    for d in df_state['District name']:
        if d in top5:
            color_map[d] = '#43aa8b'  # green for top performers
        elif d in bottom5:
            color_map[d] = '#f94144'  # red for bottom performers  
        else:
            color_map[d] = '#277da1'  # blue for middle performers
    
    # Calculate map center
    all_coords = []
    for feature in state_geo['features']:
        geom = feature['geometry']
        if geom['type'] == 'Polygon':
            all_coords.extend(geom['coordinates'][0])
        elif geom['type'] == 'MultiPolygon':
            for polygon in geom['coordinates']:
                all_coords.extend(polygon[0])
    
    if all_coords:
        lats = [c[1] for c in all_coords]
        lons = [c[0] for c in all_coords]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
    else:
        center_lat, center_lon = 23, 80
    
    # Create map with district polygons
    fig = go.Figure()
    
    for feature in state_geo['features']:
        props = feature.get('properties', {})
        district = props.get('district') or props.get('DISTRICT') or props.get('District') or props.get('NAME')
        
        if not district:
            continue
            
        # Find matching district in data
        district_value = None
        for _, row in df_state.iterrows():
            if district.lower() in row['District name'].lower() or row['District name'].lower() in district.lower():
                district_value = row[col]
                break
        
        color = color_map.get(district, '#cccccc')
        
        geom = feature['geometry']
        if geom['type'] == 'Polygon':
            for coords in geom['coordinates']:
                lons, lats = zip(*coords)
                hover_text = f"<b>{district}</b><br>{short_label(selected_subcat)}: {district_value:.2f if district_value is not None else 'N/A'}"
                fig.add_trace(go.Scattermapbox(
                    lon=lons, lat=lats,
                    mode='lines',
                    fill='toself',
                    fillcolor=color,
                    line=dict(width=1, color='white'),
                    opacity=0.7,
                    hovertemplate=hover_text + "<extra></extra>",
                    showlegend=False
                ))
        elif geom['type'] == 'MultiPolygon':
            for polygon in geom['coordinates']:
                for coords in polygon:
                    lons, lats = zip(*coords)
                    hover_text = f"<b>{district}</b><br>{short_label(selected_subcat)}: {district_value:.2f if district_value is not None else 'N/A'}"
                    fig.add_trace(go.Scattermapbox(
                        lon=lons, lat=lats,
                        mode='lines',
                        fill='toself',
                        fillcolor=color,
                        line=dict(width=1, color='white'),
                        opacity=0.7,
                        hovertemplate=hover_text + "<extra></extra>",
                        showlegend=False
                    ))
    
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=6.2,
        mapbox_center={"lat": center_lat, "lon": center_lon},
        margin={"r":5,"t":25,"l":5,"b":5},
        paper_bgcolor='white',
        font=PLOTLY_FONT,
        title=f"🗺️ {state_name} - {short_label(selected_subcat)}",
        height=280,
        autosize=True
    )
    return fig

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
def update_correlation_scatter(selected_state, selected_subcat, correlation_attr_cat, correlation_subcat):
    if not selected_state or not selected_subcat or not correlation_attr_cat or not correlation_subcat:
        indicator_style = {'backgroundColor': '#f8d7da', 'display': 'inline-block', 'width': '20px', 'height': '20px', 'borderRadius': '50%'}
        return go.Figure(), indicator_style, "No Data", "Select all parameters to see correlation analysis."
    
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            indicator_style = {'backgroundColor': '#f8d7da', 'display': 'inline-block', 'width': '20px', 'height': '20px', 'borderRadius': '50%'}
            return go.Figure(), indicator_style, "No Data", "State not found."
            
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        x_col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        y_col = correlation_subcat + '_pct' if (correlation_subcat + '_pct') in df_state.columns else correlation_subcat
        
        if x_col not in df_state.columns or y_col not in df_state.columns:
            indicator_style = {'backgroundColor': '#f8d7da', 'display': 'inline-block', 'width': '20px', 'height': '20px', 'borderRadius': '50%'}
            return go.Figure(), indicator_style, "No Data", "Data not available."
            
        df_state = df_state[['District name', x_col, y_col]].dropna()
        
        if len(df_state) < 2:
            corr_val = None
        else:
            corr_val = np.corrcoef(df_state[x_col], df_state[y_col])[0, 1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_state[x_col],
            y=df_state[y_col],
            mode='markers',
            marker=dict(size=10, color=MODERN_COLORS['primary'], opacity=0.7),
            text=df_state['District name'],
            hovertemplate='%{text}<br>X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Correlation: {short_label(selected_subcat)} vs {short_label(correlation_subcat)}",
            xaxis_title=short_label(selected_subcat),
            yaxis_title=short_label(correlation_subcat),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=40, r=20, t=60, b=40)
        )
        
        if corr_val is not None:
            abs_r = abs(corr_val)
            if abs_r < 0.3:
                color, label = '#dc3545', 'Weak'
            elif abs_r > 0.7:
                color, label = '#28a745', 'Strong'
            else:
                color, label = '#ffc107', 'Moderate'
            
            indicator_style = {
                'backgroundColor': color,
                'display': 'inline-block',
                'width': '20px',
                'height': '20px',
                'borderRadius': '50%'
            }
            description = f"Correlation coefficient: {corr_val:.3f}. This indicates a {label.lower()} relationship between the two variables."
        else:
            indicator_style = {'backgroundColor': '#6c757d', 'display': 'inline-block', 'width': '20px', 'height': '20px', 'borderRadius': '50%'}
            label = "No Data"
            description = "Insufficient data for correlation analysis."
        
        return fig, indicator_style, label, description
    except:
        indicator_style = {'backgroundColor': '#f8d7da', 'display': 'inline-block', 'width': '20px', 'height': '20px', 'borderRadius': '50%'}
        return go.Figure(), indicator_style, "Error", "Error in correlation analysis."

# Callback for district detail map
@app.callback(
    [Output("district-detail-map", "figure"), Output("district-map-title", "children")],
    [Input("state-selector", "value"), Input("subcategory-dropdown", "value")]
)
def update_district_detail_map(selected_state, selected_subcat):
    try:
        if not selected_state or not selected_subcat:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text="🗺️ Select a state and category to view district map",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color="#7f8c8d"),
                bgcolor="rgba(248, 249, 250, 0.8)",
                bordercolor="#dee2e6",
                borderwidth=2
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, "📍 Select a State"

        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"❌ State mapping not found for {selected_state.replace('_', ' ').title()}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {selected_state.replace('_', ' ').title()}"
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        if df_state.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"📊 No data available for {state_name}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
        col_name = f"{selected_subcat}_pct" if f"{selected_subcat}_pct" in df_state.columns else selected_subcat
        if col_name not in df_state.columns:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"📈 Data not available for {selected_subcat}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
        df_clean = df_state[['District name', col_name]].dropna()
        if df_clean.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"📊 No valid data for {selected_subcat} in {state_name}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
        try:
            state_file = state_file_map.get(selected_state)
            if state_file:
                with open(state_file, encoding="utf-8") as f:
                    state_geo = json.load(f)
                possible_keys = ["DISTRICT", "District", "district", "NAME", "Name", "name"]
                feature_key = None
                for key in possible_keys:
                    if state_geo['features'] and key in state_geo['features'][0].get('properties', {}):
                        feature_key = f"properties.{key}"
                        break
                if not feature_key:
                    raise Exception("No matching property key found")
                fig = go.Figure(go.Choropleth(
                    geojson=state_geo,
                    locations=df_clean['District name'],
                    z=df_clean[col_name],
                    featureidkey=feature_key,
                    colorscale="YlOrRd",
                    colorbar=dict(
                        title=short_label(selected_subcat),
                        titlefont=dict(size=10),
                        thickness=12,
                        len=0.6,
                        x=1.02
                    ),
                    text=df_clean['District name'],
                    hovertemplate='<b>%{text}</b><br>' + short_label(selected_subcat) + ': %{z:.2f}<extra></extra>'
                ))
                fig.update_geos(
                    fitbounds="locations",
                    visible=False,
                    bgcolor='rgba(0,0,0,0)'
                )
                fig.update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        projection_type='mercator'
                    ),
                    margin=dict(l=5, r=5, t=5, b=5),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=PLOTLY_FONT,
                    height=350
                )
                return fig, f"📍 {state_name} Districts"
            else:
                raise Exception("GeoJSON file not found for selected state.")
                feature_key = None
                for key in possible_keys:
                    if state_geo['features'] and key in state_geo['features'][0].get('properties', {}):
                        feature_key = f"properties.{key}"
                        break
                if not feature_key:
                    raise Exception("No matching property key found in geojson for district names.")
                # Build the choropleth map
                fig = go.Figure(go.Choropleth(
                    geojson=state_geo,
                    locations=df_clean['District name'],
                    z=df_clean[col_name],
                    featureidkey=feature_key,
                    colorscale="YlOrRd",
                    colorbar=dict(
                        title=short_label(selected_subcat),
                        titlefont=dict(size=10),
                        thickness=12,
                        len=0.6,
                        x=1.02
                    ),
                    text=df_clean['District name'],
                    hovertemplate='<b>%{text}</b><br>' + short_label(selected_subcat) + ': %{z:.2f}<extra></extra>'
                ))
                fig.update_geos(
                    fitbounds="locations",
                    visible=False,
                    bgcolor='rgba(0,0,0,0)'
                )
                fig.update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        projection_type='mercator'
                    ),
                    margin=dict(l=5, r=5, t=5, b=5),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=PLOTLY_FONT,
                    height=350
                )
                return fig, f"📍 {state_name} Districts"
            else:
                raise Exception("GeoJSON file not found for selected state.")
        except Exception as map_error:
            print(f"Map creation failed: {map_error}")
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"⚠️ Error loading district map<br>Details: {str(map_error)[:50]}...",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=12, color="#e74c3c"),
                bgcolor="rgba(248, 215, 218, 0.8)",
                bordercolor="#f5c6cb",
                borderwidth=2
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"� {state_name}"
    except Exception as e:
        print(f"District detail map error: {e}")
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text=f"⚠️ Error loading district map<br>Details: {str(e)[:50]}...",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=12, color="#e74c3c"),
            bgcolor="rgba(248, 215, 218, 0.8)",
            bordercolor="#f5c6cb",
            borderwidth=2
        )
        empty_fig.update_layout(
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=10, r=10, t=10, b=10)
    try:
        if not selected_state or not selected_subcat:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text="�️ Select a state and category to view district map",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16, color="#7f8c8d"),
                bgcolor="rgba(248, 249, 250, 0.8)",
                bordercolor="#dee2e6",
                borderwidth=2
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, "📍 Select a State"

        df = pd.read_csv('districtwise_data_percentages.csv')
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"❌ State mapping not found for {selected_state.replace('_', ' ').title()}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {selected_state.replace('_', ' ').title()}"
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        if df_state.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"📊 No data available for {state_name}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
        col_name = f"{selected_subcat}_pct" if f"{selected_subcat}_pct" in df_state.columns else selected_subcat
        if col_name not in df_state.columns:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"📈 Data not available for {selected_subcat}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
        df_clean = df_state[['District name', col_name]].dropna()
        if df_clean.empty:
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"📊 No valid data for {selected_subcat} in {state_name}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=14, color="#e74c3c")
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
        try:
            state_file = state_file_map.get(selected_state)
            if state_file:
                with open(state_file, encoding="utf-8") as f:
                    state_geo = json.load(f)
                # Try to find the correct feature key for district names
                possible_keys = ["DISTRICT", "District", "district", "NAME", "Name", "name"]
                feature_key = None
                for key in possible_keys:
                    if state_geo['features'] and key in state_geo['features'][0].get('properties', {}):
                        feature_key = f"properties.{key}"
                        break
                if not feature_key:
                    raise Exception("No matching property key found in geojson for district names.")
                # Build the choropleth map
                fig = go.Figure(go.Choropleth(
                    geojson=state_geo,
                    locations=df_clean['District name'],
                    z=df_clean[col_name],
                    featureidkey=feature_key,
                    colorscale="YlOrRd",
                    colorbar=dict(
                        title=short_label(selected_subcat),
                        titlefont=dict(size=10),
                        thickness=12,
                        len=0.6,
                        x=1.02
                    ),
                    text=df_clean['District name'],
                    hovertemplate='<b>%{text}</b><br>' + short_label(selected_subcat) + ': %{z:.2f}<extra></extra>'
                ))
                fig.update_geos(
                    fitbounds="locations",
                    visible=False,
                    bgcolor='rgba(0,0,0,0)'
                )
                fig.update_layout(
                    geo=dict(
                        showframe=False,
                        showcoastlines=False,
                        projection_type='mercator'
                    ),
                    margin=dict(l=5, r=5, t=5, b=5),
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=PLOTLY_FONT,
                    height=350
                )
                return fig, f"📍 {state_name} Districts"
            else:
                raise Exception("GeoJSON file not found for selected state.")
        except Exception as map_error:
            print(f"Map creation failed: {map_error}")
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text=f"⚠️ Error loading district map<br>Details: {str(map_error)[:50]}...",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=12, color="#e74c3c"),
                bgcolor="rgba(248, 215, 218, 0.8)",
                bordercolor="#f5c6cb",
                borderwidth=2
            )
            empty_fig.update_layout(
                plot_bgcolor='#f8f9fa',
                paper_bgcolor='white',
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                margin=dict(l=10, r=10, t=10, b=10)
            )
            return empty_fig, f"📍 {state_name}"
    except Exception as e:
        print(f"District detail map error: {e}")
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text=f"⚠️ Error loading district map<br>Details: {str(e)[:50]}...",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False,
            font=dict(size=12, color="#e74c3c"),
            bgcolor="rgba(248, 215, 218, 0.8)",
            bordercolor="#f5c6cb",
            borderwidth=2
        )
        empty_fig.update_layout(
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            margin=dict(l=10, r=10, t=10, b=10)
        )
        return empty_fig, "📍 Error Loading Map"
