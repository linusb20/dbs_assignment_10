#!/usr/bin/env python3

import sqlite3
import pandas as pd
from get_loc import db_loc

con = sqlite3.connect(db_loc('project.db'))

df_all = pd.read_sql("""
SELECT 
    year, 
    country, 
    population_count, 
    population_growth, 
    co2_emission, 
    average_temperature, 
    average_temperature_uncertainty, 
    gdp
FROM year_country
    JOIN population
        ON year_country.id = population.year_country_id
    JOIN emission
        ON year_country.id = emission.year_country_id
    JOIN temperature
        ON year_country.id = temperature.year_country_id
    JOIN gdp
        ON year_country.id = gdp.year_country_id
""", con)
