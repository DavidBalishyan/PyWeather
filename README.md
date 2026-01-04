# PyWeather 🌤️

PyWeather is a Python-based data analysis tool designed to fetch, process, and visualize historical weather data. Currently configured for **Yerevan, Armenia**, it leverages the Open-Meteo API to retrieve daily temperature and precipitation records, providing insightful analytics through various plots and statistics.

## 🚀 Features

- **Automated Data Fetching**: Retrieves historical daily weather data (Max/Min Temperature, Precipitation) automatically using the [Open-Meteo API](https://open-meteo.com/).
- **Data Persistence**: Caches downloaded data in `data/weather_data.csv` to avoid unnecessary API calls.
- **Advanced Data Processing**:
  - Calculates daily average temperatures.
  - Computes 7-day rolling averages for trend analysis.
  - Determines temperature anomalies based on monthly means.
- **Rich Visualizations** (saved in `target/`):
  - 📈 **Daily Temperature Trends**: Line graph showing daily temps vs. 7-day rolling average.
  - 📊 **Monthly Rainfall**: Bar chart of average rainfall per month.
  - 🔢 **Temperature Distribution**: Histogram showing the frequency of temperature ranges.
  - 🔥 **Anomaly Heatmap**: A detailed heatmap visualizing temperature anomalies by month and day.

## 🛠️ Prerequisites

- **Python 3.x**
- **Make** (optional, for automated build commands)

## 📦 Installation & Usage

This project includes a **Makefile** to streamline the setup and execution process.

### Using Make (Recommended)

1.  **Run the Project**:
    This will automatically create a virtual environment, install dependencies, and run the analysis.

    ```bash
    make
    ```

2.  **Clean Up**:
    To remove the virtual environment and cached files:
    ```bash
    make clean
    ```

### Manual Setup

If you prefer to run commands manually:

1.  **Create a virtual environment**:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the script**:
    ```bash
    python main.py
    ```

## 📂 Output

After running the script, check the `target/` directory for the generated visualizations:

- `daily_temperature.png`
- `monthly_rainfall.png`
- `temperature_distribution.png`
- `temperature_anomaly_heatmap.png`

Stats will also be printed to the console.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
