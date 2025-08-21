# 🌍 Earthquake Data Analysis - Last 30 Days

A **Streamlit app** that visualizes earthquake data from the last 30 days. It allows users to explore earthquake locations, magnitudes, significance, and trends over time interactively.

## Features

* **Interactive Map**

  * Earthquakes plotted by location using latitude and longitude.
  * Points sized by magnitude and colored by significance.
  * Hover to see details: magnitude, depth, significance, alert type, magnitude type, depth group, place, date and more!

* **Time Analysis**

  * View the number of earthquakes per day.
  * Filter by date, magnitude, depth, significance, and alerts.

* **Significance vs Magnitude Analysis**

  * Scatter plots showing relationships between earthquake significance and magnitude.

* **Sidebar Filters**

  * Filter by depth group, magnitude type, alert type, and significance range.
  * Filters update the map and charts dynamically.

* **Metrics Overview**

  * Total earthquakes
  * Average magnitude
  * Maximum significance
  * Number of earthquakes with alerts

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/svet-g/earthquake-data-app.git
   cd earthquake-data-app
   ```

2. Install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create a .env file (more in Environment Configuration)

4. Run the extract process:

   ```bash
   python src/extract/extract.py
   ```

5. Run the app:

   ```bash
   streamlit run app.py
   ```

## Environment Configuration

This app requires database connection details to be stored in a `.env` file at the root of the project. Use the following format:

```env
# Source Database Configuration
SOURCE_DB_NAME=
SOURCE_DB_USER=
SOURCE_DB_PASSWORD=
SOURCE_DB_HOST=
SOURCE_DB_PORT=
```

Fill in each value with the appropriate credentials for your source database.
The app will use these environment variables to extract and load earthquake data.

## Data

Data is loaded via the `extract` function from `src.extract.extract`.

The app expects a DataFrame created using the ETL pipeline in https://github.com/svet-g/earthquake-data-etl with at least the following columns:

  * `id`
  * `time` (datetime)
  * `latitude`, `longitude`
  * `mag` (magnitude)
  * `depth`
  * `sig` (significance)
  * `alert`
  * `magType` (magnitude type)
  * `depth_group`
  * `place`

The app automatically filters out earthquakes with magnitude ≤ 0.

## Usage

* Select filters in the sidebar to narrow down your view.
* Switch between tabs:

  1. **Interactive Map** – Explore earthquake locations.
  2. **Time Analysis** – View earthquake trends over time.
  3. **Significance vs Magnitude Analysis** – Compare significance and magnitude.

## Cloud App

The app is also available on the streamlit cloud server at 

## Notes / Tips

Metrics and charts update dynamically based on filters.
Designed for **wide-screen layouts** for best viewing experience.

## Tech Stack

* [Python 3](https://www.python.org/)
* [Streamlit](https://streamlit.io/)
* [Pandas](https://pandas.pydata.org/)
* [Plotly Express](https://plotly.com/python/plotly-express/)