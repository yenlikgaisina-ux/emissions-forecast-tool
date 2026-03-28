# Emissions Forecast Tool

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-ff4b4b?logo=streamlit)
![Data](https://img.shields.io/badge/Data-World%20Bank-orange)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> Interactive tool for exploring national CO2 emissions trends and generating ARIMA forecasts using World Bank Open Data.

---

## Overview

This project downloads CO2 emissions, GDP, and population data from the World Bank API for 10 countries (1990-2022), performs time series analysis, and forecasts emissions trajectories using ARIMA and ETS models. A Streamlit web app provides an interactive interface for country selection, trend comparison, and forecast generation.

---

## Features

- **Live data download** from the World Bank API (free, no registration required)
- **10 countries**: UK, US, China, India, Germany, France, Japan, Brazil, South Africa, Australia
- **Multiple metrics**: total CO2, per capita CO2, GDP, population, carbon intensity
- **ARIMA forecasting** with configurable horizon and 90% confidence intervals
- **Interactive Streamlit dashboard** with Plotly charts

---

## Running the App

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

---

## Running the Notebook

```bash
pip install -r requirements.txt
jupyter notebook notebooks/01_worldbank_pull.ipynb
```

The notebook downloads data from the World Bank API on first run and caches it locally.

---

## Repository Structure

```
emissions-forecast-tool/
|-- app/
|   +-- app.py                          # Streamlit web application
|-- data/
|   +-- clean/                          # Cached downloaded data
|-- notebooks/
|   +-- 01_worldbank_pull.ipynb         # Data pipeline and analysis
|-- requirements.txt
+-- README.md
```

---

## Data Source

| Source | Coverage | Access |
|--------|----------|--------|
| [World Bank Open Data](https://data.worldbank.org/) | 1990-2022, 200+ countries | Free API, no registration |

Indicators used:
- `EN.ATM.CO2E.KT` -- CO2 emissions (kilotonnes)
- `EN.ATM.CO2E.PC` -- CO2 emissions per capita (metric tonnes)
- `NY.GDP.MKTP.CD` -- GDP (current US$)
- `SP.POP.TOTL` -- Population

---

## Skills Demonstrated

`Python` `Pandas` `Statsmodels` `ARIMA` `ETS` `Time Series Forecasting` `Streamlit` `Plotly` `World Bank API` `REST APIs` `Data Visualisation`

---

## Author

**Yenlik Gaisina** | Data & Analytics Consultant

[LinkedIn](https://www.linkedin.com/in/yenlik-gaisina/) | Cambridge Data Science with ML & AI Programme
