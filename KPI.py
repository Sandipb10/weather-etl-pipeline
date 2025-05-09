import requests
import pandas as pd
import datetime
import sqlite3
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# --- STEP 1: Extract ---
def extract_weather_data(api_key, city="Sydney"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Data successfully extracted from API for {city}.")
        return response.json()
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

# --- STEP 2: Transform ---
def transform_weather_data(raw_data):
    main = raw_data.get("main", {})
    weather = raw_data.get("weather", [{}])[0]
    wind = raw_data.get("wind", {})

    cleaned_data = {
        "city": raw_data.get("name"),
        "temperature": main.get("temp"),
        "humidity": main.get("humidity"),
        "weather_description": weather.get("description"),
        "wind_speed": wind.get("speed"),
        "timestamp": datetime.datetime.now()
    }

    df = pd.DataFrame([cleaned_data])
    print("Data transformed into structured format.")
    return df

# --- STEP 3: Load ---
def load_to_sqlite(df, db_name="weather_data.db"):
    conn = sqlite3.connect(db_name)
    df.to_sql("weather", conn, if_exists="append", index=False)
    conn.close()
    print("Data loaded to SQL database.")

# --- Run the ETL process ---
def run_etl(api_key, cities):
    print("Starting ETL process...")
    for city in cities:
        try:
            data = extract_weather_data(api_key, city)
            df = transform_weather_data(data)
            load_to_sqlite(df)
        except Exception as e:
            print(f"Failed for {city}: {e}")
    print("ETL process complete.")

# --- Visualization ---
def visualize_weather_data():
    engine = create_engine("sqlite:///weather_data.db")
    
    # Average temp per city
    df_avg = pd.read_sql("SELECT city, AVG(temperature) as avg_temp FROM weather GROUP BY city", con=engine)
    print(df_avg)
    
    # Plot all temperature records
    df = pd.read_sql("SELECT * FROM weather", con=engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)
    
    plt.figure(figsize=(10, 5))
    for city in df['city'].unique():
        city_df = df[df['city'] == city]
        plt.plot(city_df['timestamp'], city_df['temperature'], label=city)
    
    plt.title("Temperature Over Time by City")
    plt.xlabel("Timestamp")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.tight_layout()
    plt.show()

# --- Entry point ---
if __name__ == "__main__":
    API_KEY = "607a27778f485868677652b903d20c18"  # Replace with your own key if needed
    cities = ["Melbourne", "Sydney", "Brisbane", "Perth", "Adelaide"]
    
    run_etl(API_KEY, cities)
    visualize_weather_data()

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
              labels={
                  'timestamp': 'Time',
                  'temperature': 'Temperature (°C)',
                  'city': 'City'
              })

# Improve layout
fig.update_layout(
    title_font_size=20,
    xaxis_title="Time",
    yaxis_title="Temperature (°C)",
    legend_title="Cities",
    template="plotly_dark",
    hovermode="x unified"
)

fig.show()

