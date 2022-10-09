import numpy as np
import pandas as pd
from warnings import simplefilter
simplefilter("ignore")

from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq

import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.SANDSTONE])



df = pd.read_csv("assets/unemployment analysis.csv")

df2 = df.copy()

df2["total"] = df2.sum(axis = 1)


summed = df.sum()[2:]
leastCovdEffected = pd.DataFrame()
leastCovdEffected["total"] = df[["2019", "2020"]].sum(axis = 1).sort_values()
leastCovdEffected["country_name"] = df["Country Name"]
leastCovdEffected = leastCovdEffected[:5]
 
leastCovidBar = px.bar(leastCovdEffected, y = "country_name", x = "total")
leastCovidBar.update_layout(title="Countries with lease unemployment in 20219-20", xaxis_title = "Unemployment", yaxis_title = "No. of UnEmployment",)
# print(leastCovdEffected[: 5])


totalUnEmp = summed.sum().astype("int64")
unemp10yrs = summed[::-1][:10][::-1].sum().astype("int64")

fig1v2 = px.line(x = summed.index[::-1][:10][::-1], y = summed[::-1][:10][::-1])

unEmpLastYear = summed.iloc[-1].astype("int64")

countries = df["Country Name"].unique()


# dropDownItems = [dbc.DropdownMenuItem(i) for i in countries]


app.layout = html.Div([
	html.Link(rel='stylesheet', href='assets/style.css'),
	html.Link(href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css'),

	html.H1("UnEmployment Data analysis"),
	html.P(["The EDA is based on the Kaggle Dataset ",
			html.A("here", href = "https://www.kaggle.com/datasets/pantanjali/unemployment-dataset", target="_blank")],),

	# html.Div(dbc.Alert(f'No of null values in the Dataset used {df.isnull().sum()[0]}'), className = "close"),


	html.Div([
		dbc.Row([

			dbc.Col([
			
				html.Div([
	
					html.H1(unemp10yrs,),
					html.Span("Un Employment in the Last 10 Years")
					],
					className = "card__style"),
	
				html.Div([
					html.H1(totalUnEmp),
					html.Span("Recorded UnEmployment")
					],
					className = "card__style"),
				
				html.Div([
					html.H1(unEmpLastYear),
					html.Span("UnEmployment Last Year")
					],
					className = "card__style")
				]),

			dbc.Col([

				html.Div([
					
					daq.ToggleSwitch(id = "view-switch", value = False, label = "Switch View"),
					dcc.Graph(id = "unemp-trend"),

					html.Span("UnEmployment was at its worst in 2019, majorly cause due to the world wide pandemic - COVID19,. This cause a lot of people to loose their jobs as business were mostly all closed following the 'SOCIAL DISTANCING' protocol.")

					]),

				]),

			dbc.Col([

				html.Div([
					

					daq.ToggleSwitch(id = "switch-most-emp", value = False, label = "Switch View"),
					dcc.Graph(id = "country-count"),

					]),
				html.Div([
					daq.ToggleSwitch(id = "switch-least-emp", value = False, label = "Switch View"),
					dcc.Graph(id = "country-count2")

					]),

				]),


			dbc.Col([

				html.Div([
					
					dcc.Dropdown(countries, id="country-picker", value= "India"),
		
					dcc.Graph(id = "country-view"),

					html.P("Not most but a slight few coutries like - Qatar, Cambodia, Nigeria and Myanmar had barely or no impact on their UnEmployment rate even during the pandemic."),

					dcc.Graph(figure = leastCovidBar)

					]),

				],),

			]),

		
		]),

	html.Footer([
			"Follow me on -",
			html.A(html.Img(src = "assets/linkedin.gif"), href = "https://www.linkedin.com/in/nitish-kumar-chauhan-9b461b235/", target = "_blank", className = "icons"),
			html.A(html.Img(src = "assets/kaggle.png"), href = "https://www.kaggle.com/purpledmango", target = "_blank", className = "icons"),
			html.A(html.Img(src = "assets/github.gif"), href = "https://www.kaggle.com/purpledmango", target = "_blank", className = "icons"),

		])
	])



@app.callback(Output("unemp-trend", "figure"), Input("view-switch", "value"))
def changeUnEmpGraph(switch):
	if switch == False:
		data = summed[::-1][:10][::-1]

		title = "UnEmployment trend over the last 10yrs"

	elif switch == True:
		data = summed
		title = "UnEmployment since 1991"
	
	fig = px.line(x = data.index, y = data)

	fig.update_layout(title= title, xaxis_title = "Year", yaxis_title = "No. of UnEmployment",)

	fig.update_traces(line_color="#ffa600")
	
	return fig


@app.callback(Output("country-count", "figure"), Input("switch-most-emp", "value"))
def changeUnEmpGraph(switch):
	

	if switch == False:
		data  = df2.sort_values(by = "total", ascending = False)[:5]
		title = "Country with the most UnEmployment since 1991"

	elif switch == True:
		data = df.sort_values(by = "2021", ascending = False)[:5]
		title = "Country with the most UnEmployment"
	fig1 = px.bar(data, y = "Country Name", x = "2021")
	fig1.update_layout(title= title, xaxis_title = "Year", yaxis_title = "No. of UnEmployment",)
	
	return fig1





@app.callback(Output("country-count2", "figure"), Input("switch-least-emp", "value"))
def changeUnEmpGraph(switch):
	if switch == False:
		data  = df2.sort_values(by = "total")[:5]
		title = "Country with the least UnEmployment"

	elif switch == True:
		data  = df.sort_values(by = "2021")[:5]
		title = "Country with the least UnEmployment in 2021"
	fig2 = px.bar(data, y = "Country Name", x = "2021")

	fig2.update_layout(title=title, xaxis_title = "Year", yaxis_title = "No. of UnEmployment",)

	
	return fig2

@app.callback(Output("country-view", "figure"), Input("country-picker", "value"))
def changeUnEmpGraph(key):

	data  = df[df["Country Name"] == key]


	index = (data.columns[2:])

	values = (data.values[0][2:])

	fig3 = px.line(x = index, y = values)
	fig3.update_layout(title="Un-Employment over the years in each country", xaxis_title = "Year", yaxis_title = "No. of UnEmployment",)
	fig3.update_traces(line_color="#ffa600")
	
	return fig3


server = flask.Flask(__name__)

app.title = "UnEmployment EDA"
if __name__ == "__main__":
	app.run_server(debug = False, server = server)