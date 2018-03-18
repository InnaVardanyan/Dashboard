from plotly.offline import plot
import plotly.graph_objs as go
import pandas as pd
import plotly.figure_factory as ff
import quandl
quandl.ApiConfig.api_key = 've6sEyBx_TAxWi2XfckK'

# Graph 1
y_values1 = ['X8','X7','X6','X5'] 
x_values1 = [15, 55, 15, 20] 
y_values2 = ['X4', 'X3', 'X2', 'X1' ]
x_values2 = [-15, -55, -5, -35]

trace_1 = go.Bar(
    x=x_values1, 
    y=y_values1, 
    name ="<b>Negative</b>", 
    orientation='h',
    opacity = 0.4,
    marker = dict(
        line = dict(
            color = '#002659',
            width = 2.5)
        )
    )

trace_2 = go.Bar(
    x=x_values2, 
    y=y_values2, 
    name ='Positive', 
    orientation ='h',
    opacity = 0.4,
    marker = dict(
        line = dict(
            color = '#d62e00',
            width = 2.5)
        ) 
    )
    
layout1 = dict(title='<b>Correlation of employees probability of churn</b>',
             yaxis= dict(
             title = 'Variable'))

data1 = [trace_1, trace_2]
figure1=dict(data=data1, layout=layout1)

# Graph 2

data = quandl.get("FRED/GDP")
data_graph = data[:]
data.head()

x_values = pd.to_datetime(data_graph.index.values)
y_values = data_graph.Value
trace = go.Scatter(
    x=x_values, 
    y=y_values, 
    mode='lines',
    fill = 'tonexty')

layout2 = dict(title = '<b>US GDP over time</b>')

data2=[trace]
figure2 = dict(data=data2, layout=layout2)

#  Graph 3

data = quandl.get("WIKI/GOOGL")
data_google = data[:]
data.head()

data = quandl.get("BCHARTS/ABUCOINSUSD")
data_bitcoin=data[:]
data.head()

trace1 = go.Box(
    x=data_bitcoin.Open.pct_change(), 
    name = '<b>Bitcoin</b>')

trace2 = go.Box(
    x=data_google.Open.pct_change(), 
    name ='<b>Google</b>')

layout3 = dict(title = "<i>Distribution of Price change</i>")

data3 = [trace1, trace2]
figure3 = dict(data=data3, layout=layout3)

# Graph 4

header = dict(values=['Google','Bitcoin'],
              align = ['left','center'],
              font = dict(color = 'white', size = 12),
              fill = dict(color='#119DFF')
             )

GooglePctChange=data_google.Open.pct_change()
BitcoinPctChange =data_bitcoin.Open.pct_change()

cells = dict(values=[GooglePctChange[1:5].round(3), 
                     BitcoinPctChange[1:5].round(3)],
             align = ['left','center'],
             fill = dict(color=["yellow","white"])
            )
trace4 = go.Table(header=header, cells=cells)

data4 = [trace4]
layout4 = dict(width=500, height=300)
figure4 = dict(data=data4, layout=layout4)

# Graph 5

df = [dict(Task="Task 1", Start='2018-01-01', Finish='2018-02-01', Resource='Idea Validation'),
      dict(Task="Task 2", Start='2018-03-01', Finish='2018-04-15', Resource='Prototyping'),
      dict(Task="Task 3", Start='2018-04-16', Finish='2018-09-30', Resource='Team Formation')]

colors = ['#25a3fc', '#0dba4f', '#f78a1d']

figure5 = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, title = 'Startup Roadmap')