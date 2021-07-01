#!/usr/bin/env python3

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, RadioGroup, Div
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


# Select widget
country_options = df_all['Country'].unique().tolist()
country_init = choice(country_options)

source = ColumnDataSource(data=df_all[df_all['Country'] == country_init])

select = Select(title='Select Country', value=country_init, options=country_options)
def update_country(attrname, old, new):
    source.data = df_all[df_all['Country'] == select.value]
    s.title.text = f'Correlation between Attributes for {select.value}'
select.on_change('value', update_country)

# Radio Button widget
attr_options = [a for a in df_all.columns.tolist() if a != 'Country']

attr1_init = choice(range(len(attr_options)))
attr2_init = choice(range(len(attr_options)))
attr1_radio = RadioGroup(labels=attr_options, active=attr1_init)
attr2_radio = RadioGroup(labels=attr_options, active=attr2_init)

def update_attr1(attrname, old, new):
    scatter_plot.glyph.x = attr_options[attr1_radio.active]
    s.xaxis.axis_label = attr_options[attr1_radio.active]
attr1_radio.on_change('active', update_attr1)

def update_attr2(attrname, old, new):
    scatter_plot.glyph.y = attr_options[attr2_radio.active]
    s.yaxis.axis_label =  attr_options[attr2_radio.active]
attr2_radio.on_change('active', update_attr2)

# Header for Radio Buttons
h_attr1 = Div(text="""<h3>Select Attribute for X Axis</h3>""")
h_attr2 = Div(text="""<h3>Select Attribute for Y Axis</h3>""")

def create_figure(**kwargs):
    p = figure(**kwargs, sizing_mode='scale_both')
    p.title_location = 'above'
    p.title.align ='center'
    p.title.text_font_size = '25px'
    p.title.background_fill_color = 'darkgrey'
    p.title.text_color = 'white'
    p.toolbar.logo = None
    # p.toolbar.autohide = True
    return p

colors = cycle(palette)

s = create_figure(title=f'Correlation between Attributes for {country_init}', x_axis_label=attr_options[attr1_init], y_axis_label=attr_options[attr2_init])
scatter_plot = s.circle(attr_options[attr1_init], attr_options[attr2_init], source=source, color=next(colors))

layout = column(
    select, 
    row(
        column(h_attr1, attr1_radio), 
        column(h_attr2, attr2_radio)
    ),
    s
) 

curdoc().add_root(layout)
curdoc().title = "DBS Projekt"
