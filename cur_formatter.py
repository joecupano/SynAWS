import pandas as pd
from typing import List

class CURFormatter:
    @staticmethod
    def format_cur_csv(df: pd.DataFrame) -> str:
        """Format DataFrame as CUR 2.0 CSV string"""
        # Ensure correct column order
        columns = [
            'identity/TimeInterval',
            'identity/LineItemId',
            'bill/PayerAccountId',
            'bill/BillingPeriodStartDate',
            'bill/BillingPeriodEndDate',
            'lineItem/UsageAccountId',
            'lineItem/ProductCode',
            'lineItem/UsageType',
            'lineItem/Operation',
            'lineItem/AvailabilityZone',
            'lineItem/ResourceId',
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
        
        df = df[columns]
        return df.to_csv(index=False)
