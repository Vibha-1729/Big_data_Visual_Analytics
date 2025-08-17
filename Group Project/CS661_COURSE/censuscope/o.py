import json
import pandas as pd

# load one state geojson
gj = json.load(open("andhrapradesh.geojson"))
# pick your property key
prop = next(k for k in gj["features"][0]["properties"] if "district" in k.lower())

# extract geo IDs
geo_ids = {str(feat["properties"][prop]).strip().upper() for feat in gj["features"]}

# load the Excel and normalize names
df = pd.read_excel(
    "india-districts-census-2011.xlsx", sheet_name="india-districts-census-2011"
)
df_ids = set(df["District name"].str.strip().str.upper())

print("In GeoJSON but not in DataFrame:", sorted(geo_ids - df_ids))
print("In DataFrame but not in GeoJSON:", sorted(df_ids - geo_ids))
