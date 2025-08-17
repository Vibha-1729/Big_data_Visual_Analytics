# Copilot Instructions for India Geographic Data Visualization Dashboard

## Project Overview
This is a Dash-based interactive dashboard for visualizing Indian demographic data across states and districts. The app provides choropleth maps, statistical analyses, and correlation visualizations using geographic boundaries and census-like data.

## Architecture & Data Flow

### Core Components
- **Main App** (`app.py`): Single-file Dash application with multi-panel layout
- **Geographic Data**: `india.json` (national boundaries) + individual state `.geojson` files
- **Demographic Data**: `districtwise_data_percentages.csv` with census metrics by district
- **Layout**: Left panel (India map + selectors), Right panel (analytics charts)

### Key Data Structures
- `ATTRIBUTE_MAP`: Hierarchical mapping of demographic categories to subcategories (Population → Male/Female)
- `SUBCATEGORY_SHORT_NAMES`: Display labels for chart axes to handle long column names
- `population_data`: Hardcoded state population values for map coloring
- `state_file_map`: Dynamic mapping from state names to `.geojson` filenames

### Critical Data Dependencies
- CSV must have columns: `State name`, `District name`, plus metric columns with optional `_pct` suffix
- GeoJSON files named by state key (e.g., `uttar_pradesh.geojson`)
- State names in `india.json` must match CSV `State name` values (case-insensitive)

## Development Patterns

### Callback Architecture
- **State Selection**: India map click → state selector → triggers all district-level visualizations
- **Attribute Selection**: Category dropdown → populates subcategory dropdown → updates charts
- **Correlation**: Two-attribute selection → scatter plot with color-coded correlation indicator
- **Error Handling**: All callbacks use try/catch with `go.Figure()` fallbacks

### Visual Design Patterns
- **Color Schemes**: Sequential (YlOrRd for maps), Categorical (Plasma for bars), Pastel (pie charts)
- **State Highlighting**: Selected state gets black outline + shadow effect, others fade to light green
- **Chart Consistency**: All use `PLOTLY_FONT` and `#f8f9fa` background with subtle shadows
- **Log Scaling**: Automatically applied when bar chart value ratios exceed 50:1

### Data Processing Conventions
- State names normalized: lowercase, spaces→underscores, hyphens→underscores
- Column lookup: Try `{metric}_pct` first, fallback to `{metric}`
- Short labels: Use `short_label()` function for compact axis labels
- Missing data: `dropna()` applied before all visualizations

## Development Workflow

### Running the App
```bash
python app.py  # Runs on http://127.0.0.1:8050 in debug mode
```

### Adding New Attributes
1. Add category and subcategories to `ATTRIBUTE_MAP`
2. Add short names to `SUBCATEGORY_SHORT_NAMES` 
3. Ensure CSV has corresponding columns (with or without `_pct` suffix)

### Adding New States
1. Add `.geojson` file with state key naming convention
2. Add population entry to `population_data` dict
3. Verify state name consistency between `india.json` and CSV

### Debugging Common Issues
- **Map not loading**: Check GeoJSON file naming and `featureidkey` property matching
- **Charts empty**: Verify CSV column names match `ATTRIBUTE_MAP` entries
- **State highlighting broken**: Ensure state name normalization consistency
- **Correlation errors**: Check for sufficient data points and numeric columns

## File Structure Expectations
```
project/
├── app.py                              # Main application
├── india.json                          # National boundary data
├── {state_key}.geojson                 # Individual state boundaries
├── districtwise_data_percentages.csv   # District demographic data
└── districtwise_data.csv              # Raw counts (optional)
```

## Extension Points
- **New Chart Types**: Add to right panel layout, create callback with error handling
- **Data Sources**: Modify CSV loading logic in callbacks, maintain column name patterns
- **Geographic Levels**: Add sub-district support by extending state-district pattern
- **Export Features**: Integrate with Plotly's built-in export capabilities in chart configs
