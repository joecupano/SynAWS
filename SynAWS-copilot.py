import streamlit as st
import csv
import random
import io
from datetime import datetime, timedelta

AWS_REGIONS = ['us-east-1', 'us-west-1', 'eu-west-1']
AWS_SERVICES = {
    'EC2': ['t2.micro', 't2.small', 'm5.large'],
    'S3': ['Standard', 'Infrequent Access', 'Glacier'],
    'RDS': ['db.t2.micro', 'db.m5.large']
}

st.title('Synthetic AWS Billing Data Generator')

regions = st.multiselect('Select AWS Regions:', AWS_REGIONS)
services = st.multiselect('Select AWS Services:', list(AWS_SERVICES.keys()))
days = st.selectbox('Select Number of Days:', [30, 45, 60, 90])

if st.button('Generate'):
    if not regions or not services:
        st.error("Please select at least one region and one service.")
    else:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['InvoiceID', 'PayerAccountId', 'LinkedAccountId', 'RecordType', 'RecordId', 'ProductName', 'RateId', 'SubscriptionId', 'PricingPlanId', 'UsageType', 'Operation', 'AvailabilityZone', 'ReservedInstance', 'ItemDescription', 'UsageStartDate', 'UsageEndDate', 'UsageQuantity', 'BlendedRate', 'BlendedCost', 'UnBlendedRate', 'UnBlendedCost', 'ResourceId'])

        start_date = datetime.now() - timedelta(days=days)
        for day in range(days):
            for region in regions:
                for service in services:
                    for option in AWS_SERVICES[service]:
                        usage_date = start_date + timedelta(days=day)
                        usage_quantity = random.uniform(1, 100)
                        blended_rate = random.uniform(0.01, 0.1)
                        blended_cost = usage_quantity * blended_rate
                        writer.writerow([
                            random.randint(1000000, 9999999), '123456789012', '123456789012', 'LineItem', random.randint(1000000, 9999999), service, random.randint(1000000, 9999999), random.randint(1000000, 9999999), random.randint(1000000, 9999999), option, 'RunInstances', region, 'N', f'{service} usage', usage_date.strftime('%Y-%m-%dT%H:%M:%SZ'), (usage_date + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ'), usage_quantity, blended_rate, blended_cost, blended_rate, blended_cost, ''
                        ])

        output.seek(0)
        st.download_button(label="Download CSV", data=output.getvalue(), file_name='synthetic_billing_data.csv', mime='text/csv')
