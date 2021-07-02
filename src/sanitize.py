#!/usr/bin/env python3

import pandas as pd
from get_loc import csv_in_loc, csv_out_loc


#Average Temperature Data Frame
df_temperature = pd.read_csv(csv_in_loc('GlobalLandTemperaturesByCountry.csv'), parse_dates=['dt'], date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%d')) \
    .rename(columns={'dt': 'Year'}) \
    .groupby('Country').resample('Y', on='Year').agg({'AverageTemperature': 'mean', 'AverageTemperatureUncertainty': 'mean'}) \
    .reset_index() \
    .reindex(columns=['Year', 'Country', 'AverageTemperature', 'AverageTemperatureUncertainty']) \
    .dropna(axis=0, how='any')
df_temperature['Year'] = df_temperature['Year'].dt.year
df_temperature.to_csv(csv_out_loc('GlobalLandTemperaturesByCountry.csv'), index=False)


#CO2 Emission Data Frame
df_emission = pd.read_csv(csv_in_loc('co2_emission.csv')) \
    .drop(columns=['Code']) \
    .rename(columns={'Entity': 'Country', 'Annual CO₂ emissions (tonnes )': 'CO2Emission'}) \
    .reindex(columns=['Year', 'Country', 'CO2Emission']) \
    .astype({'Year': int, 'CO2Emission': float}) \
    .sort_values(by=['Country', 'Year']) \
    .reset_index(drop=True) \
    .dropna(axis=0, how='any')
df_emission.to_csv(csv_out_loc('co2_emission.csv'), index=False)


#Population Total Data Frame
df_population_total = pd.read_csv(csv_in_loc('population_total.csv')) \
    .rename(columns={'Country Name': 'Country', 'Count': 'PopulationCount'}) \
    .reindex(columns=['Year', 'Country', 'PopulationCount']) \
    .astype({'Year': int, 'PopulationCount': int}) \
    .sort_values(by=['Country', 'Year']) \
    .reset_index(drop=True) \
    .dropna(axis=0, how='any')
df_population_total.to_csv(csv_out_loc('population_total.csv'), index=False)


#Population Growth Data Frame
df_population_growth = pd.read_csv(csv_in_loc('population_growth.csv')) \
    .drop(columns=['Country Code', 'Indicator Name', 'Indicator Code']) \
    .rename(columns={'Country Name': 'Country'})
df_population_growth = pd.melt(df_population_growth, id_vars=['Country'], value_vars=df_population_growth.columns.tolist()[1:], var_name='Year', value_name='PopulationGrowth') \
    .astype({'Year': int, 'PopulationGrowth': float}) \
    .sort_values(by=['Country', 'Year']) \
    .reset_index(drop=True) \
    .dropna(axis=0, how='any') \
    .reindex(columns=['Year', 'Country', 'PopulationGrowth'])
df_population_growth.to_csv(csv_out_loc('population_growth.csv'), index=False)


#GDP Data Frame
df_gdp = pd.read_csv(csv_in_loc('gdp.csv')) \
    .drop(columns=['Country Code', 'Indicator Name', 'Indicator Code', 'Unnamed: 65']) \
    .rename(columns={'Country Name': 'Country'})
df_gdp = pd.melt(df_gdp, id_vars=['Country'], value_vars=df_gdp.columns.tolist()[1:], var_name='Year', value_name='GDP') \
    .astype({'Year': int, 'GDP': float}) \
    .sort_values(by=['Country', 'Year']) \
    .reset_index(drop=True) \
    .dropna(axis=0, how='any') \
    .reindex(columns=['Year', 'Country', 'GDP'])
df_gdp.to_csv(csv_out_loc('gdp.csv'), index=False)
