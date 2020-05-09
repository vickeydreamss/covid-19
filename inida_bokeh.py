# Import libraries
import pandas as pd
import numpy as np
import geopandas as gpd
import json
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.models import ColumnDataSource
import requests

output_file("test1.html")


df=pd.read_excel("state.xlsx")


source = ColumnDataSource(df)
x_r = list(df.State)
x_t = list(df.Confirmed_Cases)
#print(x_r)
p1 = figure(x_range = x_r, plot_width = 1200, plot_height = 600, title = "India - State Wise Confirmed Cases")
p1.vbar(x = 'State', top = 'Confirmed_Cases', width = 0.7, source = source)
p1.xaxis.major_label_orientation = 0.8

#print(source.data)

show(p1)