#!/usr/bin/env python3

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, Panel, Tabs
from itertools import cycle
from random import choice
from get_df import df_all

country_options = df_all['country'].unique().tolist()
country_init = choice(country_options)

source = ColumnDataSource(data=df_all[df_all['country'] == country_init])

select = Select(title='Select Country', value=country_init, options=country_options)
def update_country(attrname, old, new):
    source.data = df_all[df_all['country'] == select.value]
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
for attr in [a for a in df_all.columns.tolist() if a not in ['country', 'year']]:
    s = create_figure(title=f'{attr} over Time in {country_init}', x_axis_label='Time', y_axis_label=attr)
    figures[attr] = s
    s.line('year', attr, source=source, line_width=2, color=next(colors))
    tabs.append(Panel(child=s, title=attr))

layout = column(
    select,
    Tabs(tabs=tabs)
)

curdoc().add_root(layout)
curdoc().title = "DBS Projekt"
