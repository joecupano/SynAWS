# SYNaws - Synthetic AWS Billing Data Generator

This project generates synthetic AWS billing data in CUR 2.0 format. It allows users to select AWS regions and services, configure usage patterns, and download the generated billing data as a CSV file.

## Project Structure

- `services.py`: Defines AWS services and regions with detailed configurations.
- `main.py`: Main Streamlit application integrating service configurations and data generation.
- `data_generator.py`: Generates billing data based on selected services and regions.
- `cur_formatter.py`: Formats the generated data into CUR 2.0 CSV format.

## File Descriptions

### services.py

Defines AWS services and regions with detailed configurations.

- **ServiceOption**: Dataclass representing a service option with attributes like name, min_value, max_value, unit, and hourly_rate.
- **AWSService**: Dataclass representing an AWS service with attributes like name, options, and region_multiplier.
- **AWS_SERVICES**: Dictionary defining common AWS services with their configuration options.
- **AWS_REGIONS**: List of available AWS regions.

### main.py

Main Streamlit application integrating service configurations and data generation.

- **get_download_link**: Generates a download link for the CSV file.
- **get_random_services**: Returns a mix of fixed and random services.
- **generate_random_value**: Generates a sensible random value within the option's bounds.
- **main**: Main function setting up the Streamlit page, sidebar, and service configuration tabs. Handles data generation and displays the generated data.

### data_generator.py

Generates billing data based on selected services and regions.

- **BillingDataGenerator**: Class responsible for generating billing data.
  - **__init__**: Initializes the generator with selected services, region, and days.
  - **generate_usage_pattern**: Generates realistic usage patterns with daily and weekly cycles.
  - **generate_data**: Generates billing data and returns it as a pandas DataFrame.

### cur_formatter.py

Formats the generated data into CUR 2.0 CSV format.

- **CURFormatter**: Class responsible for formatting the data.
  - **format_cur_csv**: Formats a DataFrame as a CUR 2.0 CSV string.

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run /home/joe/source/SYNaws/main.py
   ```
2. Select AWS regions and services, configure usage patterns, and generate synthetic billing data.
3. Download the generated billing data as a CSV file.

## Requirements

- Python 3.7+
- Streamlit
- pandas
- numpy

Install the required packages using pip:
```bash
pip install streamlit pandas numpy
```

## License

This project is licensed under the MIT License.