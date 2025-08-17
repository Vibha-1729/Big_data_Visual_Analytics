# ===========================================
# MAIN CALLBACKS COORDINATOR
# ===========================================

from dash import Input, Output, callback_context
from callbacks.state_callbacks import register_state_callbacks
from callbacks.district_callbacks import register_district_callbacks
from layouts.state_analysis import create_state_analysis_layout
from layouts.district_analysis import create_district_analysis_layout, create_comparison_layout
from config.settings import ATTRIBUTE_CATEGORIES

def register_all_callbacks(app):
    """Register all application callbacks"""
    
    # Register tab-specific callbacks
    register_state_callbacks(app)
    register_district_callbacks(app)
    
    # Main tab switching callback
    @app.callback(
        [Output('tab-content', 'children'),
         Output('active-tab', 'children'),
         Output('tab-state', 'className'),
         Output('tab-district', 'className'),
         Output('tab-comparison', 'className')],
        [Input('tab-state', 'n_clicks'),
         Input('tab-district', 'n_clicks'),
         Input('tab-comparison', 'n_clicks')]
    )
    def update_tab_content(state_clicks, district_clicks, comparison_clicks):
        """Handle tab switching with beautiful transitions"""
        ctx = callback_context
        
        if not ctx.triggered:
            return create_state_analysis_layout(), "state", "custom-tab active", "custom-tab", "custom-tab"
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'tab-state':
            return (create_state_analysis_layout(), "state", 
                    "custom-tab active", "custom-tab", "custom-tab")
        elif button_id == 'tab-district':
            return (create_district_analysis_layout(), "district",
                    "custom-tab", "custom-tab active", "custom-tab")
        elif button_id == 'tab-comparison':
            return (create_comparison_layout(), "comparison",
                    "custom-tab", "custom-tab", "custom-tab active")
        
        return create_state_analysis_layout(), "state", "custom-tab active", "custom-tab", "custom-tab"

    # Category dropdown initialization callback
    @app.callback(
        Output('category-dropdown', 'options'),
        [Input('tab-content', 'children')]
    )
    def update_category_dropdown(_):
        """Initialize category dropdown options"""
        return [{"label": category, "value": category} for category in ATTRIBUTE_CATEGORIES.keys()]
    
    print("✅ All callbacks registered successfully!")
