from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_table
import pandas as pd


# Read the CSV data
url = "https://raw.githubusercontent.com/yoecon/cg_survey_2023/main/CG2023_CALCULATED_SCORE.csv"
df = pd.read_csv(url)

# Filter data by 'Life' insurance type
df = df[df['INSURANCE_TYPE'] == 'Nonlife'].sort_values(by='total_weighted_score', ascending=False)

# Calculate 'all' value by summing 'total_weighted_score'
all_value = df['total_weighted_score'].sum()

# Initialize the Dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Define the layout of the app
app.layout = html.Div([
    html.H1("Nonlife Insurance - Total Weighted Score"),
    html.H2(""),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-size', children=[
        dcc.Tab(label='SIZE', value='tab-1-size'),
        dcc.Tab(label='ROE', value='tab-2-roe'),
        dcc.Tab(label='EWS', value='tab-3-ews'),
        dcc.Tab(label='BANK', value='tab-4-bank')
    ]),
    html.Div(id='tabs-content-example-graph')
])

@callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-size':
        return html.Div([
            html.H3('size'),
            dcc.Dropdown(
                id='comp-size-dropdown',
                options=[{'label': comp_size, 'value': comp_size} for comp_size in df['COMP_SIZE'].unique()] + [{'label': 'All', 'value': 'all'}],
                value='all'
            ),
            dcc.Graph(id='histogram-plot'),
            dash_table.DataTable(
                id='data-table',
                columns=[{'name': col, 'id': col} for col in ['COMP_NAME', 'COMP_SIZE','total_weighted_score','cat1_weighted_score', 'cat2_weighted_score', 'cat3_weighted_score',
                'cat4_weighted_score', 'cat5_weighted_score']],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto', 'margin-left': '20px', 'margin-right': '20px'},
                sort_action="native",
                sort_mode="multi"
            )
        ])
    elif tab == 'tab-2-roe':
        return html.Div([
            html.H3('roe'),
            dcc.Dropdown(
                id='roe-dropdown',
                options=[{'label': roe_val, 'value': roe_val} for roe_val in df['ROE'].unique()] + [{'label': 'All', 'value': 'all'}],
                value='all'
            ),
            dcc.Graph(id='histogram-roe-plot'),
            dash_table.DataTable(
                id='data-table-roe',
                columns=[{'name': col, 'id': col} for col in ['COMP_NAME', 'ROE', 'total_weighted_score','cat1_weighted_score', 'cat2_weighted_score', 'cat3_weighted_score',
                'cat4_weighted_score', 'cat5_weighted_score']],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto', 'margin-left': '20px', 'margin-right': '20px'},
                sort_action="native",
                sort_mode="multi"
            )

        ])
    elif tab == 'tab-3-ews':
        return html.Div([
            html.H3('ews'),
            dcc.Dropdown(
                id='ews-dropdown',
                options=[{'label': ews_group_val, 'value': ews_group_val} for ews_group_val in df['EWS_GROUP'].unique()] + [{'label': 'All', 'value': 'all'}],
                value='all'
            ),
            dcc.Graph(id='histogram-ews-plot'),
            dash_table.DataTable(
                id='data-table-ews',
                columns=[{'name': col, 'id': col} for col in ['COMP_NAME', 'EWS_GROUP', 'total_weighted_score','cat1_weighted_score', 'cat2_weighted_score', 'cat3_weighted_score',
                'cat4_weighted_score', 'cat5_weighted_score']],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto', 'margin-left': '20px', 'margin-right': '20px'},
                sort_action="native",
                sort_mode="multi"
            )
        ])

# Define callback to update the histogram plot and data table based on the selected COMP_SIZE
@app.callback(
    [Output('histogram-plot', 'figure'),
     Output('data-table', 'data')],
    Input('comp-size-dropdown', 'value')
)
def update_histogram_and_table(selected_comp_size):
    if selected_comp_size == 'all':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['COMP_SIZE'] == selected_comp_size]

    fig = px.histogram(filtered_df, x='total_weighted_score', nbins=10, title="Nonlife Insurance - Total Weighted score - SIZE")
    table_data = filtered_df.to_dict('records')
    return fig, table_data

# Define callback to update the histogram plot and data table based on the selected ROE
@app.callback(
    [Output('histogram-roe-plot', 'figure'),
     Output('data-table-roe', 'data')],
    Input('roe-dropdown', 'value')
)
def update_histogram_roe_and_table(selected_roe):
    if selected_roe == 'all':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['ROE'] == selected_roe]

    fig = px.histogram(filtered_df, x='total_weighted_score', nbins=10, title="Nonlife Insurance - Total Weighted score - ROE")
    table_data = filtered_df.to_dict('records')
    return fig, table_data

# Define callback to update the histogram plot and data table based on the selected EWS_GROUP
@app.callback(
    [Output('histogram-ews-plot', 'figure'),
     Output('data-table-ews', 'data')],
    Input('ews-dropdown', 'value')
)
def update_histogram_ews_and_table(selected_ews):
    if selected_ews == 'all':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['EWS_GROUP'] == selected_ews]

    fig = px.histogram(filtered_df, x='total_weighted_score', nbins=10, title="Nonlife Insurance - Total Weighted score - EWS_GROUP")
    table_data = filtered_df.to_dict('records')
    return fig, table_data



if __name__ == '__main__':
    app.run(debug=True)
