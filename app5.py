import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go 
import quandl
from figures import figure1, figure5

#quandl.ApiConfig.api_key = 'Please insert your API key'

df_GDP=quandl.get("FRED/GDP")

app=dash.Dash()
app.css.append_css({'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
	# First row
	html.Div([
		html.H2(
			children='Homework 5',
			style={'color':'#0091f9', 'fontFamily':'Comic Sans MS', 'textAlign': 'center', 'fontWeight':'bold'}),
		], className='row'),
	# Second row
	html.Div([	
		html.Div([
	    	dcc.RadioItems(
				id='option_in1',
			    options=[
			    {'label':"Employee Churn", 'value':'figure1'},
			    {'label':'Startup RoadMap','value':'figure5'}
			    ],
			    value='figure1')
			    ], className ='three columns'),
	    html.Div([
	        html.Div(id='Graph')
	    		], className = 'nine columns')
			], className='row'),
	# Third row
	html.Div([
		html.Div([
			dcc.Dropdown(
			id='option_in2',
			options=[
			{'label': 'Google', 'value': 'GOOGL'},
			{'label': 'Apple', 'value': 'AAPL'},
			{'label': 'Microsoft', 'value': 'MSFT'},
			{'label': 'IBM', 'value': 'IBM'},
			{'label': 'Amazon', 'value': 'AMZN'},
			],
			multi=True,
			value=['GOOGL', 'AAPL'],
			placeholder= "Please, select a stock" ),
			html.Button(id='submit', n_clicks=0, children='Submit'),
		], className='three columns'),
		html.Div([
			dcc.Graph(id='figure_3')
		], className='six columns'),
		html.Div([
			dcc.Graph(id='figure_4')
		], className='three columns')
	], className='row'),
	#Fourth row
	html.Div([
		dcc.Graph(id='figure_5'),
		dcc.RangeSlider(
			id = 'option_in3',
   			min=0,
    		max=len(df_GDP.index),
    		step=1,
    		value=[0, len(df_GDP.index)])
	], className='ten columns')
])


#Callback for Radio Button
@app.callback(
    Output(component_id='Graph', component_property='children'),
    [Input(component_id='option_in1', component_property='value')]
)

def update_graph_1(graph_type):
    graphs=[]
    if 'figure1' in graph_type:
        graphs.append(html.Div(dcc.Graph(id='figure1', figure=figure1))),

    if 'figure5' in graph_type:
        graphs.append(html.Div(dcc.Graph(id='figure5', figure=figure5)))
        
    return graphs

#Callback for Dropdown/Box Plot
@app.callback(
	Output(component_id='figure_3', component_property='figure'),
	[Input(component_id='submit', component_property='n_clicks')],
	[State(component_id='option_in2', component_property='value')],
)

def update_graph_2(clicks, input_value):
	quandl_input1 = "WIKI/" + input_value[0]
	stock_data1 = quandl.get(quandl_input1)
	quandl_input2 = "WIKI/" + input_value[1]
	stock_data2 = quandl.get(quandl_input2)

	trace1=go.Box(x=stock_data1.Open.pct_change(), name=input_value[0])
	trace2=go.Box(x=stock_data2.Open.pct_change(), name=input_value[1])
	layout3 = dict(title = "<i>Distribution of Price change</i>")
	data3 = [trace1, trace2]
	figure3 = dict(data=data3, layout=layout3)
	return figure3

#Callback for Dropdown/Table
@app.callback(
	Output(component_id='figure_4', component_property='figure'),
	[Input(component_id='submit', component_property='n_clicks')],
	[State(component_id='option_in2', component_property='value')]
)	

def update_graph_3(clicks, input_value):
	quandl_input1 = "WIKI/" + input_value[0]
	stock_data1 = quandl.get(quandl_input1)
	quandl_input2 = "WIKI/" + input_value[1]
	stock_data2 = quandl.get(quandl_input2)

	header = dict(values=[str(input_value[0]), str(input_value[1])],
              align = ['left','center'],
              font = dict(color = 'white', size = 12),
              fill = dict(color='#119DFF')
             )
	cells = dict(values=[stock_data1.Open.pct_change()[1:6].round(3), 
                     stock_data2.Open.pct_change()[1:6].round(3)],
             align = ['left','center'],
             fill = dict(color=["yellow","white"])
            )
	trace = go.Table(header=header, cells=cells)
	data4 = [trace]
	figure4 = dict(data=data4)
	return figure4

#Callback for RangeSlider
@app.callback(
    Output(component_id='figure_5', component_property='figure'),
    [Input(component_id='option_in3', component_property='value')]
)

def update_graph(input_value):
	filtered_df = df_GDP.index[input_value[0]:input_value[1]]
	trace = go.Scatter(
		x=filtered_df,
		y=df_GDP.Value[input_value[0]:input_value[1]], 
		mode='lines', 
		fill='tonexty')
	layout = dict(title = '<b>US GDP over time</b>')
	data=[trace]
	figure = dict(data=data, layout = layout)
	return figure

if __name__=='__main__':
	app.run_server(debug=True)

