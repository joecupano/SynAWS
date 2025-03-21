import pandas as pd

REQUIRED_COLUMNS = [
    #'identity/TimeInterval',
    #'identity/LineItemId',
    'bill/PayerAccountId',
    'bill/BillingPeriodStartDate',
    'bill/BillingPeriodEndDate',
    'lineItem/UsageAccountId',
    'lineItem/ProductCode',
    'lineItem/UsageType',
    'lineItem/Operation',
    'lineItem/AvailabilityZone',
    'lineItem/ResourceId',
    #New fields
    'bill/InvoiceId',
    'bill/BillingEntity',
    'bill/InvoiceTotal',
    'bill/BillingCurrency',
    'bill/TaxAmount',
    'bill/TotalCost',
    'lineItem/LineItemType',
    'lineItem/TaxType',
    'product/servicecode',
    'product/sku',
    'pricing/publicOnDemandRate',
    'pricing/publicOnDemandCost',
    #From previous
    #'lineItem/UsageEndTime',
    'lineItem/UsageStartDate',
    'lineItem/UsageEndDate',
    'lineItem/UsageAmount',
    'lineItem/NormalizedUsageAmount',
    'lineItem/UnblendedRate',
    'lineItem/UnblendedCost',
    'lineItem/BlendedRate',
    'lineItem/BlendedCost',
    'lineItem/LineItemDescription',
    'product/ProductName',
    'product/region',
    'pricing/unit'
]

def validate_csv(file_path: str) -> bool:
    """Validate the generated CSV file against AWS CUR 2.0 format"""
    try:
        df = pd.read_csv(file_path)

        # Check for required columns
        for column in REQUIRED_COLUMNS:
            if column not in df.columns:
                print(f"Missing required column: {column}")
                return False

        # Check data types
        for column in ['lineItem/UsageAmount', 'lineItem/NormalizedUsageAmount', 'lineItem/UnblendedRate', 'lineItem/UnblendedCost', 'lineItem/BlendedRate', 'lineItem/BlendedCost']:
            if not pd.api.types.is_numeric_dtype(df[column]):
                print(f"Column {column} should be numeric")
                return False

        for column in ['bill/BillingPeriodStartDate', 'bill/BillingPeriodEndDate', 'lineItem/UsageStartDate', 'lineItem/UsageEndDate']:
            if not pd.api.types.is_string_dtype(df[column]):
                print(f"Column {column} should be a string")
                return False

        # Check value ranges (example for usage amount)
        if (df['lineItem/UsageAmount'] < 0).any():
            print("Usage amount should not be negative")
            return False

        print("CSV file is valid")
        return True

    except Exception as e:
        print(f"Validation failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python validator.py <path_to_csv_file>")
    else:
        file_path = sys.argv[1]
        validate_csv(file_path)
