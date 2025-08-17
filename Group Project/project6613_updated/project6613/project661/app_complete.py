# ===========================================
# INDIA DEMOGRAPHICS DASHBOARD - COMPLETE REFACTORED VERSION
# ===========================================

import dash
from dash import html, dcc

# Import modular components
from config.settings import FONT_FAMILY, COLORS
from data.loader import load_geojson_data, load_state_data, load_district_data, categorize_attributes
from layouts.main_layout import create_main_layout
from callbacks import register_all_callbacks

print("🚀 Starting India Demographics Dashboard - Complete Refactored Version")
print("=" * 70)

# Initialize Dash app with beautiful styling
app = dash.Dash(
    __name__,
    title="🇮🇳 India Demographics Dashboard",
    suppress_callback_exceptions=True,
    external_stylesheets=[
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap'
    ]
)

# Add beautiful custom CSS for enhanced UI
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
                min-height: 100vh; overflow-x: hidden;
            }
            
            /* Beautiful button hover effects */
            .custom-tab:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4) !important;
            }
            
            .custom-tab.active {
                background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
                color: white !important;
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3) !important;
            }
            
            /* Enhanced scrollbar */
            ::-webkit-scrollbar { width: 8px; }
            ::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 10px; }
            ::-webkit-scrollbar-thumb { background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 10px; }
            ::-webkit-scrollbar-thumb:hover { background: linear-gradient(135deg, #4f46e5, #7c3aed); }
            
            /* Beautiful table hover effects */
            .table-row:hover {
                background-color: #f8fafc !important;
                transform: scale(1.01);
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            }
            
            /* Smooth animations */
            * { transition: all 0.3s ease !important; }
            
            /* Loading animations */
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.7; }
            }
            
            .loading { animation: pulse 2s infinite; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Set the main layout
app.layout = create_main_layout()

# Register all callbacks
register_all_callbacks(app)

# Load and verify all data
print("📊 Loading and verifying all data sources...")
try:
    india_geo = load_geojson_data()
    state_data = load_state_data()
    district_data = load_district_data()
    categories = categorize_attributes()
    
    print("✅ Data loading verification:")
    print(f"   🗺️ India GeoJSON: {len(india_geo['features'])} states loaded")
    print(f"   📊 State Data: {len(state_data)} rows, {len(state_data.columns)} columns")
    print(f"   🏘️ District Data: {len(district_data)} rows, {len(district_data.columns)} columns")
    print(f"   📈 Categories: {len(categories)} demographic groups organized")
    
    print("\n✅ All components loaded successfully!")
    print("🎨 Beautiful UI components active!")
    print("🔥 All callbacks registered and ready!")
    print("📊 6 stunning visualizations available:")
    print("   🗺️ India Choropleth Map")
    print("   🏆 State Rankings Bar Chart") 
    print("   📦 Distribution Box Plot")
    print("   🥧 Top States Pie Chart")
    print("   💡 Dynamic Insights Cards")
    print("   🔥 Correlation Heatmap")
    print("🏘️ District analysis with maps, rankings & data tables!")
    
except Exception as e:
    print(f"❌ Error during data loading: {e}")
    print("Please check your data files and try again.")

# Make sure your callback updates dcc.Graph(id='india-map') with a choropleth using india_geo.
# Example callback (in callbacks.py):
# @app.callback(Output('india-map', 'figure'), [...])
# def update_india_map(...):
#     fig = px.choropleth_mapbox(
#         state_data,
#         geojson=india_geo,
#         locations='state_code',
#         color='some_metric',
#         ...
#     )
#     return fig

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("🌟 INDIA DEMOGRAPHICS DASHBOARD - FULLY REFACTORED")
    print("🌐 Access your enhanced dashboard at: http://127.0.0.1:8080")
    print("🎨 Beautiful modular architecture with stunning visualizations!")
    print("📊 State Analysis + District Analysis + Coming Soon: Comparisons")
    print("🚀 Enjoy exploring India's demographic insights!")
    print("=" * 70)
    
    app.run(debug=True, host='127.0.0.1', port=8080)
