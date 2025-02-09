import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List
from services import AWS_SERVICES, AWSService

class BillingDataGenerator:
    def __init__(self, selected_services: Dict[str, Dict], selected_region: str, days: int):
        self.selected_services = selected_services
        self.selected_region = selected_region
        self.days = days
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=days)

    def generate_usage_pattern(self, mean_value: float, num_points: int) -> np.ndarray:
        """Generate realistic usage patterns with daily and weekly cycles"""
        base = np.random.normal(mean_value, mean_value * 0.1, num_points)
        hours = np.arange(num_points) % 24
        daily_pattern = np.sin(hours * 2 * np.pi / 24) * 0.2 * mean_value
        days = np.arange(num_points) % 168
        weekly_pattern = (days < 120).astype(float) * 0.15 * mean_value
        return np.maximum(base + daily_pattern + weekly_pattern, 0)

    def generate_data(self) -> pd.DataFrame:
        records = []
        hours = self.days * 24
        for service_name, options in self.selected_services.items():
            service = AWS_SERVICES[service_name]
            region_mult = service.region_multiplier[self.selected_region]
            for option in service.options:
                if option.name in options:
                    usage_value = float(options[option.name])
                    if usage_value > 0:
                        usage_pattern = self.generate_usage_pattern(usage_value, hours)
                        for hour in range(hours):
                            current_time = self.start_date + timedelta(hours=hour)
                            usage = usage_pattern[hour]
                            cost = usage * option.hourly_rate * region_mult
                            records.append({
                                'identity/TimeInterval': f"{current_time.strftime('%Y-%m-%d')}T00:00:00Z/{(current_time + timedelta(days=1)).strftime('%Y-%m-%d')}T00:00:00Z",
                                'identity/LineItemId': f"{service_name.lower()}-{hour}-{hash(str(current_time))}",
                                'bill/PayerAccountId': '123456789012',
                                'bill/BillingPeriodStartDate': self.start_date.strftime('%Y-%m-%d'),
                                'bill/BillingPeriodEndDate': self.end_date.strftime('%Y-%m-%d'),
                                'lineItem/UsageAccountId': '123456789012',
                                'lineItem/ProductCode': service_name,
                                'lineItem/UsageType': f"{self.selected_region}:{option.name}",
                                'lineItem/Operation': f"Use{service_name}{option.name.replace(' ', '')}",
                                'lineItem/AvailabilityZone': f"{self.selected_region}a",
                                'lineItem/ResourceId': f"{service_name.lower()}-resource-{hash(option.name)}",
                                'lineItem/UsageStartDate': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                                'lineItem/UsageEndDate': (current_time + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S'),
                                'lineItem/UsageAmount': round(usage, 6),
                                'lineItem/NormalizedUsageAmount': round(usage, 6),
                                'lineItem/UnblendedRate': round(option.hourly_rate * region_mult, 6),
                                'lineItem/UnblendedCost': round(cost, 6),
                                'lineItem/BlendedRate': round(option.hourly_rate * region_mult, 6),
                                'lineItem/BlendedCost': round(cost, 6),
                                'lineItem/LineItemDescription': f"{service.name} {option.name} usage",
                                'product/ProductName': service.name,
                                'product/region': self.selected_region,
                                'pricing/unit': option.unit
                            })
        return pd.DataFrame(records)
