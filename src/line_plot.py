#!/usr/bin/env python3

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select
from itertools import cycle
from random import choice
from get_df import df_all

country_options = df_all['country'].unique().tolist()
country_init = choice(country_options)

source = ColumnDataSource(data=df_all[df_all['country'] == country_init])

select = Select(title='Select Country', value=country_init, options=country_options)
def update_country(attrname, old, new):
    source.data = df_all[df_all['country'] == select.value]
select.on_change('value', update_country)

def create_figure(**kwargs):
    p = figure(**kwargs, sizing_mode='scale_both')
    p.title_location = 'above'
    p.title.align ='center'
    p.title.text_font_size = '25px'
    p.title.background_fill_color = 'darkgrey'
    p.title.text_color = 'white'
    p.toolbar.logo = None
    return p

colors = cycle(palette)

s1 = create_figure(title='Population Size over Time', x_axis_label='Time', y_axis_label='y')
s1.line('year', 'PopulationCount', source=source, legend_label='Population Size', line_width=2, color=next(colors))

s2 = create_figure(title='Population Growth over Time', x_axis_label='Time', y_axis_label='y')
s2.line('year', 'PopulationGrowth', source=source, legend_label='PopulationGrowth', line_width=2, color=next(colors))

s3 = create_figure(title='CO2 Emission over Time', x_axis_label='Time', y_axis_label='y')
s3.line('year', 'CO2Emission', source=source, legend_label='CO2Emission', line_width=2, color=next(colors))

s4 = create_figure(title='Average Temperature over Time', x_axis_label='Time', y_axis_label='y')
s4.line('year', 'AverageTemperature', source=source, legend_label='Average Temperature', line_width=2, color=next(colors))

s5 = create_figure(title='GDP over Time', x_axis_label='Time', y_axis_label='y')
s5.line('year', 'GDP', source=source, legend_label='GDP', line_width=2, color=next(colors))


layout = layout(
    [
        [select],
        [s1, s2], 
        [s3, s4],
        [s5],
    ]
)

curdoc().add_root(layout)
curdoc().title = "DBS Projekt"
