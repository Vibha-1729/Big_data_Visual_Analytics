# ===========================================
# MAIN LAYOUT COMPONENTS
# ===========================================

from dash import html, dcc
from config.settings import COLORS, FONT_FAMILY

def create_main_layout():
    """Create the main application layout with beautiful UI"""
    return html.Div([
        
        # Hidden div to store active tab state
        html.Div(id='active-tab', children='state', style={'display': 'none'}),
        
        # Beautiful Header Section
        html.Div([
            html.Div([
                # Logo and Title Section
                html.Div([
                    html.Div("🇮🇳", style={
                        'fontSize': '4rem',
                        'marginRight': '2rem',
                        'background': COLORS['gradient_1'],
                        'backgroundClip': 'text',
                        'WebkitBackgroundClip': 'text',
                        'color': 'transparent',
                        'filter': 'drop-shadow(2px 2px 4px rgba(0,0,0,0.3))'
                    }),
                    html.Div([
                        html.H1("India Demographics Dashboard", style={
                            'margin': 0,
                            'fontSize': '3.5rem',
                            'fontWeight': '800',
                            'background': COLORS['gradient_1'],
                            'backgroundClip': 'text',
                            'WebkitBackgroundClip': 'text',
                            'color': 'transparent',
                            'letterSpacing': '-0.02em'
                        }),
                        html.P("Explore India's Rich Demographic Landscape with Interactive Visualizations", style={
                            'margin': '0.5rem 0 0 0',
                            'fontSize': '1.3rem',
                            'color': '#64748b',
                            'fontWeight': '500',
                            'letterSpacing': '0.01em'
                        })
                    ])
                ], style={'display': 'flex', 'alignItems': 'center'}),
                
                # Stats Cards
                html.Div([
                    html.Div([
                        html.Div("📊", style={'fontSize': '2rem', 'marginBottom': '0.5rem'}),
                        html.H3("35", style={'margin': 0, 'color': COLORS['dark'], 'fontSize': '1.8rem'}),
                        html.P("States & UTs", style={'margin': 0, 'color': '#64748b', 'fontSize': '0.9rem'})
                    ], style={
                        'background': 'white',
                        'padding': '1.5rem',
                        'borderRadius': '16px',
                        'textAlign': 'center',
                        'boxShadow': '0 10px 30px rgba(99, 102, 241, 0.15)',
                        'border': '1px solid rgba(99, 102, 241, 0.1)',
                        'flex': '1'
                    }),
                    
                    html.Div([
                        html.Div("🏘️", style={'fontSize': '2rem', 'marginBottom': '0.5rem'}),
                        html.H3("640+", style={'margin': 0, 'color': COLORS['dark'], 'fontSize': '1.8rem'}),
                        html.P("Districts", style={'margin': 0, 'color': '#64748b', 'fontSize': '0.9rem'})
                    ], style={
                        'background': 'white',
                        'padding': '1.5rem',
                        'borderRadius': '16px',
                        'textAlign': 'center',
                        'boxShadow': '0 10px 30px rgba(236, 72, 153, 0.15)',
                        'border': '1px solid rgba(236, 72, 153, 0.1)',
                        'flex': '1'
                    }),
                    
                    html.Div([
                        html.Div("📈", style={'fontSize': '2rem', 'marginBottom': '0.5rem'}),
                        html.H3("80+", style={'margin': 0, 'color': COLORS['dark'], 'fontSize': '1.8rem'}),
                        html.P("Metrics", style={'margin': 0, 'color': '#64748b', 'fontSize': '0.9rem'})
                    ], style={
                        'background': 'white',
                        'padding': '1.5rem',
                        'borderRadius': '16px',
                        'textAlign': 'center',
                        'boxShadow': '0 10px 30px rgba(16, 185, 129, 0.15)',
                        'border': '1px solid rgba(16, 185, 129, 0.1)',
                        'flex': '1'
                    })
                    
                ], style={
                    'display': 'flex',
                    'gap': '1.5rem',
                    'marginTop': '2rem'
                })
                
            ], style={
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '3rem 2rem'
            })
        ], style={
            'background': f'linear-gradient(135deg, {COLORS["background_light"]} 0%, #ffffff 100%)',
            'borderBottom': '1px solid #e2e8f0'
        }),
        
        # Navigation Tabs
        html.Div([
            html.Div([
                # Tab Buttons
                html.Div([
                    html.Button([
                        html.Span("🗺️", style={'fontSize': '1.2rem', 'marginRight': '0.8rem'}),
                        "State Analysis"
                    ], 
                    id="tab-state", 
                    className="custom-tab active",
                    style={
                        'background': 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                        'color': 'white',
                        'border': 'none',
                        'padding': '1rem 2rem',
                        'borderRadius': '12px',
                        'fontSize': '1rem',
                        'fontWeight': '600',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease',
                        'boxShadow': '0 6px 20px rgba(99, 102, 241, 0.3)',
                        'marginRight': '1rem',
                        'fontFamily': FONT_FAMILY
                    }),
                    
                    html.Button([
                        html.Span("🏘️", style={'fontSize': '1.2rem', 'marginRight': '0.8rem'}),
                        "District Analysis"
                    ], 
                    id="tab-district", 
                    className="custom-tab",
                    style={
                        'background': 'white',
                        'color': '#64748b',
                        'border': '2px solid #e2e8f0',
                        'padding': '1rem 2rem',
                        'borderRadius': '12px',
                        'fontSize': '1rem',
                        'fontWeight': '600',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease',
                        'marginRight': '1rem',
                        'fontFamily': FONT_FAMILY
                    }),
                    
                    html.Button([
                        html.Span("⚖️", style={'fontSize': '1.2rem', 'marginRight': '0.8rem'}),
                        "Compare States"
                    ], 
                    id="tab-comparison", 
                    className="custom-tab",
                    style={
                        'background': 'white',
                        'color': '#64748b',
                        'border': '2px solid #e2e8f0',
                        'padding': '1rem 2rem',
                        'borderRadius': '12px',
                        'fontSize': '1rem',
                        'fontWeight': '600',
                        'cursor': 'pointer',
                        'transition': 'all 0.3s ease',
                        'fontFamily': FONT_FAMILY
                    })
                    
                ], style={'display': 'flex', 'alignItems': 'center'})
                
            ], style={
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '1.5rem 2rem',
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center'
            })
        ], style={
            'background': 'white',
            'borderBottom': '1px solid #e2e8f0',
            'position': 'sticky',
            'top': '0',
            'zIndex': '100',
            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.05)'
        }),
        
        # Main Content Area
        html.Div([
            html.Div(id='tab-content', children=[], style={
                'minHeight': 'calc(100vh - 300px)',
                'maxWidth': '1400px',
                'margin': '0 auto'
            })
        ], style={
            'background': f'linear-gradient(135deg, {COLORS["background_light"]} 0%, #ffffff 100%)',
            'fontFamily': FONT_FAMILY
        }),
        
        # Beautiful Footer
        html.Div([
            html.Div([
                html.Div([
                    html.P([
                        "🚀 Built with ",
                        html.Strong("Dash & Plotly", style={'color': COLORS['primary']}),
                        " • Data insights for a better India 🇮🇳"
                    ], style={
                        'margin': 0,
                        'color': '#64748b',
                        'fontSize': '1rem',
                        'textAlign': 'center'
                    }),
                    html.P("© 2024 India Demographics Dashboard. Empowering decisions through data.", style={
                        'margin': '0.5rem 0 0 0',
                        'color': '#94a3b8',
                        'fontSize': '0.9rem',
                        'textAlign': 'center'
                    })
                ])
            ], style={
                'maxWidth': '1400px',
                'margin': '0 auto',
                'padding': '2rem',
                'textAlign': 'center'
            })
        ], style={
            'background': f'linear-gradient(135deg, {COLORS["background_light"]} 0%, #ffffff 100%)',
            'borderTop': '1px solid #e2e8f0',
            'marginTop': '3rem'
        })
        
    ], style={
        'fontFamily': FONT_FAMILY,
        'backgroundColor': COLORS['background_light'],
        'minHeight': '100vh'
    })
