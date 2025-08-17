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
app.title = "India State Drilldown"

# Define the overall layout of the dashboard
# Left panel: India map and selectors
# Right panel: All district/statewise charts, correlation, and pie charts
app.layout = html.Div([
    # --- Left Panel: India Map and Selectors ---
    html.Div([
        html.Div([
            # State selector dropdown (with 'None' option to clear selection)
            dcc.Dropdown(
                id='state-selector',
                options=[{"label": "None", "value": ""}] + state_dropdown_options,
                value="",
                placeholder="Select a state",
                style={
                    "margin": "5px 10px 5px 0",
                    "fontSize": "14px",
                    "height": "35px",
                    "width": "300px",
                    "display": "inline-block",
                    "verticalAlign": "top"
                }
            ),
            # Attribute category dropdown (main attribute selection)
            dcc.Dropdown(
                id='attribute-category-dropdown',
                options=[{"label": k, "value": k} for k in ATTRIBUTE_MAP.keys()],
                placeholder="Select Attribute Category",
                style={
                    "width": "260px",
                    "margin": "5px 10px",
                    "fontSize": "14px",
                    "height": "35px",
                    "display": "inline-block",
                    "verticalAlign": "top"
                }
            )
        ], style={"display": "flex", "flexDirection": "row", "alignItems": "center", "marginBottom": "10px"}),
        # Main India map (always visible)
        dcc.Graph(id='india-map', style={'height': '85vh', 'width': '100%', 'margin-left': '0px'})
    ], style={'width': '50%', 'height': '100vh', 'display': 'inline-block', 'backgroundColor': 'white', 'padding-left': '10px', 'position': 'relative'}),

    # --- Right Panel: District/Statewise Analysis and Correlation ---
    html.Div([
        # Bar chart for subcategory breakdown
        dcc.Graph(id='district-bar', config={'displayModeBar': False}, style={'height': '32vh', 'width': '100%', 'padding': '0', 'margin': '0'}),
        # Subcategory dropdown (populated based on attribute category)
        dcc.Dropdown(
            id='subcategory-dropdown',
            placeholder="Select Subcategory",
            style={
                'width': '100%',
                'marginTop': '6px',
                'fontSize': '13px',
                'height': '32px',
                'backgroundColor': 'white',
            }
        ),
        # Box-whisker and state-district map side by side
        html.Div([
            # Box-whisker plot (distribution of selected subcategory across districts)
            dcc.Graph(id='box-whisker', style={
                'height': '28vh',
                'width': '48%',
                'display': 'inline-block',
                'marginRight': '2%',
                'verticalAlign': 'top',
                'backgroundColor': 'white',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.07)',
                'borderRadius': '8px',
                'padding': '0',
            }),
            # State district map (top/bottom 5 districts highlighted)
            dcc.Graph(id='state-district-map', style={
                'height': '28vh',
                'width': '48%',
                'display': 'inline-block',
                'verticalAlign': 'top',
                'backgroundColor': 'white',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.07)',
                'borderRadius': '8px',
                'padding': '0',
            })
        ], style={'width': '100%', 'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'marginTop': '10px'}),
        # --- Correlation Box and Pie Charts Row ---
        html.Div([
            # Correlation box (dropdown to select second attribute for correlation)
            html.Div([
                html.Div("Correlation", style={
                    'fontWeight': 'bold',
                    'fontSize': '15px',
                    'marginBottom': '6px',
                    'color': '#277da1',
                    'letterSpacing': '0.5px',
                    'paddingLeft': '2px',
                }),
                dcc.Dropdown(
                    id='correlation-attribute-dropdown',
                    options=[{"label": k, "value": k} for k in ATTRIBUTE_MAP.keys()],
                    placeholder="Select Attribute for Correlation",
                    style={
                        'width': '100%',
                        'fontSize': '13px',
                        'height': '32px',
                        'backgroundColor': 'white',
                        'marginBottom': '0',
                    }
                )
            ], style={
                'width': '28%',
                'backgroundColor': '#f8f9fa',
                'borderRadius': '8px',
                'boxShadow': '0 1px 4px rgba(0,0,0,0.06)',
                'padding': '10px 8px 8px 8px',
                'marginTop': '10px',
                'marginBottom': '0',
                'border': '1px solid #e0e0e0',
                'display': 'inline-block',
                'verticalAlign': 'top',
            }),
            # Pie charts for top 5 and bottom 5 districts (right)
            html.Div([
                dcc.Graph(id='top5-pie', style={'display': 'inline-block', 'width': '48%', 'height': '24vh', 'verticalAlign': 'top', 'marginRight': '2%'}),
                dcc.Graph(id='bottom5-pie', style={'display': 'inline-block', 'width': '48%', 'height': '24vh', 'verticalAlign': 'top'})
            ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '2%'})
        ], style={'width': '100%', 'marginTop': '10px', 'textAlign': 'center', 'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}),
        # --- Correlation Scatter Plot Row ---
        html.Div([
            # Correlation indicator and description (above scatter plot)
            html.Div([
                html.Span(id='correlation-indicator', style={
                    'display': 'inline-block',
                    'width': '18px',
                    'height': '18px',
                    'borderRadius': '4px',
                    'marginRight': '10px',
                    'verticalAlign': 'middle',
                    'border': '1.5px solid #bbb',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.07)'
                }),
                html.Span(id='correlation-indicator-label', style={
                    'fontWeight': 'bold',
                    'fontSize': '13px',
                    'verticalAlign': 'middle',
                    'marginRight': '12px',
                }),
                html.Span(id='correlation-description', style={
                    'fontSize': '13px',
                    'color': '#444',
                    'backgroundColor': '#f8f9fa',
                    'borderRadius': '6px',
                    'padding': '8px 10px',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.04)',
                    'minHeight': '38px',
                    'textAlign': 'left',
                    'display': 'inline-block',
                    'width': 'calc(100% - 120px)'
                })
            ], style={
                'marginBottom': '16px',
                'marginTop': '16px',
                'display': 'flex',
                'flexDirection': 'row',
                'alignItems': 'center',
                'width': '100%'
            }),
            # Correlation scatter plot (relationship between two attributes for all districts)
            dcc.Graph(id='correlation-scatter', style={'height': '28vh', 'width': '100%', 'marginTop': '0', 'backgroundColor': 'white', 'boxShadow': '0 2px 8px rgba(0,0,0,0.07)', 'borderRadius': '8px'})
        ], style={'width': '100%', 'marginTop': '0', 'marginBottom': '32px', 'padding': '0'})
    ], style={
        'width': '35%',  # widened from 23% to 35%
        'height': 'auto',
        'display': 'inline-block',
        'verticalAlign': 'top',
        'backgroundColor': 'white',
        'margin': '1vh 1vw 0 0',
        'position': 'absolute',
        'top': '0',
        'right': '0',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.07)',
        'borderRadius': '8px',
        'padding': '0.5vh 0.5vw'
    }),

    # --- Hidden District Map Container (not used in main UI) ---
    html.Div([
        dcc.Graph(id='district-map', style={'height': '100%', 'width': '100%'})
    ], id='district-map-container', style={
        'width': '25%',
        'height': '50vh',
        'display': 'none',  # hidden by default
        'backgroundColor': 'white',
        'position': 'absolute',
        'top': '34vh',
        'right': '0',
        'padding': '1vh',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.07)',
        'borderRadius': '8px'
    }),

    # Remove the old box-whisker left panel
], style={'backgroundColor': 'white', 'position': 'relative'})

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
    outlines = []
    custom_colors = []
    for f in india_geo['features']:
        props = f.get('properties', {})
        state = props.get('st_nm') or props.get('name')
        if state:
            key = state.lower().replace(" ", "_").replace("-", "_")
            locations.append(state)
            pops.append(population_data.get(key, 0))
            if selected_state and key == selected_state:
                outlines.append('black')
                custom_colors.append(population_data.get(key, 0))  # Use real value for selected
            else:
                outlines.append('#888')
                custom_colors.append(None)  # Mark as faded

    # If a state is selected, set all other states to transparent/faded
    if selected_state:
        # Color non-selected states with very light green, selected state with population color
        max_pop = max(pops) if pops else 1
        color_vals = []
        for i, state in enumerate(locations):
            key = state.lower().replace(" ", "_").replace("-", "_")
            if key == selected_state:
                color_vals.append(pops[i])
            else:
                color_vals.append(0)
        # Custom color scale: 0 (light green), min_pop (light green), max_pop (YlOrRd)
        custom_scale = [
            [0.0, '#e6f4ea'],
            [0.00001, '#e6f4ea'],
            [0.00002, px.colors.sequential.YlOrRd[0]],
            [1.0, px.colors.sequential.YlOrRd[-1]]
        ]
        fig = px.choropleth_mapbox(
            geojson=india_geo,
            locations=locations,
            featureidkey="properties.st_nm" if 'st_nm' in india_geo['features'][0]['properties'] else "properties.name",
            color=color_vals,
            color_continuous_scale=custom_scale,
            range_color=(0, max_pop),
            mapbox_style="white-bg",
            center={"lat": 22.9734, "lon": 78.6569},
            zoom=3.8,
            opacity=1.0,
            labels={'color': 'Population'}
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
            center={"lat": 22.9734, "lon": 78.6569},
            zoom=3.8,
            opacity=1.0,
            labels={'color': 'Population'}
        )
    fig.update_traces(
        hovertemplate="%{location}<extra></extra>"
    )
    fig.update_layout(
        clickmode='event+select',
        margin={"r":0,"t":0,"l":60,"b":0},
        paper_bgcolor='white',
        coloraxis_colorbar=dict(
            title="Population",
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=0.0,
            thickness=15,
            len=0.7
        )
    )
    # Simulate pop-out effect for selected state by drawing thick and thin outlines
    if selected_state:
        for f in india_geo['features']:
            props = f.get('properties', {})
            state = props.get('st_nm') or props.get('name')
            key = state.lower().replace(" ", "_").replace("-", "_")
            if key == selected_state:
                geom = f['geometry']
                if geom['type'] == 'Polygon':
                    for coords in geom['coordinates']:
                        lons, lats = zip(*coords)
                        lats_pop = [lat + 0.8 for lat in lats]
                        fig.add_trace(go.Scattermapbox(
                            lon=lons, lat=lats_pop,
                            mode='lines',
                            line=dict(width=12, color='rgba(0,0,0,0.25)'),
                            hoverinfo='skip',
                            showlegend=False
                        ))
                        fig.add_trace(go.Scattermapbox(
                            lon=lons, lat=lats,
                            mode='lines',
                            line=dict(width=5, color='black'),
                            hoverinfo='skip',
                            showlegend=False
                        ))
                elif geom['type'] == 'MultiPolygon':
                    for polygon in geom['coordinates']:
                        for coords in polygon:
                            lons, lats = zip(*coords)
                            lats_pop = [lat + 0.8 for lat in lats]
                            fig.add_trace(go.Scattermapbox(
                                lon=lons, lat=lats_pop,
                                mode='lines',
                                line=dict(width=12, color='rgba(0,0,0,0.25)'),
                                hoverinfo='skip',
                                showlegend=False
                            ))
                            fig.add_trace(go.Scattermapbox(
                                lon=lons, lat=lats,
                                mode='lines',
                                line=dict(width=5, color='black'),
                                hoverinfo='skip',
                                showlegend=False
                            ))

    return fig

