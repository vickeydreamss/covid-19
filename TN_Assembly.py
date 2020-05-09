# Import libraries
import pandas as pd
import numpy as np
import math
import fiona
import geopandas as gpd
import json

from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, NumeralTickFormatter
from bokeh.palettes import brewer
from bokeh.models import ColumnDataSource
from bokeh.io.doc import curdoc
from bokeh.models import Slider, HoverTool, Select
from bokeh.layouts import widgetbox, row, column
from bokeh.transform import dodge
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'

output_file("Assembly.html")

fp = r'C:\Users\mmm\PycharmProjects\covid-19\maps-master\assembly-constituencies\India_AC.shp'

India_assembly = gpd.read_file(fp)
print(India_assembly.head())
#India_assembly.to_excel("assembly_geo.xlsx")
TN = India_assembly[India_assembly.ST_NAME == 'TAMIL NADU']
print(TN.dtypes)
TN1 = TN.to_json()
json_data = json.dumps(TN1)
geosource = GeoJSONDataSource(geojson = json_data)


#Define a sequential multi-hue color palette.
palette = brewer['YlGnBu'][8]
#Reverse color order so that dark blue is highest obesity.
#palette = palette[::-1]
#Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 10000, nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels = {'5000': '>5000'}

#Add hover tool
hover = HoverTool(tooltips = [ ('Assembly:','@AC_NAME')])
#Create color bar.
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
#Create figure object.
p = figure(title = 'Tamil Nadu Assembly Details', plot_height = 800 , plot_width = 850, toolbar_location = None, tools = [hover])
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
#Add patch renderer to figure.
p.patches('xs','ys', source = geosource,
          line_color = 'black', line_width = 0.25, fill_alpha = 0.5)
#Specify layout
p.add_layout(color_bar, 'below')
show(p)