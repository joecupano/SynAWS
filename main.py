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
    core_additional = ['RDS', 'DynamoDB', 'Lambda']
    other_services = [s for s in AWS_SERVICES.keys() if s not in ['EC2', 'S3'] + core_additional]
    random_additional = random.sample(other_services, min(num_services, len(other_services)))
    return core_additional + random_additional

def generate_random_value(option):
    """Generate a sensible random value within the option's bounds"""
    min_val = float(option.min_value)
    max_val = float(option.max_value)
    if option.unit == 'GB':
        return round(random.uniform(min_val, max_val * 0.3), 1)
    elif 'instances' in option.name.lower():
        return float(random.uniform(min_val, min(max_val, 5)))
    elif 'requests' in option.unit.lower():
        return float(random.uniform(min_val, max_val * 0.5))
    return float(random.uniform(min_val, max_val * 0.2))

def main():
    st.set_page_config(page_title="AWS Billing Data Generator", layout="wide")
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

    st.sidebar.subheader("1. Global Settings")
    days = st.sidebar.selectbox("Number of days of data to generate", [30, 45, 60, 90])
    num_random_services = st.sidebar.slider("Number of additional random services per region", 1, 5, 3)

    st.sidebar.subheader("2. Select Regions")
    selected_regions = {}
    for region in AWS_REGIONS:
        selected_regions[region] = st.sidebar.checkbox(f"Region: {region}", key=f"region_{region}")

    active_regions = [region for region, selected in selected_regions.items() if selected]

    if not active_regions:
        st.warning("Please select at least one region from the sidebar to configure services.")
        return

    st.header("Service Configuration")
    st.write("Configure services for selected regions")

    selected_services_by_region = {}
    tabs = st.tabs(active_regions)

    for region, tab in zip(active_regions, tabs):
        with tab:
            st.markdown(f"Region: {region}")
            selected_services = {}
            st.markdown("Required Services")
            use_random_required = st.checkbox("Generate random values for required services", key=f"{region}_random_required")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Amazon EC2")
                selected_services['EC2'] = {}
                for option in AWS_SERVICES['EC2'].options:
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

            with col2:
                st.markdown("Amazon S3")
                selected_services['S3'] = {}
                for option in AWS_SERVICES['S3'].options:
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

            st.markdown("Additional Services")
            random_services = get_random_services(num_random_services)
            enabled_services = {}
            for service_name in random_services:
                enabled_services[service_name] = st.checkbox(f"Enable {service_name}", key=f"{region}_{service_name}_enable")

            if any(enabled_services.values()):
                for service_name, is_enabled in enabled_services.items():
                    if is_enabled:
                        st.markdown(f"**{service_name} Configuration**")
                        service = AWS_SERVICES[service_name]
                        if service_name not in selected_services:
                            selected_services[service_name] = {}
                        use_random = st.checkbox("Generate random values", key=f"{region}_{service_name}_random")
                        num_options = len(service.options)
                        cols = st.columns(min(num_options, 2))
                        for idx, option in enumerate(service.options):
                            with cols[idx % 2]:
                                default_value = float(generate_random_value(option)) if use_random else float(option.min_value)
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

    if st.button("Generate Billing Data"):
        if not any(selected_services_by_region.values()):
            st.error("Please configure at least one service in any selected region")
            return

        with st.spinner("Generating billing data..."):
            all_records = []
            progress_bar = st.progress(0)
            for idx, (region, services) in enumerate(selected_services_by_region.items()):
                if services:
                    generator = BillingDataGenerator(services, region, days)
                    df = generator.generate_data()
                    all_records.append(df)
                progress_bar.progress((idx + 1) / len(selected_services_by_region))

            if all_records:
                final_df = pd.concat(all_records, ignore_index=True)
                formatter = CURFormatter()
                csv_string = formatter.format_cur_csv(final_df)
                st.markdown(get_download_link(csv_string), unsafe_allow_html=True)
                st.subheader("Data Preview")
                st.dataframe(final_df.head())
                st.subheader("Summary Statistics")
                total_cost = final_df['lineItem/UnblendedCost'].sum()
                st.write(f"Total Cost: ${total_cost:,.2f}")
                region_costs = final_df.groupby('product/region')['lineItem/UnblendedCost'].sum()
                st.write("Cost by Region:")
                st.bar_chart(region_costs)
                service_costs = final_df.groupby('lineItem/ProductCode')['lineItem/UnblendedCost'].sum()
                st.write("Cost by Service:")
                st.bar_chart(service_costs)

if __name__ == "__main__":
    main()