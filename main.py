import streamlit as st
import pandas as pd
import numpy as np
import random
from services import AWS_SERVICES, AWS_REGIONS
from data_generator import BillingDataGenerator
from cur_formatter import CURFormatter
import base64
from datetime import datetime

def get_download_link(csv_string: str) -> str:
    """Generate a download link for the CSV file"""
    b64 = base64.b64encode(csv_string.encode()).decode()
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"aws_billing_data_{date_str}.csv"
    return f'<a href="data:text/csv;base64,{b64}" download="{filename}">Download CSV file</a>'

def get_random_services(num_services: int = 3) -> list:
    """Get a mix of fixed and random services"""
    # Core additional services that should always be available
    core_additional = ['RDS', 'DynamoDB', 'Lambda']

    # Get other services excluding both required (EC2, S3) and core additional services
    other_services = [s for s in AWS_SERVICES.keys() if s not in ['EC2', 'S3'] + core_additional]
    random_additional = random.sample(other_services, min(num_services, len(other_services)))

    # Combine core additional services with random ones
    return core_additional + random_additional

def generate_random_value(option):
    """Generate a sensible random value within the option's bounds"""
    min_val = float(option.min_value)
    max_val = float(option.max_value)

    # For storage/data related options (GB units)
    if option.unit == 'GB':
        # Generate values that lean towards lower range
        return round(random.uniform(min_val, max_val * 0.3), 1)

    # For instance counts
    elif 'instances' in option.name.lower():
        # Usually fewer instances are needed
        return float(random.uniform(min_val, min(max_val, 5)))

    # For request counts
    elif 'requests' in option.unit.lower():
        # Generate values that lean towards middle range
        return float(random.uniform(min_val, max_val * 0.5))

    # Default random generation - return float
    return float(random.uniform(min_val, max_val * 0.2))

