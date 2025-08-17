import json
import os
import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from scipy.stats import pearsonr, spearmanr
import numpy as np

# ------------------------
# 1. Load & prepare data
# ------------------------
district_df = pd.read_excel(
    r"C:\Users\Vibha Narayan\OneDrive\Desktop\coding\GitDemo\CS661\Group Project\CS661_COURSE\censuscope\india-districts-census-2011.xlsx",
    sheet_name="india-districts-census-2011"
)
state_df = pd.read_excel(
    r"C:\Users\Vibha Narayan\OneDrive\Desktop\coding\GitDemo\CS661\Group Project\CS661_COURSE\censuscope\statewise_aggregated_data.xlsx"
)

# Normalize district and state names
district_df["district_norm"] = district_df["District name"].str.strip().str.upper()
state_df["State name"] = state_df["State name"].str.strip()

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
    "Religion": ["Hindus", "Muslims", "Sikhs", "Jains", "Buddhists", "Others_Religions", "Religion_Not_Stated"],
    "Household Access": ["LPG_or_PNG_Households", "Housholds_with_Electric_Lighting", "Households_with_Internet", "Households_with_Computer"],
    "Locality": ["Rural_Households", "Urban_Households", "Households"],
    "Education": ["Below_Primary_Education", "Primary_Education", "Middle_Education", "Secondary_Education", "Higher_Education", "Graduate_Education", "Other_Education"],
    "Age Group": ["Age_Group_0_29", "Age_Group_30_49", "Age_Group_50", "Age not stated"],
    "Assets": [
        "Households_with_Telephone_Mobile_Phone_Landline_only",
        "Households_with_Telephone_Mobile_Phone_Mobile_only",
        "Households_with_Television",
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
map_modes = [
    {"label": "Most subcategory district", "value": "max"},
    {"label": "Least subcategory district", "value": "min"},
    {"label": "Top 5 / Bottom 5", "value": "topbot"},
    {"label": "5 Nearest to Average", "value": "avg5"}
]
import json
import os
import pandas as pd
from dash import Dash, dcc, html, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from scipy.stats import pearsonr, spearmanr
import numpy as np
def get_sidebar():
    return html.Div([
        html.Div([
            html.Div([
                html.Span("🅱", style={"fontSize": "2rem", "marginRight": "10px"}),
                html.Span("Sidebar", style={"fontSize": "1.5rem", "fontWeight": "bold"})
            ], style={"display": "flex", "alignItems": "center", "marginBottom": "10px"}),
            html.Hr(style={"borderColor": "#444"}),
            html.Div([
                html.Div([
                    html.Span("🏠", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    html.Span("Home", style={"fontSize": "1.1rem", "fontWeight": "500"})
                ], style={"background": "#0d6efd", "color": "#fff", "borderRadius": "7px", "padding": "10px 18px", "marginBottom": "8px", "display": "flex", "alignItems": "center"}),
                html.Div([
                    html.Span("🧮", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    html.Span("Dashboard", style={"fontSize": "1.1rem", "fontWeight": "500"})
                ], style={"color": "#f8f8f8", "padding": "10px 18px", "marginBottom": "8px", "display": "flex", "alignItems": "center", "cursor": "pointer"}),
                html.Div([
                    html.Span("📋", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    html.Span("Orders", style={"fontSize": "1.1rem", "fontWeight": "500"})
                ], style={"color": "#f8f8f8", "padding": "10px 18px", "marginBottom": "8px", "display": "flex", "alignItems": "center", "cursor": "pointer"}),
                html.Div([
                    html.Span("🔲", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    html.Span("Products", style={"fontSize": "1.1rem", "fontWeight": "500"})
                ], style={"color": "#f8f8f8", "padding": "10px 18px", "marginBottom": "8px", "display": "flex", "alignItems": "center", "cursor": "pointer"}),
                html.Div([
                    html.Span("👤", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    html.Span("Customers", style={"fontSize": "1.1rem", "fontWeight": "500"})
                ], style={"color": "#f8f8f8", "padding": "10px 18px", "marginBottom": "8px", "display": "flex", "alignItems": "center", "cursor": "pointer"}),
            ], style={"marginBottom": "32px"}),
            html.Hr(style={"borderColor": "#444"}),
            html.Div([
                html.Div([
                    html.Img(src="https://randomuser.me/api/portraits/men/1.jpg", style={"width": "32px", "height": "32px", "borderRadius": "50%", "marginRight": "10px"}),
                    html.Span("mdo", style={"fontWeight": "bold", "fontSize": "1.1rem"}),
                    html.Span("▼", style={"marginLeft": "6px", "fontSize": "0.9rem"})
                ], style={"display": "flex", "alignItems": "center"})
            ], style={"marginTop": "auto", "paddingTop": "16px"})
        ], style={"display": "flex", "flexDirection": "column", "height": "100vh"}),
    ],
    style={
        "height": "100vh",
        "width": "400px",
        "background": "#23272f",
        "color": "#f8f8f8",
        "font-family": "Segoe UI, Roboto, Arial, sans-serif",
        "padding": "28px 24px 24px 24px",
        "box-shadow": "4px 0px 16px rgba(0, 0, 0, 0.18)",
        "position": "absolute",
        "top": "0",
        "left": "0",
        "z-index": "1000"
    })

# ------------------------
# 2. Dash layout
# ------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Sidebar layout
def get_sidebar():
    return html.Div([
        html.H3("State & Attribute Selection", className="text-center", style={
            "padding-top": "20px",
            "color": "#23272f",
            "fontWeight": "bold"
        }),
        html.Hr(style={"borderColor": "#ddd"}),
        html.Label("First State", style={"color": "#23272f", "fontWeight": "500", "marginBottom": "4px"}),
        dcc.Dropdown(
            id="state1-dropdown",
            options=[{"label": s, "value": s} for s in states],
            placeholder="Select first state",
            style={"margin-bottom": "14px"}
        ),
        html.Label("Second State", style={"color": "#23272f", "fontWeight": "500", "marginBottom": "4px"}),
        dcc.Dropdown(
            id="state2-dropdown",
            options=[{"label": s, "value": s} for s in states],
            placeholder="Select second state",
            style={"margin-bottom": "14px"}
        ),
        html.Label("Attribute", style={"color": "#23272f", "fontWeight": "500", "marginBottom": "4px"}),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{"label": k, "value": k} for k in ATTRIBUTE_MAP],
            placeholder="Select attribute",
            disabled=True,
            style={"margin-bottom": "14px"}
        ),
        html.Label("Subcategory", style={"color": "#23272f", "fontWeight": "500", "marginBottom": "4px"}),
        dcc.Dropdown(
            id="subcat-dropdown",
            placeholder="Select subcategory",
            disabled=True,
            style={"margin-bottom": "14px"}
        ),
        html.Label("Map Mode", style={"color": "#23272f", "fontWeight": "500", "marginBottom": "4px"}),
        dcc.Dropdown(
            id="map-mode-dropdown",
            options=map_modes,
            placeholder="Select map mode",
            disabled=True,
            style={"margin-bottom": "14px"}
        ),
    ],
    style={
        "height": "100vh",
        "width": "400px",
        "background": "#fff",
        "color": "#23272f",
        "font-family": "Segoe UI, Roboto, Arial, sans-serif",
        "padding": "28px 24px 24px 24px",
        "box-shadow": "4px 0px 16px rgba(0, 0, 0, 0.08)",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "z-index": "1000",
        "borderRight": "1px solid #eee"
    })

def get_content():
    return html.Div([
        html.H4("Compare Two States by Attribute", style={"margin-bottom": "20px"}),
        dbc.Row([
            dbc.Col(dcc.Graph(id="state-comparison-radar", style={"display": "none", "height": "70vh", "width": "100%"}, config={"displayModeBar": True, "scrollZoom": True}), width=12),
        ], style={"margin-bottom": "10px"}),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Graph(id="state1-choropleth", style={"display": "none", "height": "50vh", "width": "100%"}, config={"displayModeBar": True, "scrollZoom": True}), width=6),
            dbc.Col(dcc.Graph(id="state2-choropleth", style={"display": "none", "height": "50vh", "width": "100%"}, config={"displayModeBar": True, "scrollZoom": True}), width=6),
        ], style={"margin-bottom": "10px"})
    ],
    style={
        "padding": "20px 24px 20px 424px",  # 400px sidebar + 24px padding
        "background-color": "#fff",
        "min-height": "100vh",
        "width": "100vw"
    })

# App layout
sidebar = get_sidebar()
content = get_content()
app.layout = html.Div([
    sidebar,
    content
])

# ------------------------
# 3. Callbacks
# ------------------------
@app.callback(
    Output("category-dropdown", "disabled"),
    Input("state1-dropdown", "value"),
    Input("state2-dropdown", "value")
)
def enable_category(s1, s2):
    return not (s1 and s2)

@app.callback(
    Output("subcat-dropdown", "options"),
    Output("subcat-dropdown", "disabled"),
    Input("category-dropdown", "value")
)
def set_subcats(cat):
    if not cat:
        return [], True
    return [{"label": sc, "value": sc} for sc in ATTRIBUTE_MAP[cat]], False

@app.callback(
    Output("map-mode-dropdown", "disabled"),
    Input("subcat-dropdown", "value")
)
def enable_map_mode(sub):
    return sub is None

@app.callback(
    Output("state-comparison-radar", "figure"),
    Output("state-comparison-radar", "style"),
    Input("state1-dropdown", "value"),
    Input("state2-dropdown", "value"),
    Input("category-dropdown", "value")
)
def update_radar(s1, s2, cat):
    if not (s1 and s2 and cat):
        return go.Figure(), {"display":"none", "height": "70vh", "width": "100%"}
    try:
        subs = ATTRIBUTE_MAP[cat]
        v1 = [float(state_df.loc[state_df["State name"]==s1, sc].values[0]) for sc in subs]
        v2 = [float(state_df.loc[state_df["State name"]==s2, sc].values[0]) for sc in subs]
        p, _ = pearsonr(v1, v2)
        s, _ = spearmanr(v1, v2)
    except:
        return go.Figure(), {"display":"none", "height": "70vh", "width": "100%"}
    theta = subs + [subs[0]]
    r1 = v1 + [v1[0]]
    r2 = v2 + [v2[0]]
    fig = go.Figure([
        go.Scatterpolar(r=r1, theta=theta, fill='toself', name=s1, marker=dict(size=8)),
        go.Scatterpolar(r=r2, theta=theta, fill='toself', name=s2, marker=dict(size=8)),
    ])
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        template="plotly_white",
        title=f"{cat}: {s1} vs {s2}<br>Pearson={p:.2f}, Spearman={s:.2f}",
        height=700,
        font=dict(color="#222"),
        legend=dict(font=dict(color="#222"))
    )
    return fig, {"display":"block", "height": "70vh", "width": "100%"}

