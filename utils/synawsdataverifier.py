import pandas as pd
import uuid

# Load the CSV file
df = pd.read_csv("aws_billing_data_20250225_123327.csv")

# Required columns for verification
required_columns = [
    "lineItem/UsageAmount", "lineItem/UnblendedRate", "lineItem/UnblendedCost",
    "identity/LineItemId", "bill/PayerAccountId", "product/region"
]

# Check for missing columns
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Missing required columns: {missing_columns}")
else:
    # Verify Cost Calculation
    df["calculated_cost"] = df["lineItem/UsageAmount"].astype(float) * df["lineItem/UnblendedRate"].astype(float)
    df["cost_match"] = df["calculated_cost"].round(2) == df["lineItem/UnblendedCost"].astype(float).round(2)

# Check for Negative or Zero Costs
    negative_costs = df[df["lineItem/UnblendedCost"] < 0].shape[0]
    zero_costs = df[df["lineItem/UnblendedCost"] == 0].shape[0]
    zero_cost_records = df[df["lineItem/UnblendedCost"] == 0]

    # Remove zero-cost records if necessary
    df = df[df["lineItem/UnblendedCost"] > 0]

    # Check for Unique Line Item IDs
    unique_line_items = df["identity/LineItemId"].nunique() == len(df)

    # Check for duplicate Line Item IDs
    duplicate_counts = df["identity/LineItemId"].value_counts()
    duplicates = duplicate_counts[duplicate_counts > 1].index.tolist()

# Generate unique Line Item IDs where duplicates exist
def generate_unique_line_item_id(service):
    return f"{service}-{uuid.uuid4().hex[:12]}"

for index, row in df.iterrows():
    if row["identity/LineItemId"] in duplicates:
        df.at[index, "identity/LineItemId"] = generate_unique_line_item_id(row["lineItem/ProductCode"])
        generate_unique_line_item_id(row["lineItem/ProductCode"])
        # Drop duplicates while keeping the first occurrence
    df = df.drop_duplicates(subset="identity/LineItemId", keep="first")

    # Display Verification Results
    verification_results = {
        "Total Records": len(df),
        "Cost Calculation Match": df["cost_match"].value_counts().to_dict(),
        "Negative Cost Records": negative_costs,
        "Zero Cost Records": zero_costs,
        "Unique Line Items": df["identity/LineItemId"].nunique() == len(df)
    }

print(verification_results)
print(zero_cost_records)
print(duplicates)