def main():
    st.set_page_config(page_title="AWS Billing Data Generator", layout="wide")

    # Add custom CSS
    st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] {
            padding: 0px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
            padding: 0px 4px;
        }
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 12px;
            margin: 0px;
            line-height: 1;
        }
        .stTabs [data-baseweb="tab-list"] button {
            padding: 4px 8px;
            min-height: 30px;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 8px;
        }
        .stTabs [data-baseweb="tab"] div.stMarkdown p {
            font-size: 0.9rem;
            margin: 0.2rem 0;
        }
        .stTabs [data-baseweb="tab"] h1, 
        .stTabs [data-baseweb="tab"] h2,
        .stTabs [data-baseweb="tab"] h3,
        .stTabs [data-baseweb="tab"] h4 {
            font-size: 0.9rem !important;
            margin: 0.3rem 0 !important;
            font-weight: normal !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("AWS Billing Data Generator")
    st.write("Generate synthetic AWS billing data in CUR 2.0 format")

    # Sidebar configuration
    st.sidebar.subheader("1. Global Settings")
    days = st.sidebar.selectbox("Number of days of data to generate", [30, 45, 60, 90])
    num_random_services = st.sidebar.slider("Number of additional random services per region", 1, 5, 3)

    # Region selection
    st.sidebar.subheader("2. Select Regions")
    selected_regions = {}
    for region in AWS_REGIONS:
        selected_regions[region] = st.sidebar.checkbox(f"Region: {region}", key=f"region_{region}")

    # Only show service configuration if at least one region is selected
    active_regions = [region for region, selected in selected_regions.items() if selected]

    if not active_regions:
        st.warning("Please select at least one region from the sidebar to configure services.")
        return

    # Main content area for service configuration
    st.header("Service Configuration")
    st.write("Configure services for selected regions")

    selected_services_by_region = {}

    # Create tabs for selected regions
    tabs = st.tabs(active_regions)

    for region, tab in zip(active_regions, tabs):
        with tab:
            st.markdown(f"Region: {region}")
            selected_services = {}

            # Required services (EC2 and S3)
            st.markdown("Required Services")

            # Add random values checkbox for required services
            use_random_required = st.checkbox("Generate random values for required services", 
                                          key=f"{region}_random_required")

            col1, col2 = st.columns(2)

            # EC2 Configuration
            with col1:
                st.markdown("Amazon EC2")
                selected_services['EC2'] = {}
                for option in AWS_SERVICES['EC2'].options:
                    # Generate random value if checkbox is checked
                    default_value = generate_random_value(option) if use_random_required else float(option.min_value)
                    value = st.number_input(
                        f"EC2 - {option.name} ({option.unit})",
                        min_value=float(option.min_value),
                        max_value=float(option.max_value),
                        value=default_value,
                        step=0.1 if 'GB' in option.unit or 'seconds' in option.unit.lower() else 1.0,
                        key=f"{region}_EC2_{option.name}"
                    )
                    if value > 0:
                        selected_services['EC2'][option.name] = value

            # S3 Configuration
            with col2:
                st.markdown("Amazon S3")
                selected_services['S3'] = {}
                for option in AWS_SERVICES['S3'].options:
                    # Generate random value if checkbox is checked
                    default_value = generate_random_value(option) if use_random_required else float(option.min_value)
                    value = st.number_input(
                        f"S3 - {option.name} ({option.unit})",
                        min_value=float(option.min_value),
                        max_value=float(option.max_value),
                        value=default_value,
                        step=0.1 if 'GB' in option.unit or 'seconds' in option.unit.lower() else 1.0,
                        key=f"{region}_S3_{option.name}"
                    )
                    if value > 0:
                        selected_services['S3'][option.name] = value

            # Random Additional Services
            st.markdown("Additional Services")
            random_services = get_random_services(num_random_services)

            # First show all service enable/disable checkboxes
            enabled_services = {}
            for service_name in random_services:
                enabled_services[service_name] = st.checkbox(
                    f"Enable {service_name}", 
                    key=f"{region}_{service_name}_enable"
                )

            # Then show configurations for enabled services
            if any(enabled_services.values()):
                for service_name, is_enabled in enabled_services.items():
                    if is_enabled:
                        st.markdown(f"**{service_name} Configuration**")
                        service = AWS_SERVICES[service_name]

                        # Initialize the service in selected_services if enabled
                        if service_name not in selected_services:
                            selected_services[service_name] = {}

                        # Add random values option for this service
                        use_random = st.checkbox(
                            "Generate random values", 
                            key=f"{region}_{service_name}_random"
                        )

                        # Create columns for the service options
                        num_options = len(service.options)
                        cols = st.columns(min(num_options, 2))  # Max 2 columns

                        for idx, option in enumerate(service.options):
                            with cols[idx % 2]:  # Alternate between columns
                                # Always convert numeric values to float for consistency
                                default_value = float(generate_random_value(option)) if use_random else (
                                    float(option.min_value)
                                )

                                # Always use float for number_input
                                value = st.number_input(
                                    f"{option.name} ({option.unit})",
                                    min_value=float(option.min_value),
                                    max_value=float(option.max_value),
                                    value=default_value,
                                    step=0.1 if 'GB' in option.unit or 'seconds' in option.unit.lower() else 1.0,
                                    key=f"{region}_{service_name}_{option.name}"
                                )
                                if value > 0:
                                    selected_services[service_name][option.name] = value

            selected_services_by_region[region] = selected_services

    # Generate button
    if st.button("Generate Billing Data"):
        if not any(selected_services_by_region.values()):
            st.error("Please configure at least one service in any selected region")
            return

        with st.spinner("Generating billing data..."):
            all_records = []
            progress_bar = st.progress(0)

            # Generate data for each region
            for idx, (region, services) in enumerate(selected_services_by_region.items()):
                if services:
                    generator = BillingDataGenerator(services, region, days)
                    df = generator.generate_data()
                    all_records.append(df)
                progress_bar.progress((idx + 1) / len(selected_services_by_region))

            if all_records:
                # Combine all regional data
                final_df = pd.concat(all_records, ignore_index=True)

                # Format as CUR CSV
                formatter = CURFormatter()
                csv_string = formatter.format_cur_csv(final_df)

                # Display download link
                st.markdown(get_download_link(csv_string), unsafe_allow_html=True)

                # Display preview
                st.subheader("Data Preview")
                st.dataframe(final_df.head())

                # Display summary
                st.subheader("Summary Statistics")
                total_cost = final_df['lineItem/UnblendedCost'].sum()
                st.write(f"Total Cost: ${total_cost:,.2f}")

                # Cost by Region
                region_costs = final_df.groupby('product/region')['lineItem/UnblendedCost'].sum()
                st.write("Cost by Region:")
                st.bar_chart(region_costs)

                # Cost by Service
                service_costs = final_df.groupby('lineItem/ProductCode')['lineItem/UnblendedCost'].sum()
                st.write("Cost by Service:")
                st.bar_chart(service_costs)

if __name__ == "__main__":
    main()