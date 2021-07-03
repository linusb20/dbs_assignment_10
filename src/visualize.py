#!/usr/bin/env python3

import pandas as pd
import math
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.plotting import figure
from bokeh.palettes import Dark2_5 as palette
from bokeh.models import ColumnDataSource, Select, RadioGroup, Slider, Div, Panel, Tabs, CheckboxGroup
from itertools import cycle
from random import choice, sample
from get_df import df_all


def create_figure(**kwargs):
    p = figure(**kwargs)
    p.title_location = 'above'
    p.title.align ='center'
    p.title.text_font_size = '15px'
    p.title.background_fill_color = 'darkgrey'
    p.title.text_color = 'white'
    p.toolbar.logo = None
    return p

def create_hbar():
    year_options = df_all['year'].unique().tolist()
    year_init = choice(year_options)

    source = ColumnDataSource(data=df_all[df_all['year'] == year_init])

    slider = Slider(start=min(year_options), end=max(year_options), value=year_init, step=1, title="Select Year")
    def update_year(attrname, old, new):
        source.data = df_all[df_all['year'] == slider.value]
        s.title.text = f'{select.value} in {slider.value}'
    slider.on_change('value', update_year)

    attr_options = [a for a in df_all.columns.tolist() if a not in ['country', 'year']]
    attr_init = choice(attr_options)
    select = Select(title='Select Attribute', value=attr_init, options=attr_options)
    def update_attr(attrname, old, new):
        hbar_plot.glyph.right= select.value
        s.title.text = f'{select.value} in {slider.value}'
        s.xaxis.axis_label = select.value
    select.on_change('value', update_attr)

    colors = cycle(palette)

    s = create_figure(title=f'{attr_init} in {year_init}', y_range=source.data['country'], x_axis_label=attr_init, y_axis_label='Countries', plot_height=len(df_all['country'].unique())*10)
    # s.xaxis.formatter.use_scientific = False
    hbar_plot = s.hbar(y='country', left=0, right=attr_init, height=0.5, source=source, color=next(colors))

    layout = column(
        row(children=[select, slider]),
        s
    ) 
    return layout

def create_scatter():
    country_options = df_all['country'].unique().tolist()
    country_init = choice(country_options)

    source = ColumnDataSource(data=df_all[df_all['country'] == country_init])

    select = Select(title='Select Country', value=country_init, options=country_options)
    def update_country(attrname, old, new):
        source.data = df_all[df_all['country'] == select.value]
        s.title.text = f'Correlation between Attributes for {select.value}'
    select.on_change('value', update_country)

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
    h_attr1 = Div(text='<h3>Select Attribute for X Axis</h3>')
    h_attr2 = Div(text='<h3>Select Attribute for Y Axis</h3>')

    colors = cycle(palette)

    s = create_figure(title=f'Correlation between Attributes for {country_init}', x_axis_label=attr_options[attr1_init], y_axis_label=attr_options[attr2_init])
    s.axis.formatter.use_scientific = False
    # s.axis.major_label_orientation = math.pi / 4
    scatter_plot = s.circle(attr_options[attr1_init], attr_options[attr2_init], source=source, color=next(colors))

    layout = column(
        select, 
        row(
            column(h_attr1, attr1_radio), 
            column(h_attr2, attr2_radio)
        ),
        s
    ) 
    return layout

def create_line():
    country_options = df_all['country'].unique().tolist()
    country_init = choice(country_options)

    source = ColumnDataSource(data=df_all[df_all['country'] == country_init])

    select = Select(title='Select Country', value=country_init, options=country_options)
    def update_country(attrname, old, new):
        source.data = df_all[df_all['country'] == select.value]
        for attr, f in figures.items(): f.title.text = f'{attr} over Time in {select.value}'
    select.on_change('value', update_country)

    attr_options = [a for a in df_all.columns.tolist() if a not in ['country', 'year']]
    attr_init = sample(range(len(attr_options)), 2)

    checkbox = CheckboxGroup(labels=attr_options, active=attr_init)

    def create_layout_children(active):
        return [row(checkbox, select)] + [row(*[figures[attr_options[a]] for a in active[i:i+2]]) for i in range(0, len(active), 2)]

    def update_attr(attrname, old, new):
        layout.children = create_layout_children(checkbox.active)
    checkbox.on_change('active', update_attr)

    colors = cycle(palette)
    figures = dict()
    for attr in attr_options:
        s = create_figure(title=f'{attr} over Time in {country_init}', x_axis_label='Time', y_axis_label=attr)
        s.line('year', attr, source=source, line_width=2, color=next(colors))
        figures[attr] = s

    layout = column(children=create_layout_children(attr_init))
    return layout 


def create_line_tabs():
    country_options = df_all['country'].unique().tolist()
    country_init = choice(country_options)

    source = ColumnDataSource(data=df_all[df_all['country'] == country_init])

    select = Select(title='Select Country', value=country_init, options=country_options)
    def update_country(attrname, old, new):
        source.data = df_all[df_all['country'] == select.value]
        for attr, f in figures.items(): f.title.text = f'{attr} over Time in {select.value}'
    select.on_change('value', update_country)

    colors = cycle(palette)

    figures = dict() 
    tabs = []
    for attr in [a for a in df_all.columns.tolist() if a not in ['country', 'year']]:
        s = create_figure(title=f'{attr} over Time in {country_init}', x_axis_label='Time', y_axis_label=attr)
        s.axis.formatter.use_scientific = False
        # s.yaxis.major_label_orientation = math.pi / 4 
        s.line('year', attr, source=source, line_width=2, color=next(colors))
        figures[attr] = s
        tabs.append(Panel(child=s, title=attr))

    layout = column(
        select,
        Tabs(tabs=tabs)
    )
    return layout


tabs = []
tabs.append(Panel(child=create_hbar(), title='Bar Plot'))
tabs.append(Panel(child=create_scatter(), title='Scatter Plot'))
tabs.append(Panel(child=create_line(), title='Line Plot'))
tabs.append(Panel(child=create_line_tabs(), title='Line Plot With Tabs'))

title = 'DBS Projekt'
header = Div(text=f'<h1>{title}</h1>')

layout = column(
    header,
    Tabs(tabs=tabs)
) 

curdoc().add_root(layout)
curdoc().title = title
