import pandas as pd

# Sample dataframe simulating the structure needed
data = {
    "Feature": ["Costs MI", "Costs MI", "Revenue", "Costs MI", "Costs MI"],
    "FTP Period": ["Q1", "Q2", "Q1", "Q2", "Q3"],
    "FTP Classification": ["A", "A", "B", "B", "A"],
    "FTP Division": ["Div1", "Div1", "Div2", "Div1", "Div2"],
    "Plan Business": ["Biz1", "Biz1", "Biz2", "Biz1", "Biz1"],
    "P&L": [100, 150, 200, 120, 130]
}

df = pd.DataFrame(data)

# Filter for 'Costs MI'
filtered_df = df[df["Feature"] == "Costs MI"]

# Create pivot table
pivot_df = pd.pivot_table(
    filtered_df,
    values="P&L",
    index=["FTP Classification", "FTP Division", "Plan Business"],
    columns="FTP Period",
    aggfunc="sum",
    fill_value=0
)

import ace_tools as tools; tools.display_dataframe_to_user(name="Pivot Table - Costs MI", dataframe=pivot_df)
pivot_df