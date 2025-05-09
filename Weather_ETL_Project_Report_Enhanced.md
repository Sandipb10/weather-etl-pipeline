
# Weather Data ETL Pipeline Project

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![API](https://img.shields.io/badge/OpenWeatherMap-API-orange)

## 📌 Project Description
This project involves building an **ETL (Extract, Transform, Load)** pipeline that fetches weather data for multiple cities from the OpenWeatherMap API, transforms the raw JSON data into a structured format, and loads it into an SQLite database. Additionally, the data is visualized over time to track temperature changes for each city using interactive charts.

## 🛠️ Tools & Technologies
- **Python** — For scripting and automation
- **Pandas** — Data manipulation and transformation
- **SQLite** — Local SQL database for storage
- **SQLAlchemy** — Database connection and querying
- **Matplotlib & Plotly** — Data visualization
- **OpenWeatherMap API** — Data source for weather information

## 🔄 ETL Process Overview

### 1️⃣ Extract
The script sends an HTTP GET request to the OpenWeatherMap API for the specified cities. Weather data such as temperature, humidity, and descriptions are fetched and returned in JSON format.

### 2️⃣ Transform
The JSON response is transformed into a structured format using Pandas. The relevant fields extracted include:
- City name
- Temperature
- Humidity
- Weather description
- Wind speed
- Timestamp

These fields are then organized into a DataFrame for easy manipulation.

### 3️⃣ Load
The transformed data is then loaded into a local **SQLite database** (`weather_data.db`). If the table already exists, new rows are appended.

The database schema is as follows:

| Column Name           | Data Type | Description                     |
|------------------------|-----------|---------------------------------|
| city                  | TEXT      | Name of the city                |
| temperature           | REAL      | Temperature in Celsius          |
| humidity              | INTEGER   | Humidity percentage             |
| weather_description   | TEXT      | Description of weather          |
| wind_speed            | REAL      | Wind speed in m/s               |
| timestamp             | TEXT      | Timestamp of data retrieval     |

## 📊 Visualization
The project now features enhanced visualization using **Plotly** for interactive and visually appealing charts.

### 1️⃣ Improved Temperature Over Time Chart
- **Interactive Line Chart:** Displays temperature variations for each city.
- **Hover Features:** Displays city name, timestamp, and temperature.
- **Zoom and Pan:** Easily explore specific time ranges.
- **Toggle Cities:** Turn city lines on/off for focused analysis.

### 📝 Code Snippet for Improved Visualization
```python
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Connect to the database
engine = create_engine("sqlite:///weather_data.db")
df = pd.read_sql("SELECT * FROM weather", con=engine)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values(by='timestamp', inplace=True)

# Plotly interactive line plot
fig = px.line(df, x='timestamp', y='temperature', color='city',
              title='🌤️ Temperature Over Time by City',
              labels={'timestamp': 'Time', 'temperature': 'Temperature (°C)', 'city': 'City'})

# Enhance layout
fig.update_layout(
    title_font_size=20,
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
    legend_title="Cities",
    template="plotly_dark",
    hovermode="x unified"
)
fig.show()
```

---

## 🗂️ Code Structure
```
├── KPI.py
├── weather_data.db
└── README.md
```

- `KPI.py`: Main ETL and visualization script.
- `weather_data.db`: SQLite database storing weather records.
- `README.md`: Project documentation and setup instructions.

---

## 🚀 How to Run
1. Clone the repository:
```bash
git clone https://github.com/your-username/weather-etl-pipeline.git
```

2. Navigate to the project directory:
```bash
cd weather-etl-pipeline
```

3. Install dependencies:
```bash
pip install requests pandas sqlalchemy matplotlib plotly
```

4. Run the ETL script:
```bash
python KPI.py
```

5. Weather data will be stored in `weather_data.db` and the visualization will be displayed.

---

## 🔄 Future Improvements
- Implement error logging for better debugging.
- Add more cities and countries.
- Extend visualization to include humidity and wind speed.
- Deploy on AWS Lambda for real-time weather tracking.

---

## ✅ Conclusion
This ETL pipeline demonstrates the ability to extract real-time weather data, transform it into meaningful information, and load it into a structured database format. It also provides visual insights, making it a solid foundation for building real-time weather monitoring applications.

---


Below is a sample output of the visualization:

![Weather Data Visualization](path_to_your_image.png)

