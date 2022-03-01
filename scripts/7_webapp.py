# Import required libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input,Output, html, dcc, dash_table

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

# Create a dash application
app = Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Application layout
app.layout = html.Div(
    children=[ 
                html.H1('Deco Planification',
                        style={'textAlign':'center','color':'#503D36','font-size':24}), 
                               
                # Create an outer division 1
                html.Div([
                    # Add an division 1.1
                    html.Div([
                        # Create an division for adding dropdown helper text for report type
                        html.Div(
                            [
                            html.H2('% O2:', style={'width':'75px','margin-right': '2em'}),
                            
                            dcc.Input(id='input-o2', 
                                    type='number',
                                    placeholder='O2 value',
                                    value=21,
                                    style={'width':'50px','padding':'3px',
                                    'font-size':'20px','margin-right': '2em'}),
                            ], style={'display':'flex'}
                        ),
                        

                        html.Div(
                            [
                            html.H2('Depth:', style={'width':'75px','margin-right': '2em'}),
                            dcc.Input(id='input-depth', 
                                    type='number',
                                    placeholder='depth in m',
                                    value=40,
                                    style={'width':'50px','padding':'3px','font-size':'20px'}),
                            ], style={'display':'flex'}
                        ),
                        
                        html.Div(
                            [
                            html.H2('Time:', style={'width':'75px','margin-right': '2em'}),
                            dcc.Input(id='input-time', 
                                    type='number',
                                    placeholder='time in min',
                                    value=20,
                                    style={'width':'50px','padding':'3px','font-size':'20px'}),
                            ], style={'display':'flex'}
                        ),

                    # Place them next to each other using the division style
                    ]),
                    
                    # Add next division 1.2
                    html.Div([ ], id='plot1'),
                ], style={'display':'flex'}),
                
                # Add new outer division 2
                html.Div([
                        # Create an division for adding dropdown helper text for choosing year
                        html.Div(
                            [
                            html.H2('Steps:', style={'margin-right': '2em'}),
                            html.Div([], id='steps')
                            ])
                    ]),
            ])                                

@app.callback( [Output('steps','children'),
                Output('plot1','children')
               ],
               [Input('input-o2', 'value'),
                Input('input-depth', 'value'),
                Input('input-time', 'value')],
               )

def show_deco(o2, depth, bottom_time):
    dp = DiveProfile()
    dp.add_gas(0, o2)
    dp.calculate(depth, bottom_time)
    # dp.print_df()
    # dp.plot_dive()
    print(dp.steps())
    # return dp.print_df(), dp.plot_dive()
    dive_fig = px.line(dp.df, x='time', y='depth', title='deco graph')
    old_steps = "{}".format(dp.steps())
    steps = dash_table.DataTable(dp.steps().to_dict('records'),[{"name": i, "id": i} for i in dp.steps().columns])
    return steps, dcc.Graph(figure=dive_fig)


# Run the app
if __name__ == '__main__':
    app.run_server()
