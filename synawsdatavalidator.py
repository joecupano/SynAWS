import pandas as pd
import matplotlib.pyplot as plt

# Replace with actual file paths
aws_billing_file = "aws_billing_data_20250226_151146.csv"
apptio_daily_compute_file = "Daily_Compute_Usage.csv"
apptio_total_spend_file = "Total_Spend_By_Account.csv"
apptio_top_spending_file = "Top_Spending_Drivers.csv"

# Load data
df_aws = pd.read_csv(aws_billing_file)
df_daily_compute = pd.read_csv(apptio_daily_compute_file)
df_total_spend = pd.read_csv(apptio_total_spend_file)
df_top_spending = pd.read_csv(apptio_top_spending_file)

# Validate Total Spend
aws_total_spend = df_aws["unblended_cost"].sum()
apptio_total_spend = df_total_spend.iloc[:, -1].sum()

# Validate Daily Compute Cost Trends
aws_compute_cost = df_aws[df_aws["enhanced_service_name"].str.contains("EC2|RDS|Lambda|Compute", na=False)]["unblended_cost"].sum()
apptio_compute_cost = df_daily_compute.iloc[:, -1].sum()

# Validate Top Spending Drivers
aws_top_spending = df_aws.groupby("enhanced_service_name")["unblended_cost"].sum().nlargest(5)
apptio_top_spending = df_top_spending.iloc[:, [-2, -1]]
apptio_top_spending.columns = ["service", "cost"]
apptio_top_spending = apptio_top_spending.groupby("service")["cost"].sum().nlargest(5)

# Create bar chart for Total Spend Comparison
plt.figure(figsize=(8, 5))
plt.bar(["AWS", "Apptio"], [aws_total_spend, apptio_total_spend], color=['blue', 'orange'])
plt.xlabel("Data Source")
plt.ylabel("Total Spend ($)")
plt.title("AWS vs Apptio Total Spend Comparison")
plt.show()

# Create bar chart for Compute Cost Comparison
plt.figure(figsize=(8, 5))
plt.bar(["AWS", "Apptio"], [aws_compute_cost, apptio_compute_cost], color=['blue', 'orange'])
plt.xlabel("Data Source")
plt.ylabel("Compute Cost ($)")
plt.title("AWS vs Apptio Compute Cost Comparison")
plt.show()

# Create bar chart for Top AWS Spending Services
plt.figure(figsize=(10, 5))
plt.barh(aws_top_spending.index, aws_top_spending.values, color='blue')
plt.xlabel("Spending ($)")
plt.ylabel("Service")
plt.title("Top AWS Spending Services")
plt.gca().invert_yaxis()
plt.show()

# Create bar chart for Top Apptio Spending Services
plt.figure(figsize=(10, 5))
plt.barh(apptio_top_spending.index, apptio_top_spending.values, color='orange')
plt.xlabel("Spending ($)")
plt.ylabel("Service")
plt.title("Top Apptio Spending Services")
plt.gca().invert_yaxis()
plt.show()
