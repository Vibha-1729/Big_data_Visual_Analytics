#!/usr/bin/env python3

import pandas as pd

print("🔍 Debugging Data Loading...")

# Load the data the same way as the main app
try:
    state_data_full = pd.read_csv('statewiseaggregated.csv')
    essential_cols = ['State name', 'District code', 'Population']
    pct_cols = [col for col in state_data_full.columns if col.endswith('_pct')]
    state_data = state_data_full[essential_cols + pct_cols]
    
    print(f"✅ Data loaded successfully")
    print(f"📊 Shape: {state_data.shape}")
    print(f"🏷️  Total percentage columns: {len(pct_cols)}")
    
    # Check for the specific column
    target_col = 'Households_with_Scooter_Motorcycle_Moped_pct'
    print(f"\n🎯 Checking column: {target_col}")
    print(f"   Exists: {target_col in state_data.columns}")
    
    if target_col in state_data.columns:
        print(f"   Data type: {state_data[target_col].dtype}")
        print(f"   Non-null count: {state_data[target_col].count()}")
        print(f"   Null count: {state_data[target_col].isnull().sum()}")
        print(f"   Min value: {state_data[target_col].min()}")
        print(f"   Max value: {state_data[target_col].max()}")
        print(f"   Sample values:")
        print(state_data[['State name', target_col]].head(10))
        
        # Try the exact operations that the ranking function does
        print(f"\n🧪 Testing ranking operations...")
        rankings_data = state_data[['State name', target_col]].dropna()
        print(f"   After dropna: {len(rankings_data)} rows")
        
        rankings_data = rankings_data.groupby('State name')[target_col].mean().reset_index()
        print(f"   After groupby: {len(rankings_data)} rows")
        
        rankings_data = rankings_data.sort_values(target_col, ascending=False).reset_index(drop=True)
        print(f"   After sorting: {len(rankings_data)} rows")
        print(f"   Top 5 states:")
        print(rankings_data.head())
    else:
        print(f"❌ Column not found!")
        print(f"Available columns containing 'scooter':")
        scooter_cols = [col for col in state_data.columns if 'scooter' in col.lower()]
        print(scooter_cols)
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
