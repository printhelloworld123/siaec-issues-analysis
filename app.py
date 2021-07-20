import os
import base64
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
from haversine import haversine
import markdown
from markdown import *


original = pd.read_csv('files/query_result_2021-07-20T04_17_33.426513Z.csv')
address = pd.read_csv('files/address.csv')
df = pd.read_csv('files/all_siaec_waypoints_cleaned_onemap_address_extracted_200721.csv')

# Preparing the graph plots #

## Preparing the dataframe for plotting the overall trend in mismatches ##
df_overall_trend = pd.DataFrame(df.groupby('date').match.apply(pd.value_counts))

df_overall_trend['date_final'] = list(map(lambda x: x[0], list(df_overall_trend.index)))

df_overall_trend_plot = pd.DataFrame(columns=['Date', 'Mismatch(%)'])
dates = set(df_overall_trend['date_final'])
for date in dates:
    overall_stat = df_overall_trend.loc[date,'match']
    mismatch_percent = round(overall_stat[False] / (overall_stat[False] + overall_stat[True]) * 100, 2)
    index = len(df_overall_trend_plot)
    df_overall_trend_plot.loc[index,'Date'] = date
    df_overall_trend_plot.loc[index,'Mismatch(%)'] = mismatch_percent
    
df_overall_trend_plot = df_overall_trend_plot.sort_values(by=['Date'])
df_overall_trend_plot = df_overall_trend_plot.reset_index()
df_overall_trend_plot = df_overall_trend_plot.drop(columns=['index'])

df_adjusted = df[df['date'] > '2021-05-31']
df_adjusted_match_false = df_adjusted[df_adjusted['match'] == False]

# Preparing the dataframe for plotting the distance deviation between req-offered & req-onemap #
requested_coords = np.array(df_adjusted_match_false[['requested_lat','requested_lon']])
onemap_coords = np.array(df_adjusted_match_false[['onemap_lat','onemap_lon']])
offer_coords = np.array(df_adjusted_match_false[['offer_lat','offer_lon']])

df_adjusted_match_false['distance_deviation(m) b/w req & onemap'] = list(map(lambda req, onemap: 
                                                                             haversine(req, onemap) * 100,
                                                                             requested_coords, onemap_coords))

df_adjusted_match_false['distance_deviation(m) b/w req & offered'] = list(map(lambda req, offer: 
                                                                             haversine(req, offer) * 100,
                                                                             requested_coords, offer_coords))

df_dist_1 = pd.DataFrame(columns=['Distance', 'Source'])
df_dist_1['Distance'] = list(df_adjusted_match_false['distance_deviation(m) b/w req & offered'])
df_dist_1['Source'] = 'requested-offered'

df_dist_2 = pd.DataFrame(columns=['Distance', 'Source'])
df_dist_2['Distance'] = list(df_adjusted_match_false['distance_deviation(m) b/w req & onemap'])
df_dist_2['Source'] = 'requested-onemap'

df_dist = pd.concat([df_dist_1,df_dist_2])
df_dist = df_dist.reset_index()

# Plotting the graph of overall trend in mismatches #
fig_overall_trend = px.line(df_overall_trend_plot, 
                            x='Date', 
                            y='Mismatch(%)', 
                            title='Total Mismatch in requested and offered bookings per day (%)')

fig_overall_trend.update_layout(xaxis_tickformat = '%d %B %Y',
                                yaxis_title="% of Mismatch")

fig_overall_trend.add_vline(x='2021-05-17', 
                            line_width=2, 
                            line_dash="dash", 
                            line_color="red")

fig_overall_trend.add_vline(x='2021-05-31', 
                            line_width=2, 
                            line_dash="dash", 
                            line_color="red")


# Plotting the graph of overall distance deviation between req-offered & req-onemap #
fig_dist_dev = px.histogram(df_dist, 
                            x="Distance", 
                            color="Source",
                            marginal="box",
                            histnorm='percent',
                            nbins=30,
                            color_discrete_map = {True:'rgb(82,188,163)',False:'#E45756'},
                            title = "Distance deviation for all mismatches since 31 May")
                          
fig_dist_dev.update_layout(barmode='overlay',
                           xaxis_title="Distance deviation range", 
                           yaxis_title="% of waypoints")

fig_dist_dev.update_layout(legend=dict(orientation="h",
                                       yanchor="bottom",
                                       x=1,
                                       y=1.02,
                                       xanchor="right"))

fig_dist_dev.update_layout(legend_title_text='')
fig_dist_dev.update_traces(opacity=0.7)

# Preparing the interface #
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

## Styles for the sidebar ##
SIDEBAR_STYLE = {"position": "fixed",
                 "top": 0,
                 "left": 0,
                 "bottom": 0,
                 "width": "16rem",
                 "padding": "2rem 1rem",
                 "background-color": "#f8f9fa"}

# Styles for the main content ##
CONTENT_STYLE = {"margin-left": "18rem",
                 "margin-right": "2rem",
                 "padding": "2rem 1rem"}

sidebar = html.Div([html.Hr(),
                    dbc.Nav([dbc.NavLink("SIAEC Issue Overall Analysis", href="/", active="exact"),
                             dbc.NavLink("Methodology", href="/methodology", active="exact")],
                            vertical=True,
                            pills=True)],style=SIDEBAR_STYLE)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar,content])

