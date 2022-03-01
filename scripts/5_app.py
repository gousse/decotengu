# Import required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import html
from dash import dcc
from dash import no_update
from dash.dependencies import Input, Output, State
import decotengu
import matplotlib.pyplot as plt


class DiveProfile:
    depth       = 0
    bottom_time = 0
    gf_low      = 0.8
    gf_high     = 0.85
    o2 = 21

    def __init__(self, depth=40, bottom_time=20):
        self.df             = pd.DataFrame(columns=['time','phase','depth','abs_p','gf','tissues'])
        # self.df.index.name  ='time'
        self.o2             = o2
        # self.depth          = depth
        # self.bottom_time    = bottom_time
        self.engine         = decotengu.Engine()
  
        print(self.__class__.__name__,'is constructed')

    def calculate(self, depth, bottom_time):
        self.engine.model.gf_low = self.gf_low
        self.engine.model.gf_high= self.gf_high
        print("calculating profile for {} m depth, bottom_time {} min".format(depth,bottom_time))
        print(self.engine.model)
        print(self.engine.model.gf_low, self.engine.model.gf_high)
        profile = list(self.engine.calculate(depth, bottom_time))
        for step in profile:
            print(step)
            self.df.loc[self.df.shape[0]] = {'time': step.time,
                                             'depth':  (-self.engine._to_depth(step.abs_p)),
                                             'phase':  step.phase,
                                             'abs_p':  step.abs_p,
                                             'gf':     step.data[1],
                                             'tissues':step.data[0]}

    def add_gas(self, *args):
        self.engine.add_gas(*args)   # add_gas(depth, o2, he=0, travel=False)
        print("added gas",args)

    def print_df(self):
        print(self.df)

    def plot_dive(self):
        print(self.__class__.__name__," ploting")
        print("ploting")
        print(self.df[['time','depth']])

    def steps(self):
        return self.df[['time','phase','depth','abs_p','gf']]

depth = 35
bottom_time = 40
gf_low = 0.8
gf_high = 0.85
o2 = 21

dp = DiveProfile()
dp.add_gas(0, o2)
dp.calculate(depth, bottom_time)
dp.print_df()
dp.plot_dive()
print(dp.steps())

#steps = dash_table.DataTable(dp.steps().to_dict('records'),[{"name": i, "id": i} for i in dp.steps().columns])
df = dp.steps()
df.head()
print(df.to_dict())
print(df.to_dict('records'))
print(df.columns)
a=[{'name':i, 'id':i} for i in df.columns]
print(a)