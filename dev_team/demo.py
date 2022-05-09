import os
import csv
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd

class TreeData():

    def __init__(self, row):

        self.id = row[0]
        self.coordinates = row[1:3]
        self.health = row[3:]

def read_data(fileName):

    if not os.path.exists(fileName):
        return None

    trees = []

    with open(fileName, "r") as f:

        reader = csv.reader(f)
        for row in reader:
            temp = TreeData(row)
            trees.append(temp)

    return trees


fileName = "kapapala_tracking.csv"
trees = read_data(fileName)

timeSteps = len(trees[0].health)
print(timeSteps)

df = pd.read_csv(fileName)
print(df.head())

timePeriod = widgets.IntSlider(
    value=1,
    min=1,
    max=timeSteps,
    step=1,
    description='Time Period',
    continuous_update=False
)

container = widgets.HBox(children=[timePeriod])

trace1 = go.Scatter(x=df['POINT_X'],
                    y=df['POINT_Y'],
                    mode='markers',
                    marker=dict(color=df.iloc[timePeriod.value],
                                colorscale='Viridis',
                                showscale=True
                                )
                    )
g = go.FigureWidget(data=[trace1],
                    layout=go.Layout(title=dict(text='Rapid Ohia Death')),
                    )

def response(change):
        if True:
            filter_list = [i and j and k for i, j, k in
                           zip(df['month'] == month.value, df['carrier'] == textbox.value,
                               df['origin'] == origin.value)]
            temp_df = df[filter_list]

        else:
            filter_list = [i and j for i, j in
                           zip(df['carrier'] == 'DL', df['origin'] == origin.value)]
            temp_df = df[filter_list]

        #m = dict(color=df.iloc[timePeriod.value], colorscale='Viridis', showscale=True)
        print(timePeriod.value)
        with g.batch_update():
            #g.data[0].marker = m
            g.layout.xaxis.title = 'Delay in Minutes'
            g.layout.yaxis.title = 'Number of Delays'
        trace1.show()

timePeriod.observe(response, names="value")
widgets.VBox([container,
              g])