overall_analysis_page = html.Div(
    [
        ### Title ###
        dbc.Row(dbc.Col(html.H2("SIAEC Issue Overall Analysis"),
                        style = {'padding-top' : '2%',
                                'padding-left':'5%'})),
        
        ### Section 1 Header ###
        dbc.Row(dbc.Col(html.H4("1. Overview"),
                        style = {'padding-top' : '2%',
                                'padding-left':'5%'})),
        
        ### Section 1 Graph - Overall Trend in Mismatches ###
        dbc.Row([dbc.Col(dcc.Graph(id='example-graph',
                                   figure=fig_overall_trend,
                                   style={"height": "500px",
                                          "width": "1050px",
                                          "padding-left":"2%"}))]),
        
        ### Section 1 Text ###
        dbc.Row(dbc.Col(children=markdown_text_page_1_section_1,
                        style={"marginLeft":"4%",
                               "marginRight":"10%",
                              "text-align":"justify"})),
        
        ### Section 2 Header ###
        dbc.Row(dbc.Col(html.H4("2. Mismatch Analysis"),
                        style = {"padding-top" : "2%",
                                "padding-left":"5%"})),
        
        ### Section 2 Map Visualization ###     
        dbc.Row([html.Iframe(src="https://studio.unfolded.ai/public/68e645c2-d4aa-4193-afbe-deeeaf14cf0d/embed",
                            style={"height": "550px",
                                   "width": "990px",
                                   "overflow":"auto",
                                   "border":"0",
                                   "padding-top":"2%",
                                   "padding-left":"5%",
                                   "padding-bottom":"2%"})]),
        
        ### Section 2 Histogram ###
        dbc.Row([dbc.Col(dcc.Graph(id='example-graph-1',
                                   figure=fig_dist_dev,
                                   style={"height": "500px", 
                                          "width":"1050px",
                                          "padding-left":"2%"}))]),
        
        ### Section 2 Text ###
        dbc.Row([dbc.Col(children=markdown_text_page_1_section_2_1,
                        style={"marginLeft":"4%",
                               "marginRight":"10%",
                              "marginBottom":"2%",
                              "text-align":"justify"})]),
        dbc.Row([dbc.Col(children=markdown_text_page_1_section_2_2,
                        style={"marginLeft":"4%",
                               "marginRight":"10%",
                              "marginBottom":"2%",
                              "text-align":"justify"})]),
        dbc.Row([dbc.Col(children=markdown_text_page_1_section_2_3,
                        style={"marginLeft":"4%",
                               "marginRight":"10%",
                              "marginBottom":"5%",
                              "text-align":"justify"})])   
    ]
)


methodology_page = html.Div(
    [
        ### Title ###
        dbc.Row(dbc.Col(html.H2("Methodology"),
                        style = {'padding-top' : '2%',
                                'padding-left':'5%'})),
        
        ### Section 1 Header ###
        dbc.Row(dbc.Col(html.H4("1. Steps"),
                        style = {'padding-top' : '2%',
                                'padding-left':'5%'})),
        
        ### Section 1 Text ###
        dbc.Row(dbc.Col(children=markdown_text_page_2_section_1_1,
                        style={"marginLeft":"4%",
                               "marginRight":"15%",
                               "padding-top":"2%",
                              "text-align":"justify"})),
        dbc.Row(dbc.Col(children=markdown_text_page_2_section_1_2,
                        style={"marginLeft":"4%",
                               "marginRight":"15%",
                               "padding-top":"2%",
                              "text-align":"justify"})),
        dbc.Row(dbc.Col(children=markdown_text_page_2_section_1_3,
                        style={"marginLeft":"4%",
                               "marginRight":"15%",
                               "padding-top":"2%",
                              "text-align":"justify"})),
        dbc.Row(dbc.Col(children=markdown_text_page_2_section_1_4,
                        style={"marginLeft":"4%",
                               "marginRight":"15%",
                               "padding-top":"2%",
                              "text-align":"justify"})),
        dbc.Row(dbc.Col(children=markdown_text_page_2_section_1_5,
                        style={"marginLeft":"4%",
                               "marginRight":"15%",
                               "padding-top":"2%",
                              "text-align":"justify"})),
        
        ### Section 2 Header ###
        dbc.Row(dbc.Col(html.H4("2. Data"),
                        style = {'padding-top' : '2%',
                                'padding-left':'5%'})),
        
        ### Section 2 Text ###
        dbc.Row(dbc.Col(children=markdown_text_page_2_section_2,
                        style={"marginLeft":"4%",
                               "marginRight":"15%",
                               "padding-top":"2%",
                              "text-align":"justify"})),
        
        ### Section 2 Download CSV File Buttons ###
        dbc.Row(dbc.Col(html.Div([dbc.Button("Download Bookings CSV", id="bookings_csv",color="info",
                                             className="mr-1",
                                             style={"marginLeft": "3.5%",
                                                    "marginTop": "2%",
                                                   "padding-right":"2%"}),
                                  
                                  dcc.Download(id="download_bookings_csv"),
                                  
                                  dbc.Button("Download Addresses CSV", id="addresses_csv",color="info",
                                             className="mr-1",
                                            style={"marginLeft": "3.5%",
                                                   "marginTop": "2%",}),
                                  
                                  dcc.Download(id="download_address_csv")])))
        
    ]
)

## Callbacks ##

### Download Bookings CSV Button ###
@app.callback(Output("download_bookings_csv","data"),
              Input("bookings_csv", "n_clicks"),
              prevent_initial_call=True)
def func(n_clicks):
    return dcc.send_data_frame(original.to_csv, "all_bookings_1May_19Jul.csv")


### Download Addresses CSV Button ###
@app.callback(Output("download_address_csv","data"),
              Input("addresses_csv", "n_clicks"),
              prevent_initial_call=True)
def func(n_clicks):
    return dcc.send_data_frame(address.to_csv, "all_addresses_1May_19Jul.csv")

### Render the webpages ###
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return overall_analysis_page
    elif pathname == "/methodology":
        return methodology_page

if __name__ == "__main__":
    app.run_server(debug=True)