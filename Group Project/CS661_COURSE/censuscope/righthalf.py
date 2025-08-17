import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# --- Load data ---
district_df = pd.read_excel(
    r"C:\Users\aadya\OneDrive\Desktop\CS661_COURSE\censuscope\india-districts-census-2011.xlsx",
    sheet_name="india-districts-census-2011"
)

state_df = pd.read_excel( r"C:\Users\aadya\OneDrive\Desktop\CS661_COURSE\censuscope\statewise_aggregated_data.xlsx")

ATTRIBUTE_MAP = {
    "Population": ["Male", "Female"],
    "Literacy": ["Male_Literate", "Female_Literate", "Literate_Education", "Illiterate_Education"],
    "Category (Caste)": ["Male_SC", "Female_SC", "Male_ST", "Female_ST"],
    "Employment": [
        "Workers", "Male_Workers", "Female_Workers"
    ],
    "Employment Type": ["Main_Workers", "Marginal_Workers",
        "Non_Workers", "Cultivator_Workers", "Agricultural_Workers",
        "Household_Workers", "Other_Workers"],
    "Religion": [
        "Hindus", "Muslims", "Sikhs", "Jains", "Buddhists", "Others_Religions", "Religion_Not_Stated"
    ],
    "Household Access": [
        "LPG_or_PNG_Households", "Housholds_with_Electric_Lighting", "Households_with_Internet",
        "Households_with_Computer"
    ],
    "Locality": ["Rural_Households", "Urban_Households", "Households"],
    "Education": [
        "Below_Primary_Education", "Primary_Education", "Middle_Education",
        "Secondary_Education", "Higher_Education", "Graduate_Education",
        "Other_Education"
    ],
    "Age Group": ["Age_Group_0_29", "Age_Group_30_49", "Age_Group_50", "Age not stated"],
    "Assets": [
        "Households_with_Telephone_Mobile_Phone_Landline_only",
        "Households_with_Telephone_Mobile_Phone_Mobile_only", "Households_with_Television",
        "Households_with_Telephone_Mobile_Phone", 
        "Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car"
    ],
    "Vehicles": ["Households_with_Bicycle", "Households_with_Car_Jeep_Van",
        "Households_with_Scooter_Motorcycle_Moped"],
    "House Ownership": [
        "Ownership_Owned_Households", "Ownership_Rented_Households"],
    "Washroom Facilities": [
        "Type_of_latrine_facility_Pit_latrine_Households", "Type_of_latrine_facility_Other_latrine_Households",
        "Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households",
        "Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households",
        "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households"
    ],
    "Drinking Facilities": ["Main_source_of_drinking_water_Un_covered_well_Households", "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households",
        "Main_source_of_drinking_water_Spring_Households", "Main_source_of_drinking_water_River_Canal_Households",
        "Main_source_of_drinking_water_Other_sources_Households", "Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households",
        "Location_of_drinking_water_source_Near_the_premises_Households", "Location_of_drinking_water_source_Within_the_premises_Households",
        "Main_source_of_drinking_water_Tank_Pond_Lake_Households", "Main_source_of_drinking_water_Tapwater_Households",
        "Main_source_of_drinking_water_Tubewell_Borehole_Households", "Location_of_drinking_water_source_Away_Households"],
    "Power Parity": [
        "Power_Parity_Less_than_Rs_45000", 
        "Power_Parity_Rs_45000_150000",
        "Power_Parity_Rs_150000_330000",
        "Power_Parity_Rs_330000_545000", "Power_Parity_Above_Rs_545000"
    ]
}
states = state_df["State name"].unique()

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    dbc.Row([
        # LEFT PANEL: Controls and both graphs (fixed, no scroll)
        dbc.Col([
            html.H4("State, Attribute & Subcategory Drilldown", style={"margin-bottom": "6px", "fontSize": "19px"}),
            dcc.Dropdown(
                id="state-dropdown",
                options=[{"label": s, "value": s} for s in states],
                value=None,
                placeholder="Select a state",
                style={"margin-bottom": "7px", "fontSize": "15px"}
            ),
            dcc.Dropdown(
                id="category-dropdown",
                options=[{"label": k, "value": k} for k in ATTRIBUTE_MAP.keys()],
                value=None,
                placeholder="Select attribute",
                style={"margin-bottom": "7px", "fontSize": "15px"},
                disabled=True
            ),
            dcc.Dropdown(
                id="subcategory-dropdown",
                options=[],
                value=None,
                placeholder="Select subcategory",
                style={"margin-bottom": "7px", "fontSize": "15px"},
                disabled=True
            ),
            dcc.Graph(
                id="state-subcat-bar",
                config={"displayModeBar": False},
                style={"height": "225px", "margin-bottom": "4px", "display": "none"}
            ),
            dcc.Graph(
                id="top5-bottom5-bar",
                config={"displayModeBar": False},
                style={"height": "225px", "margin-bottom": "4px", "display": "none"}
            )
        ], width=5, style={"minHeight": "97vh", "overflow": "hidden", "padding": "16px 10px 10px 16px", "background": "#f9f9fa"}),
        # RIGHT PANEL: Placeholder (replace with your map or any content)
        dbc.Col([
            html.Div("MAP or any other visualization here", style={
                "height": "97vh",
                "background": "#f8f9fa",
                "border": "1px solid #dee2e6",
                "display": "flex", "alignItems": "center", "justifyContent": "center",
                "fontSize": 22, "color": "#aaa"
            })
        ], width=7)
    ], style={"minHeight": "97vh", "overflow": "hidden"})
], fluid=True, style={"padding": "0px"})

