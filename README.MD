# SYNaws - Synthetic AWS Billing Data Generator
This document provides an overview of how the SYNaws project works, including the purpose and functionality of each file in the project. It is intended for developers who want to understand or contribute to the project.

## Overview
SYNaws is a Python-based application that generates synthetic AWS billing data in CUR 2.0 format. It uses **Streamlit** for the user interface, allowing users to configure AWS regions and services, generate synthetic billing data, and download it as a CSV file.

## Quick start
```
docker-build.sh
docker-run.sh
```
Start web browser and connect to http://localhost:8501 or IP address:8501 of server

## Project Structure
### 1. **Main Application Files**

#### `main.py`
- **Purpose**: The entry point of the application. It provides the Streamlit-based user interface for configuring services, selecting regions, and generating billing data.
- **Key Functions**:
  - `get_download_link`: Generates a download link for the generated CSV file.
  - `get_random_services`: Selects a mix of fixed and random AWS services for configuration.
  - `generate_random_value`: Generates random values for service options within their defined bounds.
  - `main`: Sets up the Streamlit interface, handles user input, and integrates with the data generator and formatter.

### 2. **Data Generation**
#### `data_generator.py`
- **Purpose**: Generates synthetic billing data based on user-selected services, regions, and usage patterns.
- **Key Class**:
  - `BillingDataGenerator`: 
    - **`__init__`**: Initializes the generator with selected services, region, and the number of days for data generation.
    - **`generate_usage_pattern`**: Creates realistic usage patterns with daily and weekly cycles.
    - **`generate_data`**: Generates billing data as a pandas DataFrame.

### 3. **Data Formatting**
#### `cur_formatter.py`
- **Purpose**: Formats the generated billing data into the AWS CUR 2.0 CSV format.
- **Key Class**:
  - `CURFormatter`:
    - **`format_cur_csv`**: Ensures the correct column order and converts the DataFrame into a CSV string.

### 4. **Service Definitions**
#### `services.py`
- **Purpose**: Defines AWS services, their configuration options, and region-specific pricing multipliers.
- **Key Components**:
  - `ServiceOption`: A dataclass representing a service option (e.g., name, min/max values, unit, hourly rate).
  - `AWSService`: A dataclass representing an AWS service with its options and region multipliers.
  - `AWS_SERVICES`: A dictionary of predefined AWS services and their configurations.
  - `AWS_REGIONS`: A list of supported AWS regions.

### 5. **Validation Utilities**
#### `utils/validator_cmdline.py`
- **Purpose**: Validates the generated CSV file against the AWS CUR 2.0 format.
- **Key Function**:
  - `validate_csv`: Checks for required columns, data types, and value ranges in the CSV file.

#### `utils/synawsdataverifier.py`
- **Purpose**: Verifies the integrity of AWS billing data, including cost calculations and unique identifiers.
- **Key Features**:
  - Checks for missing columns, negative/zero costs, and duplicate line item IDs.
  - Generates unique IDs for duplicate entries.

#### `utils/synawsdatavalidator.py`
- **Purpose**: Compares AWS billing data with Apptio data for validation and visualization.
- **Key Features**:
  - Validates total spend, compute cost trends, and top spending drivers.
  - Generates bar charts for visual comparisons.

### 6. **Docker Configuration**
#### `Dockerfile`
- **Purpose**: Defines the Docker image for the application.
- **Key Steps**:
  - Uses the `python:3.11-slim` base image.
  - Installs dependencies from `requirements.txt`.
  - Copies the application code into the container.
  - Exposes port `8501` for the Streamlit application.

#### `docker-build.sh`
- **Purpose**: A shell script to build the Docker image.
- **Command**:
  ```bash
  docker build -t aws-billing-data-generator .
  ```

#### `docker-run.sh`
- **Purpose**: A shell script to run the Docker container.
- **Command**:
  ```bash
  docker run -p 8501:8501 aws-billing-data-generator
  ```

### 7. **Dependencies**
#### `requirements.txt`
- **Purpose**: Lists the Python dependencies required for the project.
- **Dependencies**:
  - `streamlit`: For the web-based user interface.
  - `pandas`: For data manipulation.
  - `numpy`: For numerical computations.

### 8. **Documentation**
#### `README.MD`
- **Purpose**: Provides an overview of the project, including usage instructions and requirements.
- **Key Sections**:
  - Project description.
  - File descriptions.
  - Usage instructions.
  - Installation requirements.

## How It Works
1. **User Interface**:
   - The user interacts with the Streamlit interface in `main.py` to configure AWS regions and services.
   - Users can specify usage patterns or generate random values for service options.

2. **Data Generation**:
   - The `BillingDataGenerator` in `data_generator.py` generates synthetic billing data based on the user's configuration.

3. **Data Formatting**:
   - The `CURFormatter` in `cur_formatter.py` formats the generated data into the AWS CUR 2.0 CSV format.

4. **Validation**:
   - The utilities in the `utils` folder validate the generated data for correctness and integrity.

5. **Docker Deployment**:
   - The application can be containerized using the `Dockerfile` and deployed using the provided shell scripts.
