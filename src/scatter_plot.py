#!/usr/bin/env python3

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, RadioGroup, Div
from itertools import cycle
from random import choice
from get_df import df_all

# Select widget
country_options = df_all['country'].unique().tolist()
country_init = choice(country_options)

source = ColumnDataSource(data=df_all[df_all['country'] == country_init])

select = Select(title='Select Country', value=country_init, options=country_options)
def update_country(attrname, old, new):
    source.data = df_all[df_all['country'] == select.value]
    s.title.text = f'Correlation between Attributes for {select.value}'
select.on_change('value', update_country)

# Radio Button widget
attr_options = [a for a in df_all.columns.tolist() if a != 'country']

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