# --- Callbacks ---

@app.callback(
    Output("category-dropdown", "disabled"),
    Output("category-dropdown", "value"),
    Input("state-dropdown", "value"),
)
def enable_category_dropdown(selected_state):
    if selected_state:
        return False, None
    else:
        return True, None

@app.callback(
    Output("state-subcat-bar", "figure"),
    Output("state-subcat-bar", "style"),
    Output("subcategory-dropdown", "options"),
    Output("subcategory-dropdown", "value"),
    Output("subcategory-dropdown", "disabled"),
    Input("state-dropdown", "value"),
    Input("category-dropdown", "value"),
)
def show_state_subcat_bar(selected_state, category):
    if not selected_state or not category:
        return go.Figure(), {"height": "225px", "display": "none"}, [], None, True
    subcats = ATTRIBUTE_MAP[category]
    row = state_df[state_df["State name"] == selected_state]
    values = [row[sub].values[0] for sub in subcats]
    fig = go.Figure(go.Bar(x=subcats, y=values, marker_color='#3275a8'))
    fig.update_layout(
        template="plotly_white",
        title=f"{selected_state}: Subcategory totals",
        xaxis_title="Subcategory",
        yaxis_title="Total Value",
        font={"family": "Lato"},
        margin={"l":18,"r":14,"t":36,"b":32},
        height=225
    )
    subcat_options = [{"label": sub, "value": sub} for sub in subcats]
    return fig, {"height": "225px", "display": "block", "margin-bottom": "4px"}, subcat_options, None, False

@app.callback(
    Output("top5-bottom5-bar", "figure"),
    Output("top5-bottom5-bar", "style"),
    Input("state-dropdown", "value"),
    Input("category-dropdown", "value"),
    Input("subcategory-dropdown", "value"),
)
def show_top5_bottom5_districts(selected_state, category, subcat):
    if not selected_state or not category or not subcat:
        return go.Figure(), {"height": "225px", "display": "none"}
    use_df = district_df[district_df["State name"] == selected_state]
    sorted_df = use_df[["District name", subcat]].sort_values(by=subcat, ascending=False)
    top5 = sorted_df.head(5)
    bottom5 = sorted_df.tail(5)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=top5["District name"], y=top5[subcat], name="Top 5", marker_color="#2ca02c", text=top5[subcat], textposition="auto"
    ))
    fig.add_trace(go.Bar(
        x=bottom5["District name"], y=bottom5[subcat], name="Bottom 5", marker_color="#d62728", text=bottom5[subcat], textposition="auto"
    ))
    fig.update_layout(
        barmode="group",
        template="plotly_white",
        title=f"Top 5 & Bottom 5 Districts in {selected_state} for {subcat}",
        xaxis_title="District",
        yaxis_title=subcat,
        font={"family": "Lato"},
        margin={"l":18,"r":14,"t":36,"b":32},
        height=225,
        legend_title="District Group"
    )
    return fig, {"height": "225px", "display": "block", "margin-bottom": "4px"}

if __name__ == "__main__":
    app.run(debug=True)
