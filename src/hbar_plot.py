#!/usr/bin/env python3

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, Slider, Div
from itertools import cycle
from random import choice
from get_df import df_all

# Slider widget
year_options = df_all['year'].unique().tolist()
year_init = choice(year_options)

source = ColumnDataSource(data=df_all[df_all['year'] == year_init])

slider = Slider(start=min(year_options), end=max(year_options), value=year_init, step=1, title="Select Year")
def update_year(attrname, old, new):
    source.data = df_all[df_all['year'] == slider.value]
    s.title.text = f'{select.value} in {slider.value}'
slider.on_change('value', update_year)

# Select widget
attr_options = [a for a in df_all.columns.tolist() if a not in ['country', 'year']]
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

s = create_figure(title=f'{attr_init} in {year_init}', y_range=source.data['country'], x_axis_label=attr_init, y_axis_label='Countries', plot_height=len(df_all['country'].unique())*10)
hbar_plot = s.hbar(y='country', left=0, right=attr_init, height=0.5, source=source, color=next(colors))

layout = column(
    row(children=[select, slider]),
    s
) 

curdoc().add_root(layout)
curdoc().title = "DBS Projekt"
