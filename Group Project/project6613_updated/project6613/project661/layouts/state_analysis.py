# ===========================================
# STATE ANALYSIS LAYOUT
# ===========================================

from dash import html, dcc
from config.settings import COLORS

def create_state_analysis_layout():
    """Create the beautiful State Analysis tab layout"""
    return html.Div([
        
        # Control Panel
        html.Div([
            html.Div([
                html.Span("🎯", style={
                    'fontSize': '1.5rem',
                    'marginRight': '1rem',
                    'padding': '10px',
                    'background': COLORS['gradient_1'],
                    'borderRadius': '10px',
                    'color': 'white'
                }),
                html.H3("Analysis Controls", style={'margin': 0, 'color': 'white'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Div([
                    html.Label("📊 Select Category", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="category-dropdown",
                        placeholder="Choose a demographic category...",
                        style={'borderRadius': '12px'}
                    )
                ], style={'marginBottom': '1.5rem'}),
                
                html.Div([
                    html.Label("📈 Select Attribute", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="attribute-dropdown",
                        placeholder="First select a category...",
                        style={'borderRadius': '12px'}
                    )
                ], style={'marginBottom': '1.5rem'}),
            ])
            
        ], style={
            'background': COLORS['gradient_2'],
            'padding': '2rem',
            'borderRadius': '16px',
            'margin': '1.5rem',
            'boxShadow': '0 10px 30px rgba(240, 147, 251, 0.3)'
        }),
        
        # Charts Grid
        html.Div([
            
            # India Map Card
            html.Div([
                html.Div([
                    html.Span("🗺️", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_3'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("India Choropleth Map", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="india-map",
                        style={'height': '500px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # State Rankings Card
            html.Div([
                html.Div([
                    html.Span("🏆", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_2'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("State Rankings", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="state-rankings",
                        style={'height': '500px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
        # Additional Charts Row - First Set
        html.Div([
            
            # Box Plot Card
            html.Div([
                html.Div([
                    html.Span("📦", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_4'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Distribution Summary", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="box-plot",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # Pie Chart Card
            html.Div([
                html.Div([
                    html.Span("🥧", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_5'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Top 7 States", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="top-states-pie",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
        # Additional Charts Row - Second Set
        html.Div([
            
            # Insights Card
            html.Div([
                html.Div([
                    html.Span("💡", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': 'linear-gradient(135deg, #ff9a56 0%, #ffad56 100%)',
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Key Insights", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    html.Div(id="insights-content", style={
                        'background': 'white', 
                        'borderRadius': '16px', 
                        'padding': '1.5rem', 
                        'margin': '1rem 0', 
                        'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)',
                        'minHeight': '350px'
                    })
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # Correlation Heatmap Card
            html.Div([
                html.Div([
                    html.Span("⭐", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)',
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Correlation Heatmap", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="correlation-heatmap",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
    ])
