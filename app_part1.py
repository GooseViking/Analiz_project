from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

df = pd.read_csv('project_data.csv')

df_cities = pd.read_csv('cities_data.csv')

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

all_cont = df['name'].unique()
cities = df['area_name'].unique()

SIDESTYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#abcdef",
}

CONTSTYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div([    
        html.H2("Раздел", className="display-4", style={'color': 'black'}),
            html.Hr(style={'color': 'black'}),
            dbc.Nav([
                    dbc.NavLink("Общие показатели", href="/page1", active="exact"),
                    dbc.NavLink("Карта", href="/page2", active="exact"),
                ],
                vertical=True,pills=True),
        ],
        style=SIDESTYLE,
    ),
    html.Div(id="page-content", children=[], style=CONTSTYLE)
])


@callback(
    Output("page-content", "children"),
    [Input("url", "pathname")])
def pagecontent(pathname):
    if pathname == "/page1":
        return dmc.Container([
            html.Div([
                html.H1("Информация о профессии"),
                html.P(
                    "Анализ профессии системный администратор на сайте hh.ru."
                    "Используйте фильтры, чтобы увидеть результат."
                    )
                ], style={
                    'backgroundColor': 'rgb(171, 205, 239)',
                    'padding': '10px 5px'
                }),      
            html.Div([
                        html.Div([
                            html.Label('Профессии'),
                            dcc.Dropdown(
                                id ='name',
                                options=[{'label': i, 'value': i} for i in all_cont],
                                value=['Системный администратор', 'Сетевой инженер', 'DevOps инженер', 'Сетевой администратор'],
                                multi=True
                            )
                        ],
                        style={'width': '100%', 'display': 'inline-block'}),
                        html.Div(
                            dcc.Graph(id='pie'),
                            style={'width': '100%', 'display': 'inline-block'}),
                        html.Div(
                            dcc.Graph(id='bar_first'),
                            style={'width': '100%', 'display': 'inline-block'}),
                        html.Div(
                            dcc.Graph(id='bar'),
                            style={'width': '100%', 'display': 'inline-block'}),
                        html.Div(
                            dcc.Graph(id='scatter'),
                            style={'width': '100%', 'display': 'inline-block'}),
            ])
        ], fluid=True)
    elif pathname == "/page2":
        return dmc.Container([
            html.Div([
                html.Div([
                    html.H1("Карта вакансий"),
                    html.P(
                        "На этой карте отображены города, в который предлагают исследуемую вакансию"
                    )
                ], style={
                    'backgroundColor': 'rgb(171, 205, 239)',
                    'padding': '10px 5px'
                }),
                    html.Div([
                    html.Label('Профессии'),
                    dcc.Dropdown(
                        id ='name',
                        options=[{'label': i, 'value': i} for i in all_cont],
                        value=['Системный администратор', 'Сетевой инженер', 'DevOps инженер', 'Сетевой администратор'],
                        multi=True,
                    )
                ], style={
                    'overflow': 'hidden'}),
                    html.Div(
                        dcc.Graph(id='map'),
                        style={'width': '100%', 'display': 'inline-block'}),
                ])
        ], fluid=True)

@callback(
    Output('pie', 'figure'),
    Input('name', 'value'),
)
def update_pie(name):
    filtered_data = df[(df['name'].isin(name))]
    fig = px.pie(filtered_data,
                 values=filtered_data.groupby('name')['name'].count(),
                 names=filtered_data['name'].unique(),
                 hole=.3,)
    return fig


@callback(
    Output('bar_first', 'figure'),
    Input('name', 'value'),
)
def update_bar_first(name):
    filtered_data = df[(df['name'].isin(name))]
    fig = px.bar(filtered_data,
            y=(((filtered_data.groupby('name')['salary_to'].sum()+filtered_data.groupby('name')['salary_from'].sum())/2)/filtered_data.groupby('name')['name'].count()),
            x=filtered_data['name'].unique(),
            color_discrete_sequence=px.colors.sequential.Agsunset)
    return fig


@callback(
    Output('scatter', 'figure'),
    Input('name', 'value'),
)
def update_scatter(name):
    figu = px.bar(df,
            x=df.groupby('area_name')['area_name'].count(),
            y=df['area_name'].unique(),
            orientation='h',
            color_discrete_sequence=px.colors.sequential.Blackbody)
    return figu

@callback(
    Output('bar', 'figure'),
    Input('name', 'value'),
)
def update_bar(name):
    fig = px.bar(df,
            x=df['employer_name'].unique(),
            y=df.groupby('employer_name')['employer_name'].count(),
            labels = {'y': 'Количество вакансий'})
    return fig


@callback(
    Output('map', 'figure'),
    Input('name', 'value'),
)
def update_map(name):
    df_fil = pd.merge(df, df_cities, left_on=['area_name'], right_on=['Город'],how='inner')
    fig = px.scatter_mapbox(df_fil, lat=df_fil['Широта'].unique(), lon=df_fil['Долгота'].unique(), hover_name=df_fil['area_name'].unique(),)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
