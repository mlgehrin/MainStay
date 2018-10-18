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


### APP LAYOUT ###

app.layout = html.Div([ #is an overarching Div necessary? 
	
	#Header
	html.Div([
		html.H1("Report For " + manager_name), 
		html.P("A MainStay report on managerial effectiveness"),

	]), 
	
	#Leadership 
	html.Div([
		html.H2("Leadership"),
		dcc.Graph(
			id = 'leadership_radial',
			figure = go.Figure(
				data = [
					go.Bar(
						x=list(data.leadership.keys()),
						y=list(data.leadership.values())
		)]))

	]),

	#Execution
	html.Div([ 
		html.H2("Execution"),
		dcc.Graph(
			id = 'execution_radial',
			figure = go.Figure(
				data = [
					go.Bar(
						x=list(data.execution.keys()),
						y=list(data.execution.values())
		)]))
	]),

	#Team Building
	html.Div([
		html.H2("Team Building"),
		dcc.Graph(
			id = 'team_radial',
			figure = go.Figure(
				data = [
					go.Bar(
						x=list(data.team_building.keys()),
						y=list(data.team_building.values())
		)]))
	]),

	#People Developemnt 
	html.Div([
		html.H2("People Development"),
		dcc.Graph(
			id = 'people_radial',
			figure = go.Figure(
				data = [
					go.Bar(
						x=list(data.people_development.keys()),
						y=list(data.people_development.values())
		)]))

	]),

	# Misc Metrics 
	html.Div([
		html.H3("Burn-Out"),
		html.P(data.misc["Burn_Out"]),

		html.H3("MicroManagement"),
		html.P(data.misc["Micromanagement"]),

		html.H3("Employee_Opinion"),
		html.P(data.misc["Employee_Opinion"])
		])

	], 
	style={'marginLeft':'8px', 'marginRight':'8px', 'marginTop':'8px'})


### CALLBACK FUNCTIONS ###



### RUN APP ###

if __name__ == '__main__':
    app.run_server()

