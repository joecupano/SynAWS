from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ServiceOption:
    name: str
    min_value: float
    max_value: float
    unit: str
    hourly_rate: float

@dataclass
class AWSService:
    name: str
    options: List[ServiceOption]
    region_multiplier: Dict[str, float]

# Define common AWS services with their configuration options
AWS_SERVICES = {
    'EC2': AWSService(
        name='Amazon Elastic Compute Cloud',
        options=[
            ServiceOption('t3.micro instances', 0, 20, 'instances', 0.0104),
            ServiceOption('t3.small instances', 0, 10, 'instances', 0.0208),
            ServiceOption('t3.medium instances', 0, 5, 'instances', 0.0416),
            ServiceOption('EBS GP2 Storage', 0, 1000, 'GB', 0.10),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.05, 'eu-west-1': 1.1,
            'ap-southeast-1': 1.15, 'ap-northeast-1': 1.20, 'sa-east-1': 1.25,
            'ca-central-1': 1.08, 'eu-central-1': 1.12, 'ap-south-1': 1.18,
            'af-south-1': 1.22, 'me-south-1': 1.28, 'ap-east-1': 1.21
        }
    ),
    'S3': AWSService(
        name='Amazon Simple Storage Service',
        options=[
            ServiceOption('Standard Storage', 0, 5000, 'GB', 0.023),
            ServiceOption('Intelligent-Tiering Storage', 0, 5000, 'GB', 0.0225),
            ServiceOption('GET Requests', 0, 1000000, 'requests', 0.0000004),
            ServiceOption('PUT Requests', 0, 100000, 'requests', 0.000005),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.02, 'eu-west-1': 1.07,
            'ap-southeast-1': 1.12, 'ap-northeast-1': 1.15, 'sa-east-1': 1.20,
            'ca-central-1': 1.05, 'eu-central-1': 1.08, 'ap-south-1': 1.14,
            'af-south-1': 1.18, 'me-south-1': 1.22, 'ap-east-1': 1.16
        }
    ),
    'RDS': AWSService(
        name='Amazon Relational Database Service',
        options=[
            ServiceOption('db.t3.micro instances', 0, 5, 'instances', 0.017),
            ServiceOption('db.t3.small instances', 0, 3, 'instances', 0.034),
            ServiceOption('Storage (GP2)', 0, 1000, 'GB', 0.115),
            ServiceOption('Backup Storage', 0, 500, 'GB', 0.095),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.03, 'eu-west-1': 1.12,
            'ap-southeast-1': 1.18, 'ap-northeast-1': 1.22, 'sa-east-1': 1.28,
            'ca-central-1': 1.10, 'eu-central-1': 1.15, 'ap-south-1': 1.20,
            'af-south-1': 1.25, 'me-south-1': 1.30, 'ap-east-1': 1.24
        }
    ),
    'Lambda': AWSService(
        name='AWS Lambda',
        options=[
            ServiceOption('Requests', 0, 1000000, 'requests', 0.0000002),
            ServiceOption('Compute (GB-seconds)', 0, 400000, 'GB-seconds', 0.0000166667),
            ServiceOption('Provisioned Concurrency', 0, 100, 'GB-hours', 0.015),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.01, 'eu-west-1': 1.05,
            'ap-southeast-1': 1.08, 'ap-northeast-1': 1.10, 'sa-east-1': 1.15,
            'ca-central-1': 1.03, 'eu-central-1': 1.06, 'ap-south-1': 1.09,
            'af-south-1': 1.12, 'me-south-1': 1.14, 'ap-east-1': 1.11
        }
    ),
    'CloudWatch': AWSService(
        name='Amazon CloudWatch',
        options=[
            ServiceOption('Custom Metrics', 0, 100, 'metrics', 0.3),
            ServiceOption('API Requests', 0, 100000, 'requests', 0.0000012),
            ServiceOption('Dashboard', 0, 10, 'dashboards', 3.0),
            ServiceOption('Logs Ingested', 0, 1000, 'GB', 0.50),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.0, 'eu-west-1': 1.03,
            'ap-southeast-1': 1.05, 'ap-northeast-1': 1.06, 'sa-east-1': 1.08,
            'ca-central-1': 1.02, 'eu-central-1': 1.04, 'ap-south-1': 1.05,
            'af-south-1': 1.07, 'me-south-1': 1.08, 'ap-east-1': 1.06
        }
    ),
    'DynamoDB': AWSService(
        name='Amazon DynamoDB',
        options=[
            ServiceOption('Write Capacity Units', 0, 1000, 'WCU', 0.00065),
            ServiceOption('Read Capacity Units', 0, 1000, 'RCU', 0.00013),
            ServiceOption('Storage', 0, 1000, 'GB', 0.25),
            ServiceOption('Backup Storage', 0, 500, 'GB', 0.10),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.0, 'eu-west-1': 1.04,
            'ap-southeast-1': 1.06, 'ap-northeast-1': 1.08, 'sa-east-1': 1.12,
            'ca-central-1': 1.02, 'eu-central-1': 1.05, 'ap-south-1': 1.07,
            'af-south-1': 1.10, 'me-south-1': 1.11, 'ap-east-1': 1.09
        }
    ),
    'ELB': AWSService(
        name='Elastic Load Balancing',
        options=[
            ServiceOption('Application Load Balancer', 0, 5, 'hours', 0.0225),
            ServiceOption('Network Load Balancer', 0, 3, 'hours', 0.0225),
            ServiceOption('Processed Bytes', 0, 1000, 'GB', 0.008),
            ServiceOption('LCU-hours', 0, 100, 'LCU', 0.006),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.02, 'eu-west-1': 1.08,
            'ap-southeast-1': 1.12, 'ap-northeast-1': 1.15, 'sa-east-1': 1.20,
            'ca-central-1': 1.05, 'eu-central-1': 1.10, 'ap-south-1': 1.14,
            'af-south-1': 1.18, 'me-south-1': 1.22, 'ap-east-1': 1.16
        }
    ),
    'CloudFront': AWSService(
        name='Amazon CloudFront',
        options=[
            ServiceOption('Data Transfer Out', 0, 1000, 'GB', 0.085),
            ServiceOption('Requests (HTTPS)', 0, 1000000, 'requests', 0.0000012),
            ServiceOption('Shield Advanced', 0, 1, 'protection', 3000.0),
            ServiceOption('Custom SSL Certificates', 0, 5, 'certificates', 600.0),
        ],
        region_multiplier={
            'us-east-1': 1.0, 'us-west-2': 1.0, 'eu-west-1': 1.0,
            'ap-southeast-1': 1.0, 'ap-northeast-1': 1.0, 'sa-east-1': 1.0,
            'ca-central-1': 1.0, 'eu-central-1': 1.0, 'ap-south-1': 1.0,
            'af-south-1': 1.0, 'me-south-1': 1.0, 'ap-east-1': 1.0
        }  # CloudFront pricing is usually consistent across regions
    ),
}

AWS_REGIONS = [
    'us-east-1', 'us-west-2', 'ca-central-1', 'eu-west-1', 'eu-central-1',
    'ap-southeast-1', 'ap-northeast-1', 'ap-south-1', 'ap-east-1', 'sa-east-1',
    'me-south-1', 'af-south-1'
]