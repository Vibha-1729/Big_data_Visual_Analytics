import pandas as pd
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
from scipy.stats import pearsonr, spearmanr

# ------------------------
# 1. Load & prepare data
# ------------------------
district_df = pd.read_excel(
    r"C:\Users\aadya\OneDrive\Desktop\CS661_COURSE\censuscope\india-districts-census-2011.xlsx",
    sheet_name="india-districts-census-2011"
)
state_df = pd.read_excel(
    r"C:\Users\aadya\OneDrive\Desktop\CS661_COURSE\censuscope\statewise_aggregated_data.xlsx"
)

ATTRIBUTE_MAP = {
    "Population": ["Male", "Female"],
    "Literacy": ["Male_Literate", "Female_Literate", "Literate_Education", "Illiterate_Education"],
    "Category (Caste)": ["Male_SC", "Female_SC", "Male_ST", "Female_ST"],
    "Employment": ["Workers", "Male_Workers", "Female_Workers"],
    "Employment Type": [
        "Main_Workers", "Marginal_Workers", "Non_Workers",
        "Cultivator_Workers", "Agricultural_Workers",
        "Household_Workers", "Other_Workers"
    ],
    "Religion": [
        "Hindus", "Muslims", "Sikhs", "Jains", "Buddhists", "Others_Religions", "Religion_Not_Stated"
    ],
    "Household Access": [
        "LPG_or_PNG_Households", "Housholds_with_Electric_Lighting",
        "Households_with_Internet", "Households_with_Computer"
    ],
    "Locality": ["Rural_Households", "Urban_Households", "Households"],
    "Education": [
        "Below_Primary_Education", "Primary_Education", "Middle_Education",
        "Secondary_Education", "Higher_Education", "Graduate_Education", "Other_Education"
    ],
    "Age Group": ["Age_Group_0_29", "Age_Group_30_49", "Age_Group_50", "Age not stated"],
    "Assets": [
        "Households_with_Telephone_Mobile_Phone_Landline_only",
        "Households_with_Telephone_Mobile_Phone_Mobile_only", "Households_with_Television",
        "Households_with_Telephone_Mobile_Phone",
        "Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car"
    ],
    "Vehicles": ["Households_with_Bicycle", "Households_with_Car_Jeep_Van", "Households_with_Scooter_Motorcycle_Moped"],
    "House Ownership": ["Ownership_Owned_Households", "Ownership_Rented_Households"],
    "Washroom Facilities": [
        "Type_of_latrine_facility_Pit_latrine_Households",
        "Type_of_latrine_facility_Other_latrine_Households",
        "Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households",
        "Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households",
        "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households"
    ],
    "Drinking Facilities": [
        "Main_source_of_drinking_water_Un_covered_well_Households",
        "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households",
        "Main_source_of_drinking_water_Spring_Households",
        "Main_source_of_drinking_water_River_Canal_Households",
        "Main_source_of_drinking_water_Other_sources_Households",
        "Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households",
        "Location_of_drinking_water_source_Near_the_premises_Households",
        "Location_of_drinking_water_source_Within_the_premises_Households",
        "Main_source_of_drinking_water_Tank_Pond_Lake_Households",
        "Main_source_of_drinking_water_Tapwater_Households",
        "Main_source_of_drinking_water_Tubewell_Borehole_Households",
        "Location_of_drinking_water_source_Away_Households"
    ],
    "Power Parity": [
        "Power_Parity_Less_than_Rs_45000",
        "Power_Parity_Rs_45000_150000",
        "Power_Parity_Rs_150000_330000",
        "Power_Parity_Rs_330000_545000",
        "Power_Parity_Above_Rs_545000"
    ]
}

states = state_df["State name"].unique()

# ------------------------
# 2. Initialize app & define layout
# ------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    # Title
    html.H4(
        "Compare Two States by Attribute",
        style={
            "marginTop": "5px",
            "marginBottom": "10px"
        }
    ),

    # Dropdowns + Graph
    dbc.Row([
        # Left column: selectors
        dbc.Col([
            dcc.Dropdown(
                id="state1-dropdown",
                options=[{"label": s, "value": s} for s in states],
                placeholder="Select first state",
                style={"margin-bottom": "10px"}
            ),
            dcc.Dropdown(
                id="state2-dropdown",
                options=[{"label": s, "value": s} for s in states],
                placeholder="Select second state",
                style={"margin-bottom": "10px"}
            ),
            dcc.Dropdown(
                id="category-dropdown",
                options=[{"label": k, "value": k} for k in ATTRIBUTE_MAP],
                placeholder="Select attribute",
                disabled=True,
                style={"margin-bottom": "20px"}
            ),
        ], width=4),

        # Right column: comparison chart in a Card
        dbc.Col(
            dbc.Card([
                dbc.CardHeader("Attribute Comparison", className="bg-primary text-white"),
                dbc.CardBody(
                    dcc.Graph(
                        id="state-comparison-bar",
                        config={"displayModeBar": False},
                        style={
                            "height": "460px",
                            "width": "100%",
                            "margin": "0 auto"
                        }
                    ),
                    className="p-2"
                )
            ], className="shadow-sm mb-4"),
            width=8
        ),
    ], style={"marginTop": "0", "paddingTop": "0"}),

], fluid=True, style={"paddingTop": "0px"})

# ------------------------
# 3. Callbacks
# ------------------------
@app.callback(
    Output("category-dropdown", "disabled"),
    Input("state1-dropdown", "value"),
    Input("state2-dropdown", "value"),
)
def toggle_category(s1, s2):
    return not (s1 and s2)


@app.callback(
    Output("state-comparison-bar", "figure"),
    Output("state-comparison-bar", "style"),
    Input("state1-dropdown", "value"),
    Input("state2-dropdown", "value"),
    Input("category-dropdown", "value"),
)
def update_chart(s1, s2, category):
    if not (s1 and s2 and category):
        return go.Figure(), {"display": "none"}

    subs = ATTRIBUTE_MAP[category]
    row1 = state_df[state_df["State name"] == s1].iloc[0]
    row2 = state_df[state_df["State name"] == s2].iloc[0]
    vals1 = np.array([row1[sub] for sub in subs], dtype=float)
    vals2 = np.array([row2[sub] for sub in subs], dtype=float)

    p_corr, _ = pearsonr(vals1, vals2)
    s_corr, _ = spearmanr(vals1, vals2)

    fig = go.Figure([
        go.Bar(x=subs, y=vals1, name=s1),
        go.Bar(x=subs, y=vals2, name=s2)
    ])
    fig.update_layout(
        barmode="group",
        template="plotly_white",
        title=f"{category}: {s1} vs {s2}<br>Pearson={p_corr:.2f}, Spearman={s_corr:.2f}",
        xaxis_title="Subcategory",
        yaxis_title="Value",
        height=460  # match the card height
    )

    # show the card
    style = {
        "height": "460px",
        "width": "100%",
        "margin": "0 auto",
        "display": "block"
    }
    return fig, style

# ------------------------
# 4. Run server
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
