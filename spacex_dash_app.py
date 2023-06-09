# Import required libraries
import pandas as pd
import plotly.graph_objects as go
# import dash
from dash import Dash, html, dcc, callback, Output, Input, State, no_update
# import dash_html_components as html
# import dash_core_components as dcc
# from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',

                                             # Update dropdown values using list comphrehension
                                             options=[{'label': 'All Sites', 'value': 'All'}] +\
                                             [{'label': i, 'value': i}
                                              for i in spacex_df['Launch Site'].unique()],
                                             #  {'label': 'All Sites','value': 'ALL'},
                                             #  {'label': 'CCAFS LC-40','value': 'cca1'},
                                             #  {'label': 'CCAFS SLC-40','value': 'cca2'},
                                             #  {'label': 'KSC LC-39A','value': 'ksc'},
                                             #  {'label': 'VAFB SLC-4E','value': 'vafb'},
                                             value='ALL',
                                             placeholder="Select a launch site here",
                                             searchable=True
                                             ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value')])
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
    if entered_site == 'All':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Success rate for All Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(
            filtered_df.
            groupby('class', as_index=False)['class'].
            count().
            reset_index(), 
            values='class',
            names='index',
            title='Total Success Launches for site %s' % entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(site,slider_value):
    # print(site)
    # slider_value = [float(x) for x in slider_value]
    if site=='All':
        fig = px.scatter(data_frame = spacex_df[
                                          (spacex_df['Payload Mass (kg)']<slider_value[1]) & 
                                          (spacex_df['Payload Mass (kg)']>slider_value[0])
                                          ],
                                          x = 'Payload Mass (kg)',
                   y = 'class',color='Booster Version Category'
        )
        return fig
    else:
        filtered_df_scatter = spacex_df[spacex_df['Launch Site'] == site]
        fig = px.scatter(data_frame = filtered_df_scatter[
                                          (filtered_df_scatter['Payload Mass (kg)']<slider_value[1]) & 
                                          (filtered_df_scatter['Payload Mass (kg)']>slider_value[0])
                                          ],
                                          x = 'Payload Mass (kg)',
                   y = 'class',color='Booster Version Category'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
