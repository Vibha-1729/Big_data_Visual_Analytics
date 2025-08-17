import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Output, Input
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from scipy.stats import pearsonr, spearmanr
import webbrowser
# --- Data Loading ---
# Change these paths to your actual data locations!
district_df = pd.read_excel(
    r"C:\Users\aadya\OneDrive\Desktop\CS661_COURSE\censuscope\india-districts-census-2011.xlsx",
    sheet_name="india-districts-census-2011"
)
state_df = pd.read_excel(
    r"C:\Users\aadya\OneDrive\Desktop\CS661_COURSE\censuscope\statewise_aggregated_data.xlsx"
)

# List of unique states
states = state_df["State name"].unique()

# List of numeric attributes for dropdowns
numeric_cols = [
    col for col in district_df.columns
    if district_df[col].dtype in [np.float64, np.int64]
    and col not in ["Srl No", "District code", "State code"]  # skip ID cols
]

# Dash app instance
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# --- Layout ---
app.layout = dbc.Container([
    html.Br(),
    dbc.Row(dbc.Col([
        html.H4("Correlation Comparison: District Data for Two States", style={"margin-bottom": "16px"}),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="state1-dropdown",
                options=[{"label": s, "value": s} for s in states],
                placeholder="Select first state",
                style={"margin-bottom": "12px"}
            ), width=6),
            dbc.Col(dcc.Dropdown(
                id="state2-dropdown",
                options=[{"label": s, "value": s} for s in states],
                placeholder="Select second state",
                style={"margin-bottom": "12px"}
            ), width=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="x-attribute-dropdown",
                options=[{"label": col, "value": col} for col in numeric_cols],
                placeholder="Select X attribute (e.g. Literacy Rate)",
                style={"margin-bottom": "12px"}
            ), width=6),
            dbc.Col(dcc.Dropdown(
                id="y-attribute-dropdown",
                options=[{"label": col, "value": col} for col in numeric_cols],
                placeholder="Select Y attribute (e.g. Female_Workers)",
                style={"margin-bottom": "12px"}
            ), width=6),
        ]),
        dcc.Graph(id="state-comparison-corrscatter", config={"displayModeBar": True}, style={"height": "500px"}),
        html.Br(),
        html.H5("Top Districts Closest to Regression Line"),
        dbc.Row([
            dbc.Col([
                html.H6(id="state1-table-title", style={"text-align": "center"}),
                html.Div(id="top-districts-table-1")
            ], width=6),
            dbc.Col([
                html.H6(id="state2-table-title", style={"text-align": "center"}),
                html.Div(id="top-districts-table-2")
            ], width=6),
        ])
    ], width=12)),
], fluid=True)

# --- Callback for Correlation Scatter ---
@app.callback(
    Output("state-comparison-corrscatter", "figure"),
    Output("state1-table-title", "children"),
    Output("top-districts-table-1", "children"),
    Output("state2-table-title", "children"),
    Output("top-districts-table-2", "children"),
    Input("state1-dropdown", "value"),
    Input("state2-dropdown", "value"),
    Input("x-attribute-dropdown", "value"),
    Input("y-attribute-dropdown", "value"),
)
def update_corr_scatter(state1, state2, x_col, y_col):
    # --- Validation ---
    if not (state1 and state2 and x_col and y_col):
        return go.Figure(), "", "", "", ""

    # --- Prepare Data ---
    df1 = district_df[district_df["State name"] == state1].copy()
    df2 = district_df[district_df["State name"] == state2].copy()
    df1 = df1.dropna(subset=[x_col, y_col])
    df2 = df2.dropna(subset=[x_col, y_col])

    # --- Correlation, Regression, Residuals ---
    if len(df1) > 1:
        pearson1 = pearsonr(df1[x_col], df1[y_col])[0]
        spearman1 = spearmanr(df1[x_col], df1[y_col])[0]
        m1, c1 = np.polyfit(df1[x_col], df1[y_col], 1)
        df1["y_pred"] = m1 * df1[x_col] + c1
        df1["residual"] = np.abs(df1[y_col] - df1["y_pred"])
    else:
        pearson1 = spearman1 = m1 = c1 = None
        df1["y_pred"] = df1["residual"] = np.nan

    if len(df2) > 1:
        pearson2 = pearsonr(df2[x_col], df2[y_col])[0]
        spearman2 = spearmanr(df2[x_col], df2[y_col])[0]
        m2, c2 = np.polyfit(df2[x_col], df2[y_col], 1)
        df2["y_pred"] = m2 * df2[x_col] + c2
        df2["residual"] = np.abs(df2[y_col] - df2["y_pred"])
    else:
        pearson2 = spearman2 = m2 = c2 = None
        df2["y_pred"] = df2["residual"] = np.nan

    # --- Scatter Plot ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df1[x_col], y=df1[y_col],
        mode='markers', name=state1,
        marker=dict(color='blue', size=9, opacity=0.8, line=dict(width=1, color='white')),
        text=df1["District name"],
        hovertemplate='<b>%{text}</b><br>' + x_col + ': %{x}<br>' + y_col + ': %{y}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=df2[x_col], y=df2[y_col],
        mode='markers', name=state2,
        marker=dict(color='orange', size=9, opacity=0.8, line=dict(width=1, color='white')),
        text=df2["District name"],
        hovertemplate='<b>%{text}</b><br>' + x_col + ': %{x}<br>' + y_col + ': %{y}<extra></extra>'
    ))

    # --- Trend Lines ---
    if len(df1) > 1:
        x_line1 = np.linspace(df1[x_col].min(), df1[x_col].max(), 50)
        y_line1 = m1 * x_line1 + c1
        fig.add_trace(go.Scatter(x=x_line1, y=y_line1, mode='lines', name=f"{state1} Trend", line=dict(color='blue', dash='dash')))
    if len(df2) > 1:
        x_line2 = np.linspace(df2[x_col].min(), df2[x_col].max(), 50)
        y_line2 = m2 * x_line2 + c2
        fig.add_trace(go.Scatter(x=x_line2, y=y_line2, mode='lines', name=f"{state2} Trend", line=dict(color='orange', dash='dash')))

    # --- Layout ---
    fig.update_layout(
        template="plotly_white",
        title=f"<b>{x_col} vs {y_col} (District-level)</b><br>"
              f"<span style='color:blue'>{state1}</span> (Pearson: {pearson1:.2f}, Spearman: {spearman1:.2f}) &nbsp; | &nbsp; "
              f"<span style='color:orange'>{state2}</span> (Pearson: {pearson2:.2f}, Spearman: {spearman2:.2f})",
        xaxis_title=x_col,
        yaxis_title=y_col,
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )

    # --- Top Districts Closest to Regression Line ---
    if len(df1) > 0 and "residual" in df1.columns:
        top1 = df1.nsmallest(5, "residual")[["District name", x_col, y_col]]
        table1 = dbc.Table.from_dataframe(top1, striped=True, bordered=True, hover=True)
        table1_title = f"Top 5 {state1} Districts"
    else:
        table1 = html.Div("Not enough data.")
        table1_title = ""

    if len(df2) > 0 and "residual" in df2.columns:
        top2 = df2.nsmallest(5, "residual")[["District name", x_col, y_col]]
        table2 = dbc.Table.from_dataframe(top2, striped=True, bordered=True, hover=True)
        table2_title = f"Top 5 {state2} Districts"
    else:
        table2 = html.Div("Not enough data.")
        table2_title = ""

    return fig, table1_title, table1, table2_title, table2

# --- Run App ---
if __name__ == "_main_":
    webbrowser.open("http://127.0.0.1:8050/")
    app.run_server(debug=True)