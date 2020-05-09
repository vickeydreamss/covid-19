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

output_file("India_Dashboard.html")
fp = r'C:\Users\mmm\Desktop\maps-master\States\Admin2.shp'
sf_india = gpd.read_file(fp)


df=pd.read_excel("state.xlsx")

df =df.rename(columns={'State': 'ST_NM'})

merged = sf_india.merge(df, on = 'ST_NM', how = 'left')
#merged.to_excel("merged.xlsx")
print(merged.columns)

#Read data to json
merged_json = json.loads(merged.to_json())

#Convert to str like object
json_data = json.dumps(merged_json)
geosource = GeoJSONDataSource(geojson = json_data)



palette = brewer['YlGnBu'][8]
palette = palette[::-1]
color_mapper = LinearColorMapper(palette = palette, low = merged['Confirmed_Cases'].min(), high = merged['Confirmed_Cases'].max(), nan_color = '#d9d9d9')
tick_labels = {'5000': '>5000'}

hover = HoverTool(tooltips = [ ('State:','@ST_NM'),('Confirmed_Cases: ','@Confirmed_Cases'), ('Recovered: ', '@Recovered'),('Active_Cases: ', '@Active_Cases')])
color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                     border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

p = figure(title = 'COVID-19 Status Inida', plot_height = 800 , plot_width = 850, toolbar_location = None, tools = [hover])
p.xaxis.visible = False
p.yaxis.visible = False
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

p.patches('xs','ys', source = geosource,fill_color = {'field' :'Confirmed_Cases', 'transform' : color_mapper},
          line_color = 'black', line_width = 0.25, fill_alpha = 1)

p.add_layout(color_bar, 'below')

df=pd.read_excel("state.xlsx")
df = df.sort_values(by = 'Confirmed_Cases', ascending=False)



source = ColumnDataSource(df)
x_r = list(df.State)
x_t = list(df.Confirmed_Cases)

p1 = figure(x_range = x_r, plot_width = 1400, plot_height = 600, title = "India -COVID- 19 State Wise Pareto Chart")

dodge1 = dodge('State', -0.3, range=p1.x_range)
dodge2 = dodge('State', 0.0, range=p1.x_range)
dodge3 = dodge('State', 0.3, range=p1.x_range)

p1.vbar(x = dodge1, top = 'Confirmed_Cases', width = 0.25, source = source, color= 'mediumorchid')
p1.vbar(x = dodge2, top = 'Active_Cases', width = 0.25, source = source, color = 'salmon')
p1.vbar(x = dodge3, top = 'Recovered', width = 0.25, source = source, color = 'springgreen')
p1.xaxis.major_label_orientation = 1.2
tooltips2 = [('Confirmed_Cases: ','@Confirmed_Cases'), ('Active_Cases: ', '@Active_Cases'), ('Recovered: ', '@Recovered')]
p1.add_tools(HoverTool(tooltips=tooltips2))

layout = column(children = [p, p1])
#opening thre html file

show(layout)

 

























