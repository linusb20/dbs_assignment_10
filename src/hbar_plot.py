#!/usr/bin/env python3

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, Slider, Div
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

# Slider widget
year_options = df_all['Year'].unique().tolist()
year_init = choice(year_options)

source = ColumnDataSource(data=df_all[df_all['Year'] == year_init])

slider = Slider(start=min(year_options), end=max(year_options), value=year_init, step=1, title="Select Year")
def update_year(attrname, old, new):
    source.data = df_all[df_all['Year'] == slider.value]
    s.title.text = f'{select.value} in {slider.value}'
slider.on_change('value', update_year)

# Select widget
attr_options = [a for a in df_all.columns.tolist() if a not in ['Country', 'Year']]
attr_init = choice(attr_options)
select = Select(title='Select Attribute', value=attr_init, options=attr_options)
def update_attr(attrname, old, new):
    hbar_plot.glyph.right= select.value
    s.title.text = f'{select.value} in {slider.value}'
    s.xaxis.axis_label = select.value
select.on_change('value', update_attr)

def create_figure(**kwargs):
    p = figure(**kwargs, sizing_mode='stretch_both')
    p.title_location = 'above'
    p.title.align ='center'
    p.title.text_font_size = '15px'
    p.title.background_fill_color = 'darkgrey'
    p.title.text_color = 'white'
    p.toolbar.logo = None
    # p.toolbar.autohide = True
    return p

colors = cycle(palette)

s = create_figure(title=f'{attr_init} in {year_init}', y_range=source.data['Country'], x_axis_label=attr_init, y_axis_label='Countries', plot_height=len(df_all['Country'].unique())*10)
hbar_plot = s.hbar(y='Country', left=0, right=attr_init, height=0.5, source=source, color=next(colors))

layout = column(
    row(children=[select, slider]),
    s
) 

curdoc().add_root(layout)
curdoc().title = "DBS Projekt"
