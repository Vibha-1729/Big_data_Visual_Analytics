# ===========================================
# DISTRICT ANALYSIS LAYOUT
# ===========================================

from dash import html, dcc
from config.settings import COLORS

def create_district_analysis_layout():
    """Create the beautiful District Analysis tab layout"""
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
                html.H3("District Analysis Controls", style={'margin': 0, 'color': 'white'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem'}),
            
            html.Div([
                html.Div([
                    html.Label("🗺️ Select State", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="district-state-dropdown",
                        placeholder="Choose a state to analyze districts...",
                        style={'borderRadius': '12px'}
                    )
                ], style={'marginBottom': '1.5rem'}),
                
                html.Div([
                    html.Label("📊 Select Metric", style={'color': 'white', 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                    dcc.Dropdown(
                        id="district-attribute-dropdown",
                        placeholder="First select a state...",
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
        
        # District Analysis Charts
        html.Div([
            
            # District Map Card
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
                    html.H3("District Choropleth Map", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="district-map",
                        style={'height': '500px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)', 'gridColumn': 'span 2'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '2rem', 'padding': '1rem'}),
        
        # District Rankings and Performance
        html.Div([
            
            # District Rankings Card
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
                    html.H3("District Rankings", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="district-rankings",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
            # District Performance Matrix Card
            html.Div([
                html.Div([
                    html.Span("📊", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_4'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("Performance Matrix", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                html.Div([
                    dcc.Graph(
                        id="district-scatter",
                        style={'height': '400px'},
                        config={'displayModeBar': False}
                    )
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'}),
            
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fit, minmax(400px, 1fr))', 'gap': '2rem', 'padding': '1rem'}),
        
        # District Data Table Section
        html.Div([
            html.Div([
                html.Div([
                    html.Span("📋", style={
                        'fontSize': '1.5rem',
                        'marginRight': '1rem',
                        'padding': '10px',
                        'background': COLORS['gradient_5'],
                        'borderRadius': '10px',
                        'color': 'white'
                    }),
                    html.H3("District Data Explorer", style={'margin': 0, 'color': COLORS['dark']})
                ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '1.5rem', 'paddingBottom': '1rem', 'borderBottom': '2px solid #f1f5f9'}),
                
                # Table Controls
                html.Div([
                    html.Div([
                        html.Label("🔍 Search Districts", style={'color': COLORS['dark'], 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                        dcc.Input(
                            id="district-search",
                            type="text",
                            placeholder="Search for districts...",
                            style={
                                'width': '100%',
                                'padding': '12px',
                                'borderRadius': '8px',
                                'border': '2px solid #e2e8f0',
                                'fontSize': '14px'
                            }
                        )
                    ], style={'flex': '1', 'marginRight': '1rem'}),
                    
                    html.Div([
                        html.Label("📊 Show Rows", style={'color': COLORS['dark'], 'fontWeight': '600', 'marginBottom': '0.5rem', 'display': 'block'}),
                        dcc.Dropdown(
                            id="district-table-limit",
                            options=[
                                {"label": "Top 10", "value": 10},
                                {"label": "Top 20", "value": 20},
                                {"label": "Top 50", "value": 50},
                                {"label": "All", "value": "all"}
                            ],
                            value=20,
                            style={'width': '150px'}
                        )
                    ], style={'flex': '0 0 auto'})
                    
                ], style={'display': 'flex', 'alignItems': 'end', 'marginBottom': '1.5rem'}),
                
                # Data Table
                html.Div([
                    html.Div(id="district-summary-table", style={
                        'background': 'white', 
                        'borderRadius': '12px', 
                        'padding': '1rem', 
                        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.1)',
                        'maxHeight': '600px',
                        'overflowY': 'auto'
                    })
                ], style={'background': 'white', 'borderRadius': '16px', 'padding': '1rem', 'margin': '1rem 0', 'boxShadow': '0 8px 25px rgba(0, 0, 0, 0.1)'})
                
            ], style={'background': 'white', 'borderRadius': '16px', 'padding': '2rem', 'margin': '1.5rem', 'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'})
        ], style={'padding': '1rem'}),
        
    ])

def create_comparison_layout():
    """Create the beautiful Comparison tab layout"""
    return html.Div([
        
        # Coming Soon Section
        html.Div([
            html.Div([
                html.Div("🚀", style={
                    'fontSize': '6rem',
                    'textAlign': 'center',
                    'marginBottom': '2rem',
                    'opacity': '0.7',
                    'background': COLORS['gradient_1'],
                    'backgroundClip': 'text',
                    'WebkitBackgroundClip': 'text',
                    'color': 'transparent'
                }),
                html.H1("State Comparison Tool", style={
                    'textAlign': 'center',
                    'color': COLORS['dark'],
                    'fontWeight': '700',
                    'fontSize': '3rem',
                    'marginBottom': '1rem',
                    'background': COLORS['gradient_2'],
                    'backgroundClip': 'text',
                    'WebkitBackgroundClip': 'text',
                    'color': 'transparent'
                }),
                html.H3("Coming Soon!", style={
                    'textAlign': 'center',
                    'color': '#64748b',
                    'fontWeight': '500',
                    'fontSize': '1.5rem',
                    'marginBottom': '2rem'
                }),
                html.P("We're working on an amazing side-by-side state comparison feature with interactive charts and detailed analytics!", style={
                    'textAlign': 'center',
                    'color': '#94a3b8',
                    'fontSize': '1.1rem',
                    'maxWidth': '600px',
                    'margin': '0 auto 3rem auto',
                    'lineHeight': '1.6'
                }),
                
                # Feature Preview Cards
                html.Div([
                    html.Div([
                        html.Div("📊", style={'fontSize': '3rem', 'marginBottom': '1rem'}),
                        html.H4("Multi-State Charts", style={'color': COLORS['dark'], 'marginBottom': '0.5rem'}),
                        html.P("Compare up to 4 states simultaneously", style={'color': '#94a3b8', 'fontSize': '0.9rem'})
                    ], style={
                        'background': 'white',
                        'padding': '2rem',
                        'borderRadius': '16px',
                        'textAlign': 'center',
                        'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)',
                        'border': '2px solid #f1f5f9'
                    }),
                    
                    html.Div([
                        html.Div("🎯", style={'fontSize': '3rem', 'marginBottom': '1rem'}),
                        html.H4("Performance Metrics", style={'color': COLORS['dark'], 'marginBottom': '0.5rem'}),
                        html.P("Detailed performance indicators and rankings", style={'color': '#94a3b8', 'fontSize': '0.9rem'})
                    ], style={
                        'background': 'white',
                        'padding': '2rem',
                        'borderRadius': '16px',
                        'textAlign': 'center',
                        'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)',
                        'border': '2px solid #f1f5f9'
                    }),
                    
                    html.Div([
                        html.Div("⚡", style={'fontSize': '3rem', 'marginBottom': '1rem'}),
                        html.H4("Interactive Filters", style={'color': COLORS['dark'], 'marginBottom': '0.5rem'}),
                        html.P("Dynamic filtering and real-time updates", style={'color': '#94a3b8', 'fontSize': '0.9rem'})
                    ], style={
                        'background': 'white',
                        'padding': '2rem',
                        'borderRadius': '16px',
                        'textAlign': 'center',
                        'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)',
                        'border': '2px solid #f1f5f9'
                    })
                    
                ], style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
                    'gap': '2rem',
                    'marginBottom': '3rem'
                })
                
            ], style={
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center',
                'alignItems': 'center',
                'minHeight': '60vh',
                'padding': '4rem 2rem'
            })
        ], style={
            'background': f'linear-gradient(135deg, {COLORS["background_light"]} 0%, #ffffff 100%)',
            'margin': '1.5rem',
            'borderRadius': '16px',
            'boxShadow': '0 10px 30px rgba(0, 0, 0, 0.1)'
        })
    ])
