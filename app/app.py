import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Emissions Forecast Tool", layout="wide")
st.title("Emissions Forecast Tool")
st.markdown("Explore CO2 emissions trends and forecasts using World Bank Open Data.")

INDICATORS = {
    'EN.ATM.CO2E.KT': 'co2_kt',
    'EN.ATM.CO2E.PC': 'co2_per_capita',
    'NY.GDP.MKTP.CD': 'gdp_usd',
    'SP.POP.TOTL': 'population',
}

COUNTRIES = {
    'GBR': 'United Kingdom', 'USA': 'United States', 'CHN': 'China',
    'IND': 'India', 'DEU': 'Germany', 'FRA': 'France',
    'JPN': 'Japan', 'BRA': 'Brazil', 'ZAF': 'South Africa', 'AUS': 'Australia',
}


@st.cache_data(ttl=86400)
def load_data():
    """Download emissions data from the World Bank API."""
    frames = []
    for indicator, col_name in INDICATORS.items():
        country_str = ';'.join(COUNTRIES.keys())
        url = f'https://api.worldbank.org/v2/country/{country_str}/indicator/{indicator}'
        params = {'format': 'json', 'per_page': 5000, 'date': '1990:2022'}
        resp = requests.get(url, params=params)
        data = resp.json()
        if len(data) < 2:
            continue
        records = []
        for entry in data[1]:
            if entry['value'] is not None:
                records.append({
                    'country': entry['country']['value'],
                    'country_code': entry['countryiso3code'],
                    'year': int(entry['date']),
                    col_name: float(entry['value']),
                })
        frames.append(pd.DataFrame(records))
    df = frames[0]
    for f in frames[1:]:
        col = [c for c in f.columns if c not in ['country', 'country_code', 'year']][0]
        df = df.merge(f[['country_code', 'year', col]], on=['country_code', 'year'], how='outer')
    return df


df = load_data()

# Sidebar
st.sidebar.header("Settings")
selected = st.sidebar.multiselect(
    "Countries", list(COUNTRIES.values()),
    default=['United Kingdom', 'United States', 'China']
)
metric = st.sidebar.selectbox("Metric", ['co2_kt', 'co2_per_capita', 'gdp_usd'])
metric_labels = {'co2_kt': 'CO2 (kt)', 'co2_per_capita': 'CO2 per capita (t)', 'gdp_usd': 'GDP (US$)'}

# Trend chart
st.subheader("Emissions Trends")
filtered = df[df['country'].isin(selected)].sort_values('year')
fig = px.line(filtered, x='year', y=metric, color='country',
              labels={'year': 'Year', metric: metric_labels.get(metric, metric)})
fig.update_layout(template='plotly_dark')
st.plotly_chart(fig, use_container_width=True)

# Forecast section
st.subheader("Forecast")
forecast_country = st.selectbox("Country to forecast", selected)
forecast_years = st.slider("Forecast horizon (years)", 3, 15, 8)

fc_data = df[df['country'] == forecast_country][['year', 'co2_kt']].dropna().sort_values('year')
if len(fc_data) > 10:
    fc_data = fc_data.set_index('year')
    fc_data.index = pd.PeriodIndex(fc_data.index, freq='Y')

    model = SARIMAX(fc_data['co2_kt'], order=(1, 1, 1), enforce_stationarity=False)
    fit = model.fit(disp=False)
    forecast = fit.get_forecast(steps=forecast_years)
    fc_mean = forecast.predicted_mean
    fc_ci = forecast.conf_int(alpha=0.10)

    fc_df = pd.DataFrame({
        'year': range(fc_data.index[-1].year + 1, fc_data.index[-1].year + 1 + forecast_years),
        'forecast': fc_mean.values / 1e3,
        'lower': fc_ci.iloc[:, 0].values / 1e3,
        'upper': fc_ci.iloc[:, 1].values / 1e3,
    })

    hist_df = pd.DataFrame({
        'year': [p.year for p in fc_data.index],
        'observed': fc_data['co2_kt'].values / 1e3,
    })

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Latest observed (Mt)", f"{fc_data['co2_kt'].iloc[-1]/1e3:.1f}")
    with col2:
        st.metric(f"Forecast {fc_df['year'].iloc[-1]} (Mt)", f"{fc_df['forecast'].iloc[-1]:.1f}")

    import plotly.graph_objects as go
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=hist_df['year'], y=hist_df['observed'],
                              mode='lines', name='Observed', line=dict(color='#388bfd', width=2)))
    fig2.add_trace(go.Scatter(x=fc_df['year'], y=fc_df['forecast'],
                              mode='lines+markers', name='ARIMA Forecast',
                              line=dict(color='#238636', width=2, dash='dash')))
    fig2.add_trace(go.Scatter(
        x=list(fc_df['year']) + list(fc_df['year'][::-1]),
        y=list(fc_df['upper']) + list(fc_df['lower'][::-1]),
        fill='toself', fillcolor='rgba(35,134,54,0.15)',
        line=dict(color='rgba(0,0,0,0)'), name='90% CI'))
    fig2.update_layout(template='plotly_dark',
                       xaxis_title='Year', yaxis_title='CO2 (Mt)',
                       title=f'{forecast_country} CO2 Forecast')
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Insufficient data for forecast")
