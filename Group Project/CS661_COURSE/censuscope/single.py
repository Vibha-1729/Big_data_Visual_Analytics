import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# ---- Attribute Map ----
ATTRIBUTE_MAP = {
    "Population": ["Male", "Female"],
    "Literacy": ["Male_Literate", "Female_Literate" ,"Literate_Education", "Illiterate_Education"],
    "Category (Caste)": ["Male_SC", "Female_SC", "Male_ST", "Female_ST"],
    "Employment": [
        "Workers", "Male_Workers", "Female_Workers"
    ],
    "Employment Type":["Main_Workers", "Marginal_Workers",
        "Non_Workers", "Cultivator_Workers", "Agricultural_Workers",
        "Household_Workers", "Other_Workers"],
    "Religion": [
        "Hindus", "Muslims", "Sikhs", "Jains", "Buddhists", "Others_Religions", "Religion_Not_Stated"
    ],
    "Household Access": [
        "LPG_or_PNG_Households", "Housholds_with_Electric_Lighting", "Households_with_Internet",
        "Households_with_Computer"
    ],
    "Locality":[ "Rural_Households", "Urban_Households", "Households"],
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
    "Vehicles":["Households_with_Bicycle", "Households_with_Car_Jeep_Van",
        "Households_with_Scooter_Motorcycle_Moped"],
    "House Ownership":[
        "Ownership_Owned_Households", "Ownership_Rented_Households"],
    "Washroom Facilities": [
        "Type_of_latrine_facility_Pit_latrine_Households", "Type_of_latrine_facility_Other_latrine_Households",
        "Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households",
        "Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households",
        "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households"
    ],
    "Drinking Facilities":["Main_source_of_drinking_water_Un_covered_well_Households", "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households",
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
# ---- Load Data ----
df = pd.read_excel("india-districts-census-2011.xlsx", sheet_name="india-districts-census-2011")

states = sorted(df["State name"].unique())
default_state = states[0]
default_main = "Population"
default_sub = ATTRIBUTE_MAP[default_main][0]

# ---- Dash App ----
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "CensorScope: Single State District Analysis"

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="CensorScope | Single State Analysis",
        color="primary",
        dark=True,
        fluid=True,
        style={"border-radius": "10px", "margin-bottom": "25px"}
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Select State & Attribute", className="card-title"),
                    html.Label("State:"),
                    dcc.Dropdown(
                        id="state-dropdown",
                        options=[{"label": st, "value": st} for st in states],
                        value=default_state,
                        clearable=False,
                        style={"margin-bottom": "15px"}
                    ),
                    html.Label("Main Attribute:"),
                    dcc.Dropdown(
                        id="main-attr",
                        options=[{"label": k, "value": k} for k in ATTRIBUTE_MAP.keys()],
                        value=default_main,
                        clearable=False,
                        style={"margin-bottom": "15px"}
                    ),
                    html.Label("Subcategory:"),
                    dcc.Dropdown(
                        id="sub-attr",
                        options=[{"label": sub, "value": sub} for sub in ATTRIBUTE_MAP[default_main]],
                        value=default_sub,
                        clearable=False,
                        style={"margin-bottom": "15px"}
                    ),
                ])
            ])
        ], md=5),
    ], justify="center"),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="state-graph", config={'displayModeBar': False}),
                    html.Div(id="note", style={"color": "gray", "margin-top": "15px", "font-size": "1rem"})
                ])
            ], style={"box-shadow": "0 4px 12px rgba(0,0,0,0.08)", "border-radius": "18px"})
        ], width=12)
    ]),
    html.Br(),
], fluid=True)

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
    Output("state-graph", "figure"),
    Output("note", "children"),
    Input("state-dropdown", "value"),
    Input("main-attr", "value"),
    Input("sub-attr", "value"),
)
def update_state_graph(state, main_attr, sub_attr):
    state_df = df[df["State name"] == state]
    state_sorted = state_df.sort_values(by=sub_attr, ascending=False)

    top5 = state_sorted.head(5)
    bottom5 = state_sorted.tail(5)

    fig = go.Figure()

    # Top 5: blue, Bottom 5: red
    fig.add_trace(go.Bar(
        x=top5["District name"], y=top5[sub_attr],
        name="Top 5", marker_color='#2ca02c', # greenish
        text=top5[sub_attr], textposition="auto"
    ))
    fig.add_trace(go.Bar(
        x=bottom5["District name"], y=bottom5[sub_attr],
        name="Bottom 5", marker_color='#d62728', # reddish
        text=bottom5[sub_attr], textposition="auto"
    ))

    fig.update_layout(
        barmode="group",
        template="plotly_white",
        title={
            "text": f"Top 5 & Bottom 5 Districts in {state}: {sub_attr}",
            "x": 0.5,
            "font": {"size": 22, "family": "Lato"}
        },
        xaxis_title="District",
        yaxis_title=sub_attr,
        xaxis_tickangle=45,
        legend_title="District Group",
        font={"family": "Lato"},
        margin={"l":30,"r":30,"t":80,"b":80},
        height=600,
        width=900
    )

    note = f"Showing <b>top 5</b> (green) and <b>bottom 5</b> (red) districts for <b>{sub_attr}</b> in <b>{state}</b>."
    return fig, note

# ---- Run App ----
if __name__ == "__main__":
    app.run(debug=True)
