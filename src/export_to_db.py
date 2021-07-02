#!/usr/bin/env python3

import sqlite3
import pandas as pd
from functools import reduce
from get_loc import csv_out_loc, db_loc

df_population_total = pd.read_csv(csv_out_loc('population_total.csv'), usecols=['Year', 'Country', 'PopulationCount'], dtype={'Year': int, 'PopulationCount': int})
df_population_growth = pd.read_csv(csv_out_loc('population_growth.csv'), usecols=['Year', 'Country', 'PopulationGrowth'], dtype={'Year': int, 'PopulationGrowth': float})
df_emission = pd.read_csv(csv_out_loc('co2_emission.csv'), usecols=['Year', 'Country', 'CO2Emission'], dtype={'Year': int, 'CO2Emission': float})
df_temperature = pd.read_csv(csv_out_loc('GlobalLandTemperaturesByCountry.csv'), usecols=['Year', 'Country', 'AverageTemperature', 'AverageTemperatureUncertainty' ], dtype={'Year': int, 'AverageTemperature': float, 'AverageTemperatureUncertainty': float})
df_gdp = pd.read_csv(csv_out_loc('gdp.csv'), usecols=['Year', 'Country', 'GDP'], dtype={'Year': int, 'GDP': float})

# Merge all dataframes on 'Year' and 'Country'
to_merge = [df_population_total, df_population_growth, df_emission, df_temperature, df_gdp]
df_all = reduce(lambda left,right: pd.merge(left,right,on=['Year', 'Country']), to_merge)

db_tables = {
    'year_country': df_all[['Year', 'Country']].rename_axis("id", axis=0).rename(columns={'Year': 'year', 'Country': 'country'}),
    'population': df_all[['PopulationGrowth', 'PopulationCount']].rename_axis("year_country_id", axis=0).rename(columns={'PopulationGrowth': 'population_growth', 'PopulationCount': 'population_count'}),
    'emission': df_all[['CO2Emission']].rename_axis("year_country_id", axis=0).rename(columns={'CO2Emission': 'co2_emission'}),
    'temperature': df_all[['AverageTemperature', 'AverageTemperatureUncertainty']].rename_axis("year_country_id", axis=0).rename(columns={'AverageTemperature': 'average_temperature', 'AverageTemperatureUncertainty': 'average_temperature_uncertainty'}),
    'gdp': df_all[['GDP']].rename_axis("year_country_id", axis=0).rename(columns={'GDP': 'gdp'}),
}

con = sqlite3.connect(db_loc('project.db'))
cur = con.cursor()

with con:
    cur.execute("""CREATE TABLE year_country (
                id INTEGER PRIMARY KEY, 
                year INTEGER, 
                country TEXT
                )""")
    cur.execute("""CREATE TABLE population (
                population_growth REAL, 
                population_count INTEGER,
                year_country_id INTEGER,
                FOREIGN KEY (year_country_id)
                REFERENCES year_country (id)
                )""")
    cur.execute("""CREATE TABLE emission (
                co2_emission REAL,
                year_country_id INTEGER,
                FOREIGN KEY (year_country_id)
                REFERENCES year_country (id)
                )""")
    cur.execute("""CREATE TABLE temperature (
                average_temperature REAL,
                average_temperature_uncertainty REAL,
                year_country_id INTEGER,
                FOREIGN KEY (year_country_id)
                REFERENCES year_country (id)
                )""")
    cur.execute("""CREATE TABLE gdp (
                gdp REAL,
                year_country_id INTEGER,
                FOREIGN KEY (year_country_id)
                REFERENCES year_country (id)
                )""")

for tablename, dataframe in db_tables.items():
    dataframe.to_sql(tablename, con, if_exists='append')

# cur.execute("SELECT sql FROM sqlite_master WHERE name = 'population'")
# cur.execute("SELECT * FROM year_country WHERE year = :year AND country = :country", {'year': 2001, 'country': 'Germany'})
# cur.execute("SELECT * FROM temperature JOIN year_country ON temperature.year_country_id = year_country.id")
# print(cur.fetchall())

con.close()