@app.callback(
    Output("state1-choropleth", "figure"),
    Output("state1-choropleth", "style"),
    Output("state2-choropleth", "figure"),
    Output("state2-choropleth", "style"),
    Input("state1-dropdown", "value"),
    Input("state2-dropdown", "value"),
    Input("subcat-dropdown", "value"),
    Input("map-mode-dropdown", "value")
)
def update_choropleths(s1, s2, sub, mode):
    if not (s1 and s2 and sub and mode):
        empty, hid = go.Figure(), {"display":"none", "height": "50vh", "width": "100%"}
        return empty, hid, empty, hid

    def make_map(state_name):
        fname = state_name.lower().replace(" ", "-") + ".geojson"
        path = os.path.join(r"C:\Users\Vibha Narayan\OneDrive\Desktop\coding\GitDemo\CS661\Group Project\CS661_COURSE\censuscope", fname)
        if not os.path.exists(path):
            return go.Figure()
        with open(path) as f:
            gj = json.load(f)
        prop = next((k for k in gj["features"][0]["properties"] if "district" in k.lower()), None)
        if prop is None:
            return go.Figure()
        for feat in gj["features"]:
            raw = feat["properties"].get(prop, "")
            feat["id"] = str(raw).strip().upper()

        df = district_df[district_df["State name"]==state_name].copy()
        if sub not in df.columns:
            return go.Figure()
        df["value"] = pd.to_numeric(df[sub], errors='coerce')
        df["district_norm"] = df["district_norm"].str.upper()

        if mode == "max":
            keys = df.nlargest(1, "value")["district_norm"].tolist()
        elif mode == "min":
            keys = df.nsmallest(1, "value")["district_norm"].tolist()
        elif mode == "topbot":
            top = df.nlargest(5, "value")["district_norm"].tolist()
            bot = df.nsmallest(5, "value")["district_norm"].tolist()
            keys = top + bot
        else:
            m = df["value"].mean()
            df["diff"] = (df["value"] - m).abs()
            keys = df.nsmallest(5, "diff")["district_norm"].tolist()

        def lbl(d):
            if d in keys:
                if mode == "topbot":
                    return "Top 5" if d in df.nlargest(5,"value")["district_norm"].tolist() else "Bottom 5"
                return "Highlighted"
            return "Other"

        df["highlight"] = df["district_norm"].apply(lbl)
        cmap = {"Highlighted":"#00bfff","Top 5":"#00ff00","Bottom 5":"#ff4136","Other":"#444"}
        fig = px.choropleth(
            df, geojson=gj, locations="district_norm", featureidkey="id",
            color="highlight", color_discrete_map=cmap,
            scope="asia", title=f"{state_name}: {sub} ({mode})",
            height=500,
            width=900
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(
            margin={"r":0,"t":30,"l":0,"b":0},
            template="plotly_white",
            font=dict(color="#222"),
            legend=dict(font=dict(color="#222"))
        )
        return fig

    fig1, fig2 = make_map(s1), make_map(s2)
    style = {"display":"block","height":"50vh", "width": "100%"}
    return fig1, style, fig2, style

if __name__ == "__main__":
    app.run(debug=True)
