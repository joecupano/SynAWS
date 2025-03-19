import pandas as pd
from typing import List

class CURFormatter:
    @staticmethod
    def format_cur_csv(df: pd.DataFrame) -> str:
        """Format DataFrame as CUR 2.0 CSV string"""
        # Ensure correct column order
        columns = [
            #'identity/TimeInterval', This is now removed as not CUR 2.0
            #'identity/LineItemId', This is now removed as not CUR 2.0 as LineItem description and LineItem Resource ID is what is used 
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
        
        df = df[columns]
        return df.to_csv(index=False)
