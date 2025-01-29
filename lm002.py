import pandas as pd

# Load the main Excel file (Assumed filename: "main_data.xlsx")
file_path = "main_data.xlsx"
xls = pd.ExcelFile(file_path)

# Load Entity Mapping File
entity_map_df = pd.read_excel("Entitymap.xlsx")

# Create a dictionary for entity mapping
entity_map = dict(zip(entity_map_df.iloc[:, 0], entity_map_df.iloc[:, 1]))

# Function to process a single sheet
def process_sheet(sheet_name, df):
    if sheet_name == "ND":
        # Filter Column X to keep only "New Deal - New"
        df = df[df["x"] == "New Deal - New"]

        # Filter tenure column to keep only values > 7
        df = df[df["tenure"] > 7]

    # Replace Entity and CEntity values based on mapping
    df["Entity"] = df["Entity"].map(entity_map).fillna(df["Entity"])
    df["CEntity"] = df["CEntity"].map(entity_map).fillna(df["CEntity"])

    # Filter based on 'value' column
    df = filter_values(df)

    # Remove Entity and CEntity columns
    df = df.drop(columns=["Entity", "CEntity"], errors="ignore")

    return df

# Function to filter values based on conditions
def filter_values(df):
    df["Keep"] = df["value"] > 500  # Mark records where value > 500
    
    # Identify pairs of records whose combined value exceeds 500
    combined_indices = []
    grouped = df.groupby("CEntity")
    
    for _, group in grouped:
        if len(group) > 1 and group["value"].sum() > 500:
            combined_indices.extend(group.index)
    
    df.loc[combined_indices, "Keep"] = True  # Keep these records
    df = df[df["Keep"]].drop(columns=["Keep"])
    
    return df

# Process each sheet
processed_sheets = {}
for sheet in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet)
    processed_sheets[sheet] = process_sheet(sheet, df)

# Save processed data to a new Excel file
output_file = "processed_data.xlsx"
with pd.ExcelWriter(output_file) as writer:
    for sheet, df in processed_sheets.items():
        df.to_excel(writer, sheet_name=sheet, index=False)

print(f"Processed file saved as {output_file}")