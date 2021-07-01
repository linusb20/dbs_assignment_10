#!/usr/bin/env python3

import sqlite3
import pandas as pd
from os import path

def csv_loc(fname):
    return path.abspath(path.join(path.dirname(__file__), path.pardir, 'export', fname)) 

df_population_total = pd.read_csv(csv_loc('population_total.csv'), usecols=['Year', 'Country', 'PopulationCount'], dtype={'Year': int, 'PopulationCount': int})

con = sqlite3.connect(':memory:')
cur = con.cursor()

df_population_total.to_sql('population_total', con)

cur.execute("SELECT * FROM population_total WHERE year = :year AND country = :country", {'year': 2001, 'country': 'Germany'})
print(cur.fetchall())

con.close()
