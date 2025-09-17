# Earthquake Monitoring and Analysis

## Project Overview

This project is an integrated, automated system for monitoring and analyzing global earthquake data. The system transforms complex, raw geospatial data into clear and valuable insights, helping to enhance public awareness and preparedness for seismic events.

## How It Works

The system is built on the principle of a **Data Pipeline** using the **ETL** methodology (Extract, Transform, Load).

-   **Extract:** Real-time earthquake data is collected from a trusted source (USGS API).
-   **Transform:** The raw data is processed and cleaned to ensure accuracy and integrity.
-   **Load:** The organized data is stored in a specialized geographic database (PostGIS).

## Key Features

-   **Automated Data Collection:** The system runs automatically to collect the latest data daily.
-   **Advanced Spatial Queries:** Leverages PostGIS to perform complex queries on geographic data.
-   **Interactive Map:** Visualizes the processed data on an interactive map for easy public access and understanding.

## Tools & Technologies

-   **Python:** The primary language for the project.
-   **PostgreSQL + PostGIS:** The database used for storing spatial data.
-   **USGS API:** The official data source for earthquake information.
-   **Folium:** A Python library for creating interactive map visualizations.

## Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

Ensure you have Python and PostgreSQL with the PostGIS extension installed on your system.

### 2. Installation

Install all the necessary libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt


3. Run the Pipeline
Execute the pipeline.py script to collect, process, and store the data in the database.

Bash

python pipeline.py
4. Generate the Map
After the data is loaded, run the map_app.py script to generate the interactive earthquake_map.html file.

Bash

python map_app.py
5. View the Map
Open the earthquake_map.html file in your web browser.
