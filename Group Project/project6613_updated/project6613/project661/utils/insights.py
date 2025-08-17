# ===========================================
# INSIGHTS GENERATION FUNCTIONS
# ===========================================

from dash import html
from data.loader import get_state_data
from utils.helpers import get_short_label

def generate_insights(selected_attribute, state_data=None):
    """Generate 5 key insights about India based on the selected attribute"""
    
    if not selected_attribute:
        return []
    
    try:
        # Use provided state_data or load it
        if state_data is None:
            state_data = get_state_data()
            
        # Prepare data for analysis
        insights_data = state_data[['State name', selected_attribute]].dropna()
        insights_data = insights_data.groupby('State name')[selected_attribute].mean().reset_index()
        
        # Calculate key statistics
        best_state = insights_data.loc[insights_data[selected_attribute].idxmax()]
        worst_state = insights_data.loc[insights_data[selected_attribute].idxmin()]
        national_avg = insights_data[selected_attribute].mean()
        performance_gap = best_state[selected_attribute] - worst_state[selected_attribute]
        above_avg_states = len(insights_data[insights_data[selected_attribute] > national_avg])
        total_states = len(insights_data)
        
        # Calculate additional stats
        top_25_percentile = insights_data[selected_attribute].quantile(0.75)
        top_performers = insights_data[insights_data[selected_attribute] >= top_25_percentile]
        std_dev = insights_data[selected_attribute].std()
        
        # Generate contextual insights based on attribute category
        attribute_lower = selected_attribute.lower()
        
        insights = []
        
        # Insight 1: Best Performer
        insights.append({
            'icon': '🏆',
            'title': 'Top Performer',
            'value': f"{best_state['State name']}",
            'detail': f"{best_state[selected_attribute]:.1f}%",
            'color': '#10b981'
        })
        
        # Insight 2: National Average
        insights.append({
            'icon': '🇮🇳',
            'title': 'National Average',
            'value': f"{national_avg:.1f}%",
            'detail': f"{above_avg_states}/{total_states} states above average",
            'color': '#3b82f6'
        })
        
        # Insight 3: Performance Gap
        insights.append({
            'icon': '📊',
            'title': 'Performance Gap',
            'value': f"{performance_gap:.1f}%",
            'detail': f"Between {best_state['State name']} and {worst_state['State name']}",
            'color': '#f59e0b'
        })
        
        # Insight 4: Context-specific insight
        if 'literacy' in attribute_lower or 'education' in attribute_lower:
            insights.append({
                'icon': '📚',
                'title': 'Education Focus',
                'value': f"{len(top_performers)} states",
                'detail': f"Achieve >75th percentile ({top_25_percentile:.1f}%)",
                'color': '#8b5cf6'
            })
        elif 'employment' in attribute_lower or 'worker' in attribute_lower:
            insights.append({
                'icon': '💼',
                'title': 'Employment Pattern',
                'value': f"±{std_dev:.1f}%",
                'detail': f"Standard deviation across states",
                'color': '#8b5cf6'
            })
        elif 'household' in attribute_lower or 'amenities' in attribute_lower:
            insights.append({
                'icon': '🏠',
                'title': 'Infrastructure Gap',
                'value': f"{len(top_performers)} states",
                'detail': f"Have >75th percentile amenities",
                'color': '#8b5cf6'
            })
        else:
            insights.append({
                'icon': '📈',
                'title': 'Distribution',
                'value': f"±{std_dev:.1f}%",
                'detail': f"Variation across Indian states",
                'color': '#8b5cf6'
            })
        
        # Insight 5: Bottom performer with improvement potential
        insights.append({
            'icon': '🎯',
            'title': 'Improvement Potential',
            'value': f"{worst_state['State name']}",
            'detail': f"{worst_state[selected_attribute]:.1f}% - Has growth opportunity",
            'color': '#ef4444'
        })
        
        return insights
        
    except Exception as e:
        print(f"Error generating insights: {e}")
        return []

def create_insights_layout(insights, selected_attribute):
    """Create beautiful HTML layout for insights"""
    
    if not insights:
        return html.Div([
            html.Div("📊", style={
                'fontSize': '4rem',
                'textAlign': 'center',
                'marginBottom': '1rem',
                'opacity': '0.3',
                'color': '#94a3b8'
            }),
            html.H3("Select an attribute to see insights", style={
                'textAlign': 'center',
                'color': '#64748b',
                'fontWeight': '500',
                'margin': '0'
            }),
            html.P("Choose a category and attribute to see key insights!", style={
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
    
    insight_cards = []
    
    for insight in insights:
        card = html.Div([
            html.Div([
                html.Span(insight['icon'], style={
                    'fontSize': '1.5rem',
                    'marginRight': '1rem'
                }),
                html.Div([
                    html.Div(insight['title'], style={
                        'fontSize': '0.85rem',
                        'fontWeight': '500',
                        'color': '#64748b',
                        'marginBottom': '0.25rem'
                    }),
                    html.Div(insight['value'], style={
                        'fontSize': '1.1rem',
                        'fontWeight': '700',
                        'color': insight['color'],
                        'marginBottom': '0.25rem'
                    }),
                    html.Div(insight['detail'], style={
                        'fontSize': '0.75rem',
                        'color': '#94a3b8',
                        'lineHeight': '1.2'
                    })
                ], style={'flex': '1'})
            ], style={
                'display': 'flex',
                'alignItems': 'center',
                'padding': '1rem',
                'background': 'linear-gradient(135deg, #f8fafc, #f1f5f9)',
                'borderRadius': '8px',
                'border': f'2px solid {insight["color"]}20',
                'transition': 'transform 0.2s ease',
                'cursor': 'pointer'
            })
        ], style={'marginBottom': '0.5rem'})
        
        insight_cards.append(card)
    
    return html.Div([
        html.Div([
            html.H3(f"📊 Key Insights: {get_short_label(selected_attribute)}", 
                   style={
                       'color': '#2d3748',
                       'fontSize': '1.2rem',
                       'fontWeight': '700',
                       'marginBottom': '1.5rem',
                       'textAlign': 'center'
                   })
        ]),
        html.Div(insight_cards, style={
            'display': 'flex',
            'flexDirection': 'column',
            'gap': '0.5rem'
        })
    ])