# =========================
# Plotly Font Settings
# =========================

# Global font settings for all Plotly charts
PLOTLY_FONT = dict(family="Lato, Roboto, Arial, sans-serif", size=13, color="#222")

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
    # Gradient color palette for bars
    colors = px.colors.sequential.Plasma[:len(x_labels)] if len(x_labels) > 1 else ['#636EFA']
    fig = go.Figure(go.Bar(
        x=x_labels,
        y=y_vals,
        marker=dict(
            color=colors,
            line=dict(width=0),
        ),
        text=[f'{v:.2f}' for v in y_vals],
        textposition='inside',
        insidetextanchor='middle',
        width=0.7,
        hoverinfo='x+y',
        opacity=0.92,
    ))
    fig.update_traces(
        marker_line_width=0,
        marker_line_color='rgba(0,0,0,0)',
        marker_pattern_shape="/",
        marker_pattern_fgcolor="rgba(255,255,255,0.08)",
        marker_pattern_size=4,
        marker_pattern_solidity=0.2,
        marker=dict(
            color=colors,
            line=dict(width=0),
            opacity=0.92,
        ),
        hovertemplate="%{x}: %{y:.2f}<extra></extra>",
    )
    fig.update_layout(
        title=f"Breakdown of {selected_category} in {state_name}",
        xaxis_title="Subcategory",
        yaxis_title="Percentage" if any('_pct' in c for c in subcats_pct) else "Count",
        plot_bgcolor='#f8f9fa',
        paper_bgcolor='white',
        font=PLOTLY_FONT,
        margin=dict(l=30, r=10, t=40, b=30),
        yaxis_type='log' if use_log else 'linear',
        yaxis=dict(
            rangemode='tozero',
            showgrid=True,
            gridcolor='rgba(200,200,200,0.13)',
            zerolinecolor='#bbb',
        ),
        xaxis=dict(
            tickangle=-30,
            tickfont=dict(size=12),
            automargin=True
        ),
        bargap=0.18,
        bargroupgap=0.08,
        showlegend=False,
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
        # Box-whisker plot for district values
        fig = go.Figure(go.Box(
            y=df_state[col],
            boxpoints='all',
            jitter=0.4,
            pointpos=0,
            name='Districts',
            boxmean=True,
            marker_color='#277da1',
            line_color='#277da1',
            fillcolor='rgba(39,125,161,0.15)',
            hoverinfo='y+name',
            customdata=df_state['District name'],
            hovertemplate='<b>%{customdata}</b><br>Value: %{y:.2f}<extra></extra>',
        ))
        fig.update_layout(
            title=f"Summary for {short_label(selected_subcat)} in {state_name}",
            yaxis_title="Percentage" if '_pct' in col else "Count",
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=30, r=10, t=40, b=30),
            showlegend=False,
            height=220,
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
        pastel_greens = ['#b7e4c7', '#95d5b2', '#74c69d', '#52b788', '#40916c']
        pastel_reds = ['#f8bbd0', '#f48fb1', '#f06292', '#ec407a', '#d81b60']
        # Top 5 pie chart
        top_fig = go.Figure(go.Pie(
            labels=top5['District name'],
            values=top5[col],
            hole=0.55,
            marker=dict(colors=pastel_greens, line=dict(color='#fff', width=2)),
            textinfo='label+percent',
            pull=[0.05]*5,
        ))
        top_fig.update_layout(
            title_text='Top 5 Districts',
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=False,
            height=220,
            font=PLOTLY_FONT,
            annotations=[dict(text='Top 5', x=0.5, y=0.5, font_size=16, showarrow=False)],
            paper_bgcolor='white',
        )
        # Bottom 5 pie chart
        bottom_fig = go.Figure(go.Pie(
            labels=bottom5['District name'],
            values=bottom5[col],
            hole=0.55,
            marker=dict(colors=pastel_reds, line=dict(color='#fff', width=2)),
            textinfo='label+percent',
            pull=[0.05]*5,
        ))
        bottom_fig.update_layout(
            title_text='Bottom 5 Districts',
            margin=dict(l=10, r=10, t=40, b=10),
            showlegend=False,
            height=220,
            font=PLOTLY_FONT,
            annotations=[dict(text='Bottom 5', x=0.5, y=0.5, font_size=16, showarrow=False)],
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
            mapbox_zoom=5.2,
            mapbox_center={"lat": center_lat, "lon": center_lon},
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            hovermode='closest',
        )
        return fig
    except Exception as e:
        print("District map error:", e)
        return go.Figure()

# =========================
# Correlation Scatter Plot Callback
# =========================

@app.callback(
    [Output('correlation-scatter', 'figure'),
     Output('correlation-description', 'children')],
    [Input('state-selector', 'value'),
     Input('subcategory-dropdown', 'value'),
     Input('correlation-attribute-dropdown', 'value')]
)
def update_correlation_scatter(selected_state, selected_subcat, correlation_attr_cat):
    """
    Draws a scatter plot showing the relationship between the selected subcategory and the first subcategory
    of the selected correlation attribute for all districts in the selected state. Computes and displays
    the Pearson correlation coefficient, and provides a user-friendly description and colored indicator box.
    """
    if not selected_state or not selected_subcat or not correlation_attr_cat:
        # Show empty indicator and default description
        indicator = html.Div([
            html.Div("Unrelated", style={
                'display': 'inline-block',
                'backgroundColor': '#f8d7da',
                'color': '#c1121f',
                'borderRadius': '6px',
                'padding': '4px 12px',
                'fontWeight': 'bold',
                'fontSize': '13px',
                'marginRight': '12px',
                'border': '1.5px solid #c1121f',
                'boxShadow': '0 1px 4px rgba(0,0,0,0.04)'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
        desc = "Select a state and two attributes to see their relationship across districts."
        return go.Figure(), html.Div([
            indicator,
            html.Div(desc, style={'flex': '1'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
    try:
        df = pd.read_csv('districtwise_data_percentages.csv')
        # Get state name for lookup
        state_name = None
        for k, v in reverse_state_lookup.items():
            if v == selected_state:
                state_name = k
                break
        if not state_name:
            indicator = html.Div([
                html.Div("Unrelated", style={
                    'display': 'inline-block',
                    'backgroundColor': '#f8d7da',
                    'color': '#c1121f',
                    'borderRadius': '6px',
                    'padding': '4px 12px',
                    'fontWeight': 'bold',
                    'fontSize': '13px',
                    'marginRight': '12px',
                    'border': '1.5px solid #c1121f',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.04)'
                })
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
            desc = "No data for this state."
            return go.Figure(), html.Div([
                indicator,
                html.Div(desc, style={'flex': '1'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
        df_state = df[df['State name'].str.lower() == state_name.lower()]
        # X: selected_subcat, Y: first subcat of correlation_attr_cat
        x_col = selected_subcat + '_pct' if (selected_subcat + '_pct') in df_state.columns else selected_subcat
        corr_subcats = ATTRIBUTE_MAP.get(correlation_attr_cat, [])
        if not corr_subcats:
            indicator = html.Div([
                html.Div("Unrelated", style={
                    'display': 'inline-block',
                    'backgroundColor': '#f8d7da',
                    'color': '#c1121f',
                    'borderRadius': '6px',
                    'padding': '4px 12px',
                    'fontWeight': 'bold',
                    'fontSize': '13px',
                    'marginRight': '12px',
                    'border': '1.5px solid #c1121f',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.04)'
                })
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
            desc = "No correlation attribute selected."
            return go.Figure(), html.Div([
                indicator,
                html.Div(desc, style={'flex': '1'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
        y_subcat = corr_subcats[0]
        y_col = y_subcat + '_pct' if (y_subcat + '_pct') in df_state.columns else y_subcat
        if x_col not in df_state.columns or y_col not in df_state.columns:
            indicator = html.Div([
                html.Div("Unrelated", style={
                    'display': 'inline-block',
                    'backgroundColor': '#f8d7da',
                    'color': '#c1121f',
                    'borderRadius': '6px',
                    'padding': '4px 12px',
                    'fontWeight': 'bold',
                    'fontSize': '13px',
                    'marginRight': '12px',
                    'border': '1.5px solid #c1121f',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.04)'
                })
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
            desc = "Selected attributes not available for this state."
            return go.Figure(), html.Div([
                indicator,
                html.Div(desc, style={'flex': '1'})
            ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
        df_state = df_state[['District name', x_col, y_col]].dropna()
        # Calculate Pearson correlation coefficient
        if len(df_state) < 2:
            corr_val = None
        else:
            corr_val = np.corrcoef(df_state[x_col], df_state[y_col])[0, 1]
        # Scatter plot for district values
        fig = go.Figure(go.Scatter(
            x=df_state[x_col],
            y=df_state[y_col],
            mode='markers+text',
            text=df_state['District name'],
            textposition='top center',
            marker=dict(
                size=13,
                color=df_state[x_col],
                colorscale='Viridis',
                line=dict(width=1, color='#277da1'),
                opacity=0.85,
            ),
            hovertemplate='<b>%{text}</b><br>X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>',
        ))
        fig.update_layout(
            title=f"Correlation: {short_label(selected_subcat)} vs {short_label(y_subcat)} in {state_name}",
            xaxis_title=short_label(selected_subcat),
            yaxis_title=short_label(y_subcat),
            plot_bgcolor='#f8f9fa',
            paper_bgcolor='white',
            font=PLOTLY_FONT,
            margin=dict(l=30, r=10, t=40, b=30),
            height=220,
        )
        # Description for non-technical users
        desc = f"Each point represents a district in {state_name}. The X-axis shows the value for '{short_label(selected_subcat)}', and the Y-axis shows the value for '{short_label(y_subcat)}'. If the points form a clear pattern (like a line), the two attributes are related. If the points are scattered randomly, the attributes are likely unrelated."
        # Indicator box logic (color and label based on correlation strength)
        if corr_val is not None:
            desc += f"<br/><b>Correlation coefficient (r):</b> {corr_val:.2f}. "
            abs_r = abs(corr_val)
            if abs_r < 0.2:
                # Unrelated: red, intensity by abs_r
                intensity = int(215 + 40 * abs_r)  # 215-255
                bg = f"#f8d7da"
                border = f"#c1121f"
                color = f"#c1121f"
                label = "Unrelated"
            elif abs_r > 0.7:
                # Related: green, intensity by abs_r
                g = int(180 + 60 * (abs_r - 0.7) / 0.3) if abs_r < 1 else 240
                bg = f"#d1f7d6"
                border = f"#2d6a4f"
                color = f"#2d6a4f"
                label = "Related"
            else:
                # Somewhat related: yellow, intensity by abs_r
                y = int(220 + 25 * (abs_r - 0.2) / 0.5)
                bg = f"#fff3cd"
                border = f"#e1b800"
                color = f"#b8860b"
                label = "Somewhat related"
            indicator = html.Div([
                html.Div(label, style={
                    'display': 'inline-block',
                    'backgroundColor': bg,
                    'color': color,
                    'borderRadius': '6px',
                    'padding': '4px 12px',
                    'fontWeight': 'bold',
                    'fontSize': '13px',
                    'marginRight': '12px',
                    'border': f'1.5px solid {border}',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.04)'
                })
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
        else:
            indicator = html.Div([
                html.Div("Unrelated", style={
                    'display': 'inline-block',
                    'backgroundColor': '#f8d7da',
                    'color': '#c1121f',
                    'borderRadius': '6px',
                    'padding': '4px 12px',
                    'fontWeight': 'bold',
                    'fontSize': '13px',
                    'marginRight': '12px',
                    'border': '1.5px solid #c1121f',
                    'boxShadow': '0 1px 4px rgba(0,0,0,0.04)'
                })
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
        return fig, html.Div([
            indicator,
            html.Div(desc, style={'flex': '1'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})
    except Exception as e:
        print("Correlation scatter error:", e)
        indicator = html.Div([
            html.Div("Unrelated", style={
                'display': 'inline-block',
                'backgroundColor': '#f8d7da',
                'color': '#c1121f',
                'borderRadius': '6px',
                'padding': '4px 12px',
                'fontWeight': 'bold',
                'fontSize': '13px',
                'marginRight': '12px',
                'border': '1.5px solid #c1121f',
                'boxShadow': '0 1px 4px rgba(0,0,0,0.04)'
            })
        ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '6px'})
        desc = "Unable to display correlation."
        return go.Figure(), html.Div([
            indicator,
            html.Div(desc, style={'flex': '1'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'})


# =========================
# Main Entrypoint
# =========================

if __name__ == "__main__":
    # Run the Dash app in debug mode
    app.run(debug=True)

