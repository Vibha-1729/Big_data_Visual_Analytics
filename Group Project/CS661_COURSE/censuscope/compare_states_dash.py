import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.graph_objs as go

# ---- Attribute Map ----
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

# ---- Load Data ----
df = pd.read_excel("india-districts-census-2011.xlsx", sheet_name="india-districts-census-2011")

states = sorted(df["State name"].unique())
default_main = "Population"
default_sub = ATTRIBUTE_MAP[default_main][0]
default_state1 = states[0]
default_state2 = states[1] if len(states) > 1 else states[0]

# ---- Dash App ----
app = Dash(__name__)
app.title = "Two-State Attribute Comparison (India District Census 2011)"

app.layout = html.Div([
    html.H2("Compare Attributes Across Two States (District Level)"),
    html.Div([
        html.Label("Main Attribute:"),
        dcc.Dropdown(
            id="main-attr",
            options=[{"label": k, "value": k} for k in ATTRIBUTE_MAP.keys()],
            value=default_main,
            clearable=False,
            style={"width": "300px"}
        ),
    ], style={"margin": "10px"}),

    html.Div([
        html.Label("Subcategory:"),
        dcc.Dropdown(
            id="sub-attr",
            options=[{"label": sub, "value": sub} for sub in ATTRIBUTE_MAP[default_main]],
            value=default_sub,
            clearable=False,
            style={"width": "400px"}
        ),
    ], style={"margin": "10px"}),

    html.Div([
        html.Label("State 1:"),
        dcc.Dropdown(
            id="state-1",
            options=[{"label": st, "value": st} for st in states],
            value=default_state1,
            clearable=False,
            style={"width": "400px"}
        ),
    ], style={"margin": "10px", "display": "inline-block", "vertical-align": "top"}),

    html.Div([
        html.Label("State 2:"),
        dcc.Dropdown(
            id="state-2",
            options=[{"label": st, "value": st} for st in states],
            value=default_state2,
            clearable=False,
            style={"width": "400px"}
        ),
    ], style={"margin": "10px", "display": "inline-block", "vertical-align": "top"}),

    dcc.Graph(id="comparison-graph"),
    html.Div(id="note", style={"margin": "10px", "color": "gray"}),
])

# ---- Callbacks ----

@app.callback(
    Output("sub-attr", "options"),
    Output("sub-attr", "value"),
    Input("main-attr", "value"),
)
def update_subcategory_options(main_attr):
    subcats = ATTRIBUTE_MAP[main_attr]
    return [{"label": sub, "value": sub} for sub in subcats], subcats[0]

@app.callback(
    Output("comparison-graph", "figure"),
    Output("note", "children"),
    Input("main-attr", "value"),
    Input("sub-attr", "value"),
    Input("state-1", "value"),
    Input("state-2", "value"),
)
def update_graph(main_attr, sub_attr, state1, state2):
    d1 = df[df["State name"] == state1]
    d2 = df[df["State name"] == state2]

    # Sort by attribute descending for better readability
    d1_sorted = d1.sort_values(by=sub_attr, ascending=False)
    d2_sorted = d2.sort_values(by=sub_attr, ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=d1_sorted["District name"], y=d1_sorted[sub_attr],
        name=state1, marker_color='royalblue'
    ))
    fig.add_trace(go.Bar(
        x=d2_sorted["District name"], y=d2_sorted[sub_attr],
        name=state2, marker_color='indianred'
    ))

    fig.update_layout(
        barmode="group",
        title=f"{sub_attr} - Districtwise Comparison: {state1} vs {state2}",
        xaxis_title="District",
        yaxis_title=sub_attr,
        xaxis_tickangle=45,
        legend_title="State",
        height=600,
        width=1200
    )

    note = f"Showing values for {sub_attr} in districts of {state1} and {state2}."
    return fig, note

# ---- Run App ----
if __name__ == "__main__":
    app.run(debug=True)

