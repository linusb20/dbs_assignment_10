#!/usr/bin/env python3

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, Panel, Tabs
from os import path
from functools import reduce
from itertools import cycle
from random import choice

project_root_dir = path.join(path.dirname(__file__), path.pardir) 
csv_location = path.join(project_root_dir, 'export') 

def csv_loc(fname):
    return path.abspath(path.join(csv_location, fname)) 

df_population_total = pd.read_csv(csv_loc('population_total.csv'), usecols=['Year', 'Country', 'PopulationCount'], dtype={'Year': int, 'PopulationCount': int})
df_population_growth = pd.read_csv(csv_loc('population_growth.csv'), usecols=['Year', 'Country', 'PopulationGrowth'], dtype={'Year': int, 'PopulationGrowth': float})
df_emission = pd.read_csv(csv_loc('co2_emission.csv'), usecols=['Year', 'Country', 'CO2Emission'], dtype={'Year': int, 'CO2Emission': float})
df_temperature = pd.read_csv(csv_loc('GlobalLandTemperaturesByCountry.csv'), usecols=['Year', 'Country', 'AverageTemperature', 'AverageTemperatureUncertainty' ], dtype={'Year': int, 'AverageTemperature': float, 'AverageTemperatureUncertainty': float})
df_gdp = pd.read_csv(csv_loc('gdp.csv'), usecols=['Year', 'Country', 'GDP'], dtype={'Year': int, 'GDP': float})

# Merge all dataframes on 'Year' and 'Country'
to_merge = [df_population_total, df_population_growth, df_emission, df_temperature, df_gdp]
df_all = reduce(lambda left,right: pd.merge(left,right,on=['Year', 'Country']), to_merge)

country_options = df_all['Country'].unique().tolist()
country_init = choice(country_options)

source = ColumnDataSource(data=df_all[df_all['Country'] == country_init])

select = Select(title='Select Country', value=country_init, options=country_options)
def update_country(attrname, old, new):
    source.data = df_all[df_all['Country'] == select.value]
    for attr, f in figures.items(): f.title.text = f'{attr} over Time in {select.value}'
select.on_change('value', update_country)

def create_figure(**kwargs):
    p = figure(**kwargs, sizing_mode='scale_both')
    p.title_location = 'above'
    p.title.align ='center'
    p.title.text_font_size = '15px'
    p.title.background_fill_color = 'darkgrey'
    p.title.text_color = 'white'
    p.toolbar.logo = None
    p.yaxis.formatter.use_scientific = False
    return p

colors = cycle(palette)

figures = dict() 
tabs = []
for attr in [a for a in df_all.columns.tolist() if a not in ['Country', 'Year']]:
    s = create_figure(title=f'{attr} over Time in {country_init}', x_axis_label='Time', y_axis_label=attr)
    figures[attr] = s
    s.line('Year', attr, source=source, line_width=2, color=next(colors))
    tabs.append(Panel(child=s, title=attr))

layout = column(
    select,
    Tabs(tabs=tabs)
)

curdoc().add_root(layout)
curdoc().title = "DBS Projekt"
