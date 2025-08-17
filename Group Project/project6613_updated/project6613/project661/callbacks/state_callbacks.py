# ===========================================
# STATE ANALYSIS CALLBACKS
# ===========================================

from dash import Input, Output, callback_context
from dash.dependencies import State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from data.loader import load_state_data, load_geojson_data
from utils.helpers import get_short_label
from utils.insights import generate_insights, create_insights_layout
from config.settings import FONT_FAMILY, STATE_NAME_MAPPING, ATTRIBUTE_CATEGORIES

def register_state_callbacks(app):
    """Register all state analysis callbacks"""
    
    # Load data
    state_data = load_state_data()
    india_geo = load_geojson_data()
    print("DEBUG: Loaded state_data shape:", state_data.shape)
    print("DEBUG: Loaded india_geo features:", len(india_geo.get('features', [])))
    
    # Category to attribute dropdown callback
    @app.callback(
        Output('attribute-dropdown', 'options'),
        [Input('category-dropdown', 'value')]
    )
    def update_attribute_dropdown(selected_category):
        """Update attribute dropdown based on selected category"""
        if not selected_category:
            return []
        
        attributes = ATTRIBUTE_CATEGORIES.get(selected_category, [])
        print("DEBUG: Available attributes for category", selected_category, ":", attributes)
        print("DEBUG: State data columns:", state_data.columns)
        print([col for col in state_data.columns if "christ" in col.lower()])
        return [{"label": get_short_label(attr), "value": attr} for attr in attributes]
    

    # India Map visualization callback
    @app.callback(
        Output('india-map', 'figure'),
        [Input('attribute-dropdown', 'value')]
    )
    def update_india_map(selected_attribute):
        print("DEBUG: update_india_map called with selected_attribute:", selected_attribute)
        """Update India choropleth map based on selected attribute"""
        print("DEBUG: Unique states in state_data:", state_data['State name'].unique())
        # Show default India map if no attribute selected
        if not selected_attribute:
            try:
                print("DEBUG: No attribute selected, showing default map.")
                # Create dummy data for all states to show boundaries
                state_names = []
                for feature in india_geo['features']:
                    state_names.append(feature['properties']['name'])
                
                # Create DataFrame with uniform values to show all states
                dummy_data = pd.DataFrame({
                    'state': state_names,
                    'value': [1] * len(state_names)
                })
                
                # Create beautiful default map with gradient colors
                default_fig = px.choropleth(
                    dummy_data,
                    geojson=india_geo,
                    locations='state',
                    color='value',
                    featureidkey='properties.name',
                    title="🗺️ India Map - Select an attribute to see beautiful data visualization",
                    color_continuous_scale=["#e0f2fe", "#0369a1", "#1e40af"],
                    labels={'value': 'States'}
                )
                
                default_fig.update_geos(
                    showframe=False,
                    showcoastlines=True,
                    coastlinecolor="rgba(255,255,255,0.9)",
                    coastlinewidth=1.2,
                    projection_type='natural earth',
                    fitbounds="locations",
                    bgcolor="rgba(0,0,0,0)"
                )
                
                default_fig.update_layout(
                    title_x=0.5,
                    title_font_size=20,
                    title_font_weight="bold",
                    title_font_color="#2d3748",
                    height=500,
                    margin=dict(l=0, r=0, t=60, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_family=FONT_FAMILY,
                    coloraxis_showscale=False
                )
                
                # Add beautiful state borders
                default_fig.update_traces(
                    marker_line_color="rgba(255,255,255,0.9)",
                    marker_line_width=1.2,
                    text=dummy_data["state"],
                    hovertemplate="<b>%{text}</b><br><span style='white-space:nowrap;'>Click to explore data</span><extra></extra>",
                    hoverlabel=dict(
                        bgcolor="rgba(0, 0, 0, 0.75)",   # Semi-transparent black background
                        font_color="white", 
                        font_size=14
                    )
                )
                # print(dummy_data["state"].head())
                return default_fig

            except Exception as e:
                print(f"Error creating default India map: {e}")
                # Fallback to simple figure
                fallback_fig = go.Figure()
                fallback_fig.update_layout(
                    title="🗺️ India Map Loading...",
                    title_x=0.5,
                    title_font_size=18,
                    height=500,
                    template="plotly_white",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                return fallback_fig
        
        try:
            print("DEBUG: Attribute selected, preparing choropleth for:", selected_attribute)
            # Prepare data for visualization
            # viz_data = state_data[['State name', selected_attribute]].dropna()
            viz_data = state_data[['State name', selected_attribute]].dropna()
            viz_data = viz_data.groupby('State name')[selected_attribute].mean().reset_index()
            
            # Map CSV state names to GeoJSON state names for choropleth
            viz_data['Mapped_State'] = viz_data['State name'].map(STATE_NAME_MAPPING)
            viz_data = viz_data.dropna(subset=['Mapped_State'])  # Remove states not in mapping
            
            # Beautiful India Choropleth Map with enhanced styling
            india_map_fig = px.choropleth(
                viz_data,
                geojson=india_geo,
                locations='Mapped_State',
                color=selected_attribute,
                featureidkey='properties.name',
                title=f"🗺️ {get_short_label(selected_attribute)} Across Indian States",
                color_continuous_scale="RdYlBu_r",  # Beautiful red-yellow-blue gradient (reversed)
                color_continuous_midpoint=viz_data[selected_attribute].median(skipna=True),
                labels={selected_attribute: f"{get_short_label(selected_attribute)} (%)"},
                hover_name='State name',  # Show original state name on hover
                hover_data={selected_attribute: ':.1f', 'Mapped_State': False}
            )
            
            india_map_fig.update_geos(
                showframe=False,
                showcoastlines=True,
                coastlinecolor="rgba(255,255,255,0.8)",
                coastlinewidth=1,
                projection_type='natural earth',
                fitbounds="locations",
                bgcolor="rgba(0,0,0,0)"
            )
            
            # Enhanced layout with beautiful styling
            india_map_fig.update_layout(
                title_x=0.5,
                title_font_size=20,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                margin=dict(l=0, r=0, t=60, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                coloraxis_colorbar=dict(
                    title=f"{get_short_label(selected_attribute)} (%)",
                    title_font_size=14,
                    title_font_weight="bold",
                    title_font_color="#2d3748",
                    tickfont_size=11,
                    tickfont_color="#4a5568",
                    len=0.8,
                    thickness=15,
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="rgba(0,0,0,0.1)",
                    borderwidth=1,
                    x=1.02
                )
            )
            
            # Add beautiful hover template
            india_map_fig.update_traces(
                hovertemplate="<b>%{hovertext}</b><br>" +
                             f"{get_short_label(selected_attribute)}: %{{z:.1f}}%<br>" +
                             "<extra></extra>",
                marker_line_color="rgba(255,255,255,0.8)",
                marker_line_width=0.8,
                zmin=viz_data[selected_attribute].min(skipna=True),
                zmax=viz_data[selected_attribute].max(skipna=True),
            )
            
            return india_map_fig
            
        except Exception as e:
            print(f"Error in the India map visualization: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"❌ Error loading India map for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
                title_x=0.5,
                height=500,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return error_fig

    # State Rankings visualization callback
    @app.callback(
        Output('state-rankings', 'figure'),
        [Input('attribute-dropdown', 'value')]
    )
    def update_state_rankings(selected_attribute):
        """Create beautiful state rankings bar chart"""
        
        # Show placeholder if no attribute selected
        if not selected_attribute:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="🏆 State Rankings - Select an attribute to see rankings",
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
                        text="Choose a category and attribute to see beautiful state rankings! 📊",
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
            # Prepare data for rankings
            rankings_data = state_data[['State name', selected_attribute]].dropna()
            rankings_data = rankings_data.groupby('State name')[selected_attribute].mean().reset_index()
            rankings_data = rankings_data.sort_values(selected_attribute, ascending=False).reset_index(drop=True)
            
            # Take top 15 and bottom 5 states for better visualization
            if len(rankings_data) > 20:
                top_states = rankings_data.head(15)
                bottom_states = rankings_data.tail(5)
                display_data = pd.concat([top_states, bottom_states], ignore_index=True)
            else:
                display_data = rankings_data
            
            # Create beautiful color gradient based on ranking
            colors = []
            max_val = display_data[selected_attribute].max()
            min_val = display_data[selected_attribute].min()
            
            for value in display_data[selected_attribute]:
                # Normalize value between 0 and 1
                normalized = (value - min_val) / (max_val - min_val) if max_val != min_val else 0.5
                
                # Create color gradient from red (low) to green (high)
                if normalized > 0.7:
                    colors.append('#10b981')  # Green for top performers
                elif normalized > 0.4:
                    colors.append('#f59e0b')  # Amber for middle
                else:
                    colors.append('#ef4444')  # Red for low performers
            
            # Create horizontal bar chart
            rankings_fig = go.Figure(data=[
                go.Bar(
                    y=display_data['State name'],
                    x=display_data[selected_attribute],
                    orientation='h',
                    marker=dict(
                        color=colors,
                        line=dict(color='rgba(255,255,255,0.8)', width=1),
                        pattern=dict(
                            shape="", 
                            size=8, 
                            solidity=0.3
                        )
                    ),
                    hovertemplate="<b>%{y}</b><br>" +
                                 f"{get_short_label(selected_attribute)}: %{{x:.1f}}%<br>" +
                                 "<extra></extra>",
                    text=display_data[selected_attribute].round(1),
                    textposition='outside',
                    textfont=dict(size=11, color='#374151')
                )
            ])
            
            # Beautiful styling for rankings chart
            rankings_fig.update_layout(
                title=f"🏆 State Rankings: {get_short_label(selected_attribute)}",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=500,
                margin=dict(l=150, r=50, t=60, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY,
                xaxis=dict(
                    title=f"{get_short_label(selected_attribute)} (%)",
                    title_font_size=14,
                    title_font_weight="bold",
                    title_font_color="#4a5568",
                    tickfont=dict(size=11, color="#6b7280"),
                    gridcolor="rgba(203,213,225,0.5)",
                    gridwidth=1,
                    showgrid=True,
                    zeroline=True,
                    zerolinecolor="rgba(107,114,128,0.3)",
                    zerolinewidth=2
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=11, color="#374151"),
                    showgrid=False,
                    categoryorder='total ascending'  # Order by value
                ),
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="rgba(0,0,0,0.1)",
                    font_size=12,
                    font_family=FONT_FAMILY
                )
            )
            
            # Add subtle background gradient
            rankings_fig.add_shape(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                fillcolor="rgba(248,250,252,0.3)",
                layer="below",
                line_width=0
            )
            
            return rankings_fig
            
        except Exception as e:
            print(f"Error in state rankings visualization: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"❌ Error loading rankings for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
                title_x=0.5,
                height=500,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return error_fig

    # Box Plot Distribution visualization callback
    @app.callback(
        Output('box-plot', 'figure'),
        [Input('attribute-dropdown', 'value')]
    )
    def update_box_plot(selected_attribute):
        """Create beautiful box plot for distribution analysis"""
        
        # Show placeholder if no attribute selected
        if not selected_attribute:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="📦 Distribution Summary - Select an attribute to analyze",
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
                        text="Choose a category and attribute to see distribution analysis! 📊",
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
            # Prepare data for box plot
            box_data = state_data[['State name', selected_attribute]].dropna()
            box_data = box_data.groupby('State name')[selected_attribute].mean().reset_index()
            
            # Create beautiful box plot
            box_fig = go.Figure()
            
            # Add the box plot
            box_fig.add_trace(go.Box(
                y=box_data[selected_attribute],
                name=get_short_label(selected_attribute),
                boxpoints='all',  # Show all points
                jitter=0.3,      # Spread points horizontally
                pointpos=-1.8,   # Position points to the left
                marker=dict(
                    color='rgba(99, 102, 241, 0.6)',  # Primary color with transparency
                    size=8,
                    line=dict(color='rgba(99, 102, 241, 0.8)', width=1)
                ),
                line=dict(color='rgba(45, 55, 72, 0.8)', width=2),
                fillcolor='rgba(99, 102, 241, 0.1)',
                hoveron='boxes+points',
                hovertemplate="<b>%{y:.1f}%</b><extra></extra>"
            ))
            
            # Calculate statistics for annotations
            q1 = box_data[selected_attribute].quantile(0.25)
            median = box_data[selected_attribute].median()
            q3 = box_data[selected_attribute].quantile(0.75)
            mean_val = box_data[selected_attribute].mean()
            std_val = box_data[selected_attribute].std()
            
            # Beautiful styling for box plot
            box_fig.update_layout(
                title=f"📦 Distribution: {get_short_label(selected_attribute)}",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=400,
                margin=dict(l=50, r=50, t=60, b=50),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(248,250,252,0.8)',
                font_family=FONT_FAMILY,
                showlegend=False,
                yaxis=dict(
                    title=f"{get_short_label(selected_attribute)} (%)",
                    title_font_size=14,
                    title_font_weight="bold",
                    title_font_color="#4a5568",
                    tickfont=dict(size=11, color="#6b7280"),
                    gridcolor="rgba(203,213,225,0.5)",
                    gridwidth=1,
                    showgrid=True,
                    zeroline=False
                ),
                xaxis=dict(
                    showgrid=False,
                    showticklabels=False,
                    zeroline=False
                )
            )
            
            # Add statistics annotations
            box_fig.add_annotation(
                xref="paper", yref="y",
                x=0.02, y=mean_val,
                text=f"Mean: {mean_val:.1f}%",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#10b981",
                font=dict(size=12, color="#059669", weight="bold"),
                bgcolor="rgba(240, 253, 244, 0.8)",
                bordercolor="#10b981",
                borderwidth=1
            )
            
            box_fig.add_annotation(
                xref="paper", yref="y",
                x=0.98, y=median,
                text=f"Median: {median:.1f}%",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#f59e0b",
                font=dict(size=12, color="#d97706", weight="bold"),
                bgcolor="rgba(254, 243, 199, 0.8)",
                bordercolor="#f59e0b",
                borderwidth=1
            )
            
            return box_fig
            
        except Exception as e:
            print(f"Error in box plot visualization: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"❌ Error loading distribution for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
                title_x=0.5,
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return error_fig

    # Top States Pie Chart visualization callback
    @app.callback(
        Output('top-states-pie', 'figure'),
        [Input('attribute-dropdown', 'value')]
    )
    def update_top_states_pie(selected_attribute):
        """Create beautiful pie chart showing top 7 performing states"""
        
        # Show placeholder if no attribute selected
        if not selected_attribute:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="🥧 Top 7 States - Select an attribute to see leaders",
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
                        text="Choose a category and attribute to see top performing states! 🏆",
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
            # Prepare data for pie chart
            pie_data = state_data[['State name', selected_attribute]].dropna()
            pie_data = pie_data.groupby('State name')[selected_attribute].mean().reset_index()
            
            # Get top 7 states
            top_states = pie_data.nlargest(7, selected_attribute)
            
            # Calculate "Others" category for remaining states
            remaining_states = pie_data[~pie_data['State name'].isin(top_states['State name'])]
            others_total = remaining_states[selected_attribute].sum() if len(remaining_states) > 0 else 0
            
            # Create beautiful color palette for pie chart
            colors = [
                '#6366f1',  # Primary indigo
                '#ec4899',  # Pink
                '#10b981',  # Emerald
                '#f59e0b',  # Amber
                '#ef4444',  # Red
                '#8b5cf6',  # Purple
                '#06b6d4',  # Cyan
                '#64748b'   # Gray for others
            ]
            
            # Prepare labels and values
            labels = top_states['State name'].tolist()
            values = top_states[selected_attribute].tolist()
            
            # Add "Others" if there are remaining states
            if others_total > 0:
                labels.append(f"Others ({len(remaining_states)} states)")
                values.append(others_total)
            
            # Create beautiful pie chart
            pie_fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.4,  # Create a donut chart
                marker=dict(
                    colors=colors[:len(labels)],
                    line=dict(color='white', width=3)
                ),
                textinfo='label+percent',
                textposition='auto',
                textfont=dict(size=11, color='white', weight='bold'),
                hovertemplate="<b>%{label}</b><br>" +
                             f"{get_short_label(selected_attribute)}: %{{value:.1f}}%<br>" +
                             "Share: %{percent}<br>" +
                             "<extra></extra>",
                pull=[0.05 if i == 0 else 0 for i in range(len(labels))]  # Slightly separate the top state
            )])
            
            # Beautiful styling for pie chart
            pie_fig.update_layout(
                title=f"🥧 Top 7 States: {get_short_label(selected_attribute)}",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=400,
                margin=dict(l=20, r=20, t=60, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05,
                    font=dict(size=10, color="#374151"),
                    bgcolor="rgba(248,250,252,0.8)",
                    bordercolor="rgba(203,213,225,0.5)",
                    borderwidth=1
                )
            )
            
            # Add center annotation for donut chart
            total_avg = pie_data[selected_attribute].mean()
            pie_fig.add_annotation(
                text=f"<b>Avg</b><br>{total_avg:.1f}%",
                x=0.5, y=0.5,
                font=dict(size=16, color="#2d3748", weight="bold"),
                showarrow=False,
                align="center"
            )
            
            # Add subtle background
            pie_fig.add_shape(
                type="circle",
                xref="paper", yref="paper",
                x0=0.1, y0=0.1, x1=0.9, y1=0.9,
                fillcolor="rgba(248,250,252,0.3)",
                layer="below",
                line_width=0
            )
            
            return pie_fig
            
        except Exception as e:
            print(f"Error in pie chart visualization: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title=f"❌ Error loading top states for {get_short_label(selected_attribute) if selected_attribute else 'visualization'}",
                title_x=0.5,
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return error_fig

    # Insights visualization callback
    @app.callback(
        Output('insights-content', 'children'),
        [Input('attribute-dropdown', 'value')]
    )
    def update_insights_card(selected_attribute):
        """Create beautiful insights card with key statistics and observations"""
        
        if not selected_attribute:
            return create_insights_layout([], None)
        
        # Generate insights
        insights = generate_insights(selected_attribute, state_data)
        
        # Create layout
        return create_insights_layout(insights, selected_attribute)

    # Correlation Heatmap visualization callback
    @app.callback(
        Output('correlation-heatmap', 'figure'),
        [Input('attribute-dropdown', 'value')]
    )
    def update_correlation_heatmap(selected_attribute):
        """Create beautiful correlation heatmap showing relationships between demographic attributes"""
        
        # Show placeholder if no attribute selected
        if not selected_attribute:
            placeholder_fig = go.Figure()
            placeholder_fig.update_layout(
                title="🔥 Correlation Heatmap - Select an attribute to see relationships",
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
                        text="Choose an attribute to see stunning correlation analysis! 🔥📊",
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
            # Select key demographic metrics for correlation analysis
            correlation_metrics = [
                'Total_Literate_pct',
                'Worker_pct',
                'HouseholdAssets_Computer_pct',
                'HouseholdAssets_Internet_pct',
                'HouseholdAmenities_ElectricityConnection_pct',
                'HouseholdAmenities_CleanFuel_pct',
                'HouseholdAmenities_DrinkingWaterTreated_pct',
                'HouseholdAmenities_Flush_latrine_connected_to_piped_sewer_system_pct',
                'Total_Male_pct',
                'Total_Female_pct'
            ]
            
            # Filter available metrics based on what exists in the data
            available_metrics = [metric for metric in correlation_metrics if metric in state_data.columns]
            
            # If not enough metrics, add more from available columns
            if len(available_metrics) < 8:
                numeric_cols = [col for col in state_data.columns 
                              if col != 'State name' and state_data[col].dtype in ['float64', 'int64'] 
                              and col not in available_metrics]
                available_metrics.extend(numeric_cols[:12-len(available_metrics)])
            
            # Take 8-10 metrics for clean heatmap
            final_metrics = available_metrics[:10]
            
            # Ensure selected attribute is included
            if selected_attribute not in final_metrics:
                final_metrics = [selected_attribute] + final_metrics[:9]
            
            # Prepare correlation data
            corr_data = state_data[['State name'] + final_metrics].dropna()
            corr_data = corr_data.groupby('State name').mean().reset_index()
            
            # Calculate correlation matrix
            correlation_matrix = corr_data[final_metrics].corr()
            
            # Create short labels for better readability
            short_labels = [get_short_label(metric) for metric in final_metrics]
            
            # Create beautiful correlation heatmap
            heatmap_fig = go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=short_labels,
                y=short_labels,
                colorscale=[
                    [0, '#ef4444'],      # Strong negative correlation - Red
                    [0.25, '#f97316'],   # Moderate negative - Orange  
                    [0.4, '#fbbf24'],    # Weak negative - Yellow
                    [0.5, '#f8fafc'],    # No correlation - Light gray
                    [0.6, '#a7f3d0'],    # Weak positive - Light green
                    [0.75, '#34d399'],   # Moderate positive - Green
                    [1, '#059669']       # Strong positive - Dark green
                ],
                zmid=0,  # Center colorscale at 0
                zmin=-1,
                zmax=1,
                hoverongaps=False,
                hovertemplate="<b>%{y}</b> vs <b>%{x}</b><br>" +
                             "Correlation: %{z:.3f}<br>" +
                             "<extra></extra>",
                showscale=True,
                colorbar=dict(
                    title="Correlation<br>Coefficient",
                    title_font_size=12,
                    title_font_weight="bold",
                    title_font_color="#2d3748",
                    tickfont=dict(size=10, color="#4a5568"),
                    len=0.8,
                    thickness=15,
                    bgcolor="rgba(255,255,255,0.9)",
                    bordercolor="rgba(0,0,0,0.1)",
                    borderwidth=1,
                    x=1.02,
                    tickvals=[-1, -0.5, 0, 0.5, 1],
                    ticktext=['-1.0<br>Strong<br>Negative', '-0.5', '0.0<br>No<br>Relation', '+0.5', '+1.0<br>Strong<br>Positive']
                )
            ))
            
            # Add correlation values as text annotations
            annotations = []
            for i, row in enumerate(correlation_matrix.values):
                for j, value in enumerate(row):
                    # Only show text for significant correlations or diagonal
                    if abs(value) > 0.3 or i == j:
                        text_color = 'white' if abs(value) > 0.6 else '#2d3748'
                        annotations.append(
                            dict(
                                x=j, y=i,
                                text=f"{value:.2f}",
                                showarrow=False,
                                font=dict(
                                    color=text_color,
                                    size=10,
                                    weight='bold'
                                )
                            )
                        )
            
            # Beautiful styling for heatmap
            heatmap_fig.update_layout(
                title=f"🔥 Correlation Analysis: {get_short_label(selected_attribute)} & Related Metrics",
                title_x=0.5,
                title_font_size=18,
                title_font_weight="bold",
                title_font_color="#2d3748",
                height=400,
                margin=dict(l=100, r=80, t=80, b=100),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_family=FONT_FAMILY,
                xaxis=dict(
                    title="",
                    tickfont=dict(size=10, color="#374151"),
                    tickangle=45,
                    side='bottom'
                ),
                yaxis=dict(
                    title="",
                    tickfont=dict(size=10, color="#374151"),
                    autorange='reversed'  # Reverse to match matrix orientation
                ),
                annotations=annotations,
                hoverlabel=dict(
                    bgcolor="white",
                    bordercolor="rgba(0,0,0,0.1)",
                    font_size=12,
                    font_family=FONT_FAMILY
                )
            )
            
            # Add subtle border around heatmap
            heatmap_fig.add_shape(
                type="rect",
                xref="x", yref="y",
                x0=-0.5, y0=-0.5,
                x1=len(final_metrics)-0.5, y1=len(final_metrics)-0.5,
                line=dict(color="rgba(45,55,72,0.2)", width=2),
                fillcolor="rgba(0,0,0,0)"
            )
            
            return heatmap_fig
            
        except Exception as e:
            print(f"Error in correlation heatmap: {e}")
            error_fig = go.Figure()
            error_fig.update_layout(
                title="❌ Error loading correlation heatmap",
                title_x=0.5,
                height=400,
                template="plotly_white",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            return error_fig

    print("✅ State analysis callbacks registered successfully!")
