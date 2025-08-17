# ===========================================
# DISTRICT ANALYSIS CALLBACKS
# ===========================================

from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from data.loader import load_district_data
from utils.helpers import get_district_short_label
from config.settings import FONT_FAMILY, CSV_TO_GEOJSON_MAPPING, DISTRICT_ATTRIBUTE_CATEGORIES

def register_district_callbacks(app):
    """Register all district analysis callbacks"""
    
    # Load data
    district_data = load_district_data()
    
    # District state dropdown callback
    @app.callback(
        Output('district-state-dropdown', 'options'),
        [Input('tab-content', 'children')]
    )
    def update_district_state_dropdown(_):
        """Populate state dropdown for district analysis"""
        if district_data.empty:
            return []
        
        states = sorted(district_data['State name'].unique())
        return [{"label": state, "value": state} for state in states]

    # District attribute dropdown callback
    @app.callback(
        Output('district-attribute-dropdown', 'options'),
        [Input('district-state-dropdown', 'value')]
    )
    def update_district_attribute_dropdown(selected_state):
        """Update district attribute dropdown based on available data"""
        if not selected_state or district_data.empty:
            return []
        
        # Get all percentage columns available for the selected state
        state_data = district_data[district_data['State name'] == selected_state]
        available_cols = []
        
        for category, attributes in DISTRICT_ATTRIBUTE_CATEGORIES.items():
            category_attrs = []
            for attr in attributes:
                if attr in state_data.columns:
                    category_attrs.append({
                        "label": f"  {get_district_short_label(attr)}",
                        "value": attr
                    })
            
            if category_attrs:
                available_cols.append({
                    "label": f"📊 {category}",
                    "value": f"category_{category}",
                    "disabled": True
                })
                available_cols.extend(category_attrs)
        
        return available_cols

    # District map visualization callback
    @app.callback(
        Output('district-map', 'figure'),
        [Input('district-state-dropdown', 'value'),
         Input('district-attribute-dropdown', 'value')]
    )
    def update_district_map(selected_state, selected_attribute):
        """Create beautiful district-level choropleth map using statewise GeoJSON files"""
        
        if not selected_state:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="🗺️ District Map - Select a state to visualize",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#64748b",
                height=500,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                annotations=[
                    dict(
                        text="Choose a state to see beautiful district-level visualization! 🗺️📊",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=16, color="#94a3b8"),
                        showarrow=False
                    )
                ]
            )
            return placeholder_fig
        
        try:
            # Get state GeoJSON file name
            state_file_key = selected_state.lower().replace(' ', '_').replace('-', '_')
            geojson_file = CSV_TO_GEOJSON_MAPPING.get(state_file_key)
            
            if not geojson_file:
                # Show error for missing GeoJSON
                error_fig = go.Figure()
                error_fig.update_layout(
                    title=f"❌ No map data available for {selected_state}",
                    title_x=0.5,
                    title_font_size=18,
                    title_font_color="#ef4444",
                    height=500,
                    template="plotly_white",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_family=FONT_FAMILY,
                    annotations=[
                        dict(
                            text=f"District map data for {selected_state} is not available.<br>Please select a different state.",
                            xref="paper", yref="paper",
                            x=0.5, y=0.5,
                            xanchor='center', yanchor='middle',
                            font=dict(size=14, color="#ef4444"),
                            showarrow=False
                        )
                    ]
                )
                return error_fig
            
            # Load state-specific GeoJSON
            with open(geojson_file, 'r') as f:
                state_geo = json.load(f)
            
            # Get district data for selected state
            state_districts = district_data[district_data['State name'] == selected_state].copy()
            
            if selected_attribute and selected_attribute in state_districts.columns:
                # Create choropleth map with data
                district_map_fig = px.choropleth(
                    state_districts,
                    geojson=state_geo,
                    locations='District name',
                    color=selected_attribute,
                    featureidkey='properties.DISTRICT',
                    title=f"🗺️ {get_district_short_label(selected_attribute)} in {selected_state}",
                    color_continuous_scale="Viridis",
                    labels={selected_attribute: f"{get_district_short_label(selected_attribute)} (%)"},
                    hover_name='District name',
                    hover_data={selected_attribute: ':.1f'}
                )
            else:
                # Show district boundaries without data coloring
                dummy_data = state_districts[['District name']].copy()
                dummy_data['value'] = 1
                
                district_map_fig = px.choropleth(
                    dummy_data,
                    geojson=state_geo,
                    locations='District name',
                    color='value',
                    featureidkey='properties.DISTRICT',
                    title=f"🗺️ Districts of {selected_state} - Select an attribute to see data",
                    color_continuous_scale=["#e0f2fe", "#0369a1"],
                    hover_name='District name'
                )
            
            # Update map layout
            district_map_fig.update_geos(
                showframe=False,
                showcoastlines=False,
                projection_type='mercator',
                fitbounds="locations",
                bgcolor="rgba(0,0,0,0)"
            )
            
            district_map_fig.update_layout(
                title_x=0.5,
                title_font_size=20,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                margin=dict(l=0, r=0, t=60, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                coloraxis_showscale=True if selected_attribute else False
            )
            
            # Add beautiful hover template
            if selected_attribute:
                district_map_fig.update_traces(
                    hovertemplate="<b>%{hovertext}</b><br>" +
                                 f"{get_district_short_label(selected_attribute)}: %{{z:.1f}}%<br>" +
                                 "<extra></extra>",
                    marker_line_color="rgba(255,255,255,0.8)",
                    marker_line_width=0.5
                )
            else:
                district_map_fig.update_traces(
                    hovertemplate="<b>%{hovertext}</b><br>District of " + selected_state + "<extra></extra>",
                    marker_line_color="rgba(255,255,255,0.8)",
                    marker_line_width=0.5
                )
            
            return district_map_fig
            
        except Exception as e:
            print(f"Error creating district map: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"❌ Error loading district map for {selected_state}",
                title_x=0.5,
                height=500,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[
                    dict(
                        text=f"Error: {str(e)[:100]}...",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=14, color="#ef4444"),
                        showarrow=False
                    )
                ]
            )
            return error_fig

    # District rankings callback
    @app.callback(
        Output('district-rankings', 'figure'),
        [Input('district-state-dropdown', 'value'),
         Input('district-attribute-dropdown', 'value')]
    )
    def update_district_rankings(selected_state, selected_attribute):
        """Create beautiful district rankings visualization"""
        
        if not selected_state:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="🏆 District Rankings - Select a state to analyze",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#64748b",
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                annotations=[
                    dict(
                        text="Choose a state and metric to see district rankings! 🏆📊",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=16, color="#94a3b8"),
                        showarrow=False
                    )
                ]
            )
            return placeholder_fig
        
        try:
            # Get district data for selected state
            state_districts = district_data[district_data['State name'] == selected_state].copy()
            
            if selected_attribute and selected_attribute in state_districts.columns:
                # Sort districts by selected attribute
                rankings_data = state_districts[['District name', selected_attribute]].dropna()
                rankings_data = rankings_data.sort_values(selected_attribute, ascending=False)
                
                # Take top 15 districts for better visualization
                if len(rankings_data) > 15:
                    rankings_data = rankings_data.head(15)
                
                # Create color gradient based on performance
                colors = []
                max_val = rankings_data[selected_attribute].max()
                min_val = rankings_data[selected_attribute].min()
                
                for value in rankings_data[selected_attribute]:
                    normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
                    if normalized > 0.7:
                        colors.append('#10b981')  # Green for top performers
                    elif normalized > 0.4:
                        colors.append('#f59e0b')  # Amber for middle
                    else:
                        colors.append('#ef4444')  # Red for low performers
                
                # Create horizontal bar chart
                rankings_fig = go.Figure(data=[
                    go.Bar(
                        y=rankings_data['District name'],
                        x=rankings_data[selected_attribute],
                        orientation='h',
                        marker=dict(
                            color=colors,
                            line=dict(color='rgba(255,255,255,0.8)', width=1)
                        ),
                        hovertemplate="<b>%{y}</b><br>" +
                                     f"{get_district_short_label(selected_attribute)}: %{{x:.1f}}%<br>" +
                                     "<extra></extra>",
                        text=rankings_data[selected_attribute].round(1),
                        textposition='outside',
                        textfont=dict(size=10, color='#374151')
                    )
                ])
                
                rankings_fig.update_layout(
                    title=f"🏆 District Rankings: {get_district_short_label(selected_attribute)} in {selected_state}",
                    title_x=0.5,
                    title_font_size=16,
                    title_font_weight="bold",
                    title_font_color="#2d3748",
                    height=400,
                    margin=dict(l=120, r=50, t=60, b=50),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(248,250,252,0.8)',
                    font_family=FONT_FAMILY,
                    xaxis=dict(
                        title=f"{get_district_short_label(selected_attribute)} (%)",
                        title_font_size=12,
                        title_font_weight="bold",
                        title_font_color="#4a5568",
                        tickfont=dict(size=10, color="#6b7280"),
                        gridcolor="rgba(203,213,225,0.5)",
                        gridwidth=1,
                        showgrid=True
                    ),
                    yaxis=dict(
                        title="",
                        tickfont=dict(size=9, color="#374151"),
                        showgrid=False,
                        categoryorder='total ascending'
                    )
                )
                
            else:
                # Show placeholder for no attribute selected
                rankings_fig = go.Figure()
                rankings_fig.update_layout(
                    title=f"🏆 District Rankings for {selected_state} - Select a metric",
                    title_x=0.5,
                    title_font_size=16,
                    title_font_weight="bold",
                    title_font_color="#64748b",
                    height=400,
                    template="plotly_white",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_family=FONT_FAMILY,
                    annotations=[
                        dict(
                            text="Select a metric to see district rankings!",
                            xref="paper", yref="paper",
                            x=0.5, y=0.5,
                            xanchor='center', yanchor='middle',
                            font=dict(size=14, color="#94a3b8"),
                            showarrow=False
                        )
                    ]
                )
            
            return rankings_fig
            
        except Exception as e:
            print(f"Error in district rankings: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title="❌ Error loading district rankings",
                title_x=0.5,
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return error_fig

    # District scatter plot callback
    @app.callback(
        Output('district-scatter', 'figure'),
        [Input('district-state-dropdown', 'value'),
         Input('district-attribute-dropdown', 'value')]
    )
    def update_district_scatter(selected_state, selected_attribute):
        """Create district performance matrix scatter plot"""
        
        if not selected_state:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="📊 Performance Matrix - Select a state to analyze",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#64748b",
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                annotations=[
                    dict(
                        text="Choose a state to see district performance analysis! 📊",
                        xref="paper", yref="paper",
                        x=0.5, y=0.5,
                        xanchor='center', yanchor='middle',
                        font=dict(size=16, color="#94a3b8"),
                        showarrow=False
                    )
                ]
            )
            return placeholder_fig
        
        try:
            state_districts = district_data[district_data['State name'] == selected_state].copy()
            
            if selected_attribute and selected_attribute in state_districts.columns:
                # Create performance vs literacy scatter plot
                if 'Literate_%' in state_districts.columns:
                    scatter_fig = px.scatter(
                        state_districts,
                        x='Literate_%',
                        y=selected_attribute,
                        hover_name='District name',
                        title=f"📊 {get_district_short_label(selected_attribute)} vs Literacy in {selected_state}",
                        labels={
                            'Literate_%': 'Literacy Rate (%)',
                            selected_attribute: f"{get_district_short_label(selected_attribute)} (%)"
                        },
                        color=selected_attribute,
                        color_continuous_scale="Viridis",
                        size_max=15
                    )
                    
                    # Add trend line
                    scatter_fig.update_traces(
                        marker=dict(
                            size=12,
                            line=dict(width=2, color='white'),
                            opacity=0.8
                        ),
                        hovertemplate="<b>%{hovertext}</b><br>" +
                                     "Literacy: %{x:.1f}%<br>" +
                                     f"{get_district_short_label(selected_attribute)}: %{{y:.1f}}%<br>" +
                                     "<extra></extra>"
                    )
                    
                else:
                    # Create simple distribution plot
                    scatter_fig = px.strip(
                        state_districts,
                        y=selected_attribute,
                        hover_name='District name',
                        title=f"📊 {get_district_short_label(selected_attribute)} Distribution in {selected_state}",
                        labels={selected_attribute: f"{get_district_short_label(selected_attribute)} (%)"}
                    )
            else:
                # Show placeholder
                scatter_fig = go.Figure()
                scatter_fig.update_layout(
                    title=f"📊 Performance Matrix for {selected_state} - Select a metric",
                    title_x=0.5,
                    title_font_size=16,
                    title_font_weight="bold",
                    title_font_color="#64748b",
                    height=400,
                    template="plotly_white",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_family=FONT_FAMILY,
                    annotations=[
                        dict(
                            text="Select a metric to see performance analysis!",
                            xref="paper", yref="paper",
                            x=0.5, y=0.5,
                            xanchor='center', yanchor='middle',
                            font=dict(size=14, color="#94a3b8"),
                            showarrow=False
                        )
                    ]
                )
                return scatter_fig
            
            # Update layout
            scatter_fig.update_layout(
                title_x=0.5,
                title_font_size=16,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=400,
                margin=dict(l=50, r=50, t=60, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY
            )
            
            return scatter_fig
            
        except Exception as e:
            print(f"Error in district scatter: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title="❌ Error loading district analysis",
                title_x=0.5,
                height=400,
                template="plotly_white"
            )
            return error_fig

    # District summary table callback
    @app.callback(
        Output('district-summary-table', 'children'),
        [Input('district-state-dropdown', 'value'),
         Input('district-attribute-dropdown', 'value'),
         Input('district-search', 'value'),
         Input('district-table-limit', 'value')]
    )
    def update_district_summary_table(selected_state, selected_attribute, search_term, limit):
        """Create beautiful interactive district summary table"""
        
        if not selected_state:
            return html.Div([
                html.Div([
                    html.Div("📋", style={
                        'fontSize': '4rem',
                        'textAlign': 'center',
                        'marginBottom': '1rem',
                        'opacity': '0.3',
                        'color': '#94a3b8'
                    }),
                    html.H3("Select a state to view district data table", style={
                        'textAlign': 'center',
                        'color': '#64748b',
                        'fontWeight': '500',
                        'margin': '0'
                    }),
                    html.P("Choose a state and attribute to see sortable district data!", style={
                        'textAlign': 'center',
                        'color': '#94a3b8',
                        'marginTop': '0.5rem'
                    })
                ], style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'height': '300px'
                })
            ])
        
        try:
            # Filter data for selected state
            state_districts = district_data[district_data['State name'] == selected_state].copy()
            
            if state_districts.empty:
                return html.Div([
                    html.H3("❌ No data available for selected state", style={
                        'textAlign': 'center', 
                        'color': '#ef4444',
                        'margin': '2rem 0'
                    })
                ])
            
            # Apply search filter if provided
            if search_term:
                state_districts = state_districts[
                    state_districts['District name'].str.contains(search_term, case=False, na=False)
                ]
            
            # Select key columns for the table
            display_columns = ['District name']
            
            # Add selected attribute if available
            if selected_attribute and selected_attribute in state_districts.columns:
                display_columns.append(selected_attribute)
            
            # Add other important columns available in the data
            additional_cols = []
            for col in ['Literate_%', 'Workers_%', 'Male_%', 'Female_%']:
                if col in state_districts.columns and col not in display_columns:
                    additional_cols.append(col)
            
            # Limit additional columns to keep table manageable
            display_columns.extend(additional_cols[:5])
            
            # Filter and sort data
            table_data = state_districts[display_columns].copy()
            
            # Sort by selected attribute if available, otherwise by literacy
            if selected_attribute and selected_attribute in table_data.columns:
                table_data = table_data.sort_values(selected_attribute, ascending=False)
            elif 'Literate_%' in table_data.columns:
                table_data = table_data.sort_values('Literate_%', ascending=False)
            
            # Apply limit
            if limit and limit < len(table_data):
                table_data = table_data.head(limit)
            
            # Create table headers with beautiful styling
            table_headers = []
            for col in display_columns:
                if col == 'District name':
                    header_text = "District"
                elif col.endswith('_%'):
                    header_text = get_district_short_label(col)
                else:
                    header_text = col.replace('_', ' ').title()
                
                table_headers.append(
                    html.Th(header_text, style={
                        'background': 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                        'color': 'white',
                        'padding': '12px 16px',
                        'textAlign': 'left',
                        'fontWeight': '600',
                        'fontSize': '14px',
                        'borderBottom': '2px solid #e2e8f0',
                        'position': 'sticky',
                        'top': '0',
                        'zIndex': '10'
                    })
                )
            
            # Create table rows with beautiful styling and performance indicators
            table_rows = []
            for idx, (_, row) in enumerate(table_data.iterrows()):
                cells = []
                
                for col_idx, col in enumerate(display_columns):
                    if col == 'District name':
                        # District name with icon
                        cell_content = html.Div([
                            html.Span("📍", style={'marginRight': '0.5rem', 'fontSize': '0.9rem'}),
                            html.Strong(str(row[col]))
                        ], style={'display': 'flex', 'alignItems': 'center'})
                    else:
                        # Numeric values with performance indicators
                        value = row[col]
                        if pd.notna(value):
                            # Performance color coding
                            if value >= 80:
                                bg_color = 'rgba(16, 185, 129, 0.1)'  # Green background
                                text_color = '#059669'
                                icon = '🟢'
                            elif value >= 60:
                                bg_color = 'rgba(245, 158, 11, 0.1)'  # Yellow background
                                text_color = '#d97706'
                                icon = '🟡'
                            else:
                                bg_color = 'rgba(239, 68, 68, 0.1)'  # Red background
                                text_color = '#dc2626'
                                icon = '🔴'
                            
                            cell_content = html.Div([
                                html.Span(icon, style={'marginRight': '0.5rem', 'fontSize': '0.8rem'}),
                                html.Span(f"{value:.1f}%", style={'fontWeight': '600', 'color': text_color})
                            ], style={
                                'display': 'flex', 
                                'alignItems': 'center',
                                'background': bg_color,
                                'padding': '4px 8px',
                                'borderRadius': '6px',
                                'width': 'fit-content'
                            })
                        else:
                            cell_content = html.Span("N/A", style={'color': '#94a3b8', 'fontStyle': 'italic'})
                    
                    cells.append(html.Td(cell_content, style={
                        'padding': '12px 16px',
                        'fontSize': '13px',
                        'borderBottom': '1px solid #e2e8f0'
                    }))
                
                # Alternate row colors for better readability
                row_style = {
                    'backgroundColor': '#f8fafc' if idx % 2 == 0 else 'white',
                    'transition': 'background-color 0.2s ease',
                    'cursor': 'pointer'
                }
                
                table_rows.append(
                    html.Tr(cells, style=row_style, className="table-row")
                )
            
            # Create the complete table
            data_table = html.Table([
                html.Thead(html.Tr(table_headers)),
                html.Tbody(table_rows)
            ], style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'fontSize': '14px',
                'fontFamily': FONT_FAMILY,
                'boxShadow': '0 1px 3px rgba(0, 0, 0, 0.1)',
                'borderRadius': '8px',
                'overflow': 'hidden'
            })
            
            # Add summary statistics
            total_districts = len(table_data)
            if selected_attribute and selected_attribute in table_data.columns:
                avg_value = table_data[selected_attribute].mean()
                best_district = table_data.iloc[0]['District name']
                best_value = table_data.iloc[0][selected_attribute]
                
                summary_stats = html.Div([
                    html.Div([
                        html.Span("📊", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                        html.Strong(f"Showing {total_districts} districts")
                    ], style={'marginBottom': '0.5rem'}),
                    
                    html.Div([
                        html.Span("🏆", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                        html.Strong(f"Best: {best_district} ({best_value:.1f}%)")
                    ], style={'marginBottom': '0.5rem'}),
                    
                    html.Div([
                        html.Span("📈", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                        html.Strong(f"Average: {avg_value:.1f}%")
                    ])
                ], style={
                    'background': 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
                    'padding': '1rem',
                    'borderRadius': '8px',
                    'marginBottom': '1rem',
                    'fontSize': '14px',
                    'color': '#0369a1',
                    'border': '1px solid #bae6fd'
                })
            else:
                summary_stats = html.Div([
                    html.Div([
                        html.Span("📊", style={'fontSize': '1.2rem', 'marginRight': '0.5rem'}),
                        html.Strong(f"Showing {total_districts} districts in {selected_state}")
                    ])
                ], style={
                    'background': 'linear-gradient(135deg, #f0f9ff, #e0f2fe)',
                    'padding': '1rem',
                    'borderRadius': '8px',
                    'marginBottom': '1rem',
                    'fontSize': '14px',
                    'color': '#0369a1',
                    'border': '1px solid #bae6fd'
                })
            
            return html.Div([
                summary_stats,
                data_table
            ])
            
        except Exception as e:
            print(f"Error creating district summary table: {e}")
            return html.Div([
                html.H3("❌ Error loading district table", style={
                    'textAlign': 'center', 
                    'color': '#ef4444',
                    'margin': '2rem 0'
                }),
                html.P(f"Error: {str(e)}", style={
                    'textAlign': 'center',
                    'color': '#94a3b8',
                    'fontSize': '12px'
                })
            ])

    print("✅ District analysis callbacks registered successfully!")
