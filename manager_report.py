import numpy as np 
import pandas as pd 
import fake_data as data
import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)
# server to be changed to...
server = app.server 


### DATA INPUT AND PARSING ###

manager_name = data.manager["Name"] 

# Variables for Gauge Chart:

# Colorscale based off score
def SetColor(x):
	if (0 <= x < 1):
		return 'rgb(255,69,0)'
	elif (1 <= x < 2):
		return 'rgb(237,118,10)'
	elif (2 <= x < 3):
		return 'rgb(216,151,23)'
	elif (3 <= x < 4):
		return 'rgb(189,180,37)'
	elif (4 <= x <= 5):
		return 'rgb(154,205,50))'

# base_chart and meter_chart defined here:
# https://plot.ly/python/gauge-charts/
base_chart = {
	'values': [4, 1, 1, 1, 1, 1, 1],
	'labels': ['-', '0', '1', '2', '3', '4', '5'],
	'domain': {'x': [0, .48]},
	'marker': {'colors': ['rgb(255, 255, 255)']*7},
	'type': 'pie',
	'direction': 'clockwise',
	'rotation': 108,
	'showlegend': False,
	'hoverinfo': 'none',
	'textinfo': 'label',
	'textposition': 'outside'}
meter_chart = {
	'values': [5, data.misc["Burn_Out"], 5 - data.misc["Burn_Out"]],
	'sort':False,
	'marker': {
		'colors': [
			'rgb(255, 255, 255)',
			SetColor(data.misc["Burn_Out"]),
			'rgb(220, 220, 220)']},
	'domain': {"x": [0, 0.48]},
	'hole': .6,
	'type': 'pie',
	'direction': 'clockwise',
	'rotation': 90,
	'showlegend': False,
	'textinfo': 'none',
	'hoverinfo': 'none'}

### APP LAYOUT ###

app.layout = html.Div([ #is an overarching Div necessary? 
	
	#Header
	html.Div([
		html.H1('Report for ' + manager_name)],
		style={'border':'2px blue solid'}), 
	html.Div(['A MainStay report on managerial effectiveness'],
		style={'border':'2px red solid'}),
	
	#Leadership 
	html.Div([
		html.H2('Leadership')],
		style={'border':'2px blue solid'}),
	html.Div(
		className='row',
		style={'border':'2px red solid'},
		children=[
		html.Div(
			style={'border':'2px red solid'},
			className='four columns',
			children=[
			dcc.Graph(
				id = 'leadership_radial',
				figure = go.Figure(
					data = [
						go.Scatterpolar(
							# theta and r lists must repeat first element to join the trace
							theta=list(data.leadership.keys())+[list(data.leadership.keys())[0]],
							r=list(data.leadership.values())+[list(data.leadership.values())[0]],
							# Can't find a cleaner way to display hoverinfo.
							# hoverinfo='r' shows 'r:3' vs hoverinfo='text' shows '3'
							# I assume you want the latter, just have to define text=r
							text=list(data.leadership.values())+[list(data.leadership.values())[0]],
							hoverinfo='text',
							name='Leadership',
							fill='toself',
							opacity=0.5
						)],
					layout=
						go.Layout(
							polar=dict(radialaxis=dict(range=[0,5])))
				))
			]),
		html.Div(
			# Looking into how to set height=100% of parent div
			style={'border':'2px red solid'},
			className='eight columns',
			children=[
			dcc.Markdown('''

#### 12-Column Layout

The 12 column layout makes the graph quite small when the window shrinks.

Thinking of fixing the graph size and having this text area scale with the page.

Added temporary borders to help visualize divs.''')])
	]),

	#Execution
	html.Div([
		html.H2('Execution')],
		style={'border':'2px blue solid'}),
	html.Div(
		className='row',
		style={'border':'2px red solid'},
		children=[
		html.Div(
			style={'border':'2px red solid','display':'inline-block','width':'550px'},
			children=[
			dcc.Graph(
				id = 'execution_radial',
				figure = go.Figure(
					data = [
						go.Scatterpolar(
							# list comp replaces underscores with spaces for graph labels
							theta=[x.replace('_',' ') for x in list(data.execution.keys())+[list(data.execution.keys())[0]]],
							r=list(data.execution.values())+[list(data.execution.values())[0]],
							text=list(data.execution.values())+[list(data.execution.values())[0]],
							hoverinfo='text',
							name='Execution',
							fill='toself',
							opacity=0.5
						)],
					layout=
						go.Layout(
							polar=dict(radialaxis=dict(range=[0,5])))
				))
			]),
		html.Div(
			style={'border':'2px red solid','display':'inline-block','vertical-align':'top'},
			children=[
			dcc.Markdown('''

#### Set Graph Width

Graph size stays the same but text moves below if text + graph width exceeds that of the page.

Added temporary borders to help visualize divs.''')])
	]),

	#Team Building
	html.Div([
		html.H2("Team Building"),
		dcc.Graph(
			id = 'team_radial',
			figure = go.Figure(
				data = [
					go.Scatterpolar(
						theta=[x.replace('_',' ') for x in list(data.team_building.keys())+[list(data.team_building.keys())[0]]],
						r=list(data.team_building.values())+[list(data.team_building.values())[0]],
						text=list(data.team_building.values())+[list(data.team_building.values())[0]],
						hoverinfo='text',
						name='Team Building',
						fill='toself',
						opacity=0.5
					)],
				layout=
					go.Layout(
						polar=dict(radialaxis=dict(range=[0,5])))
			))
	]),

	#People Developemnt 
	html.Div([
		html.H2("People Development"),
		dcc.Graph(
			id = 'people_radial',
			figure = go.Figure(
				data = [
					go.Scatterpolar(
						theta=[x.replace('_',' ') for x in list(data.people_development.keys())+[list(data.people_development.keys())[0]]],
						r=list(data.people_development.values())+[list(data.people_development.values())[0]],
						text=list(data.people_development.values())+[list(data.people_development.values())[0]],
						hoverinfo='text',
						name='People Development',
						fill='toself',
						opacity=0.5
					)],
				layout=
					go.Layout(
						polar=dict(radialaxis=dict(range=[0,5])))
			))
	]),

	# Misc Metrics
	html.Div([
		html.H3('Burn-Out')],
		style={'border':'2px blue solid'}),
	html.Div(
		className='row',
		style={'border':'2px red solid'},
		children=[
			html.Div(
				style={'border':'2px red solid'},
				className='four columns',
				children=[
				dcc.Graph(
					id = 'burnout_dial',
					figure = go.Figure(
						data = [base_chart, meter_chart],
						layout=
							go.Layout(
								annotations=[{
									'xref': 'paper',
									'yref': 'paper',
									'x': 0.22,
									'y': 0.6,
									'text': '{}'.format(data.misc["Burn_Out"]),
									'font':{'size':30},
									'showarrow':False}])
					)
				)
			]),
			html.Div(
				style={'border':'2px red solid'},
				className='eight columns',
				children=[
				dcc.Markdown('''

#### Gauge Chart

Haven't gotten around to making this look good yet.''')])
	]),

	html.Div([
		html.H3("MicroManagement"),
		html.P(data.misc["Micromanagement"]),

		html.H3("Employee Opinion"),
		html.P(data.misc["Employee_Opinion"])
		])

], 
	style={'marginLeft':'8px', 'marginRight':'8px', 'marginTop':'8px'})


### CALLBACK FUNCTIONS ###




### RUN APP ###

if __name__ == '__main__':
    app.run_server()

