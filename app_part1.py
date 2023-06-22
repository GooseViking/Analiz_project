from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_mantine_components as dmc

df = pd.read_csv('project_data.csv')

external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

all_cont = df['name'].unique()

app.layout = dmc.Container([
    html.Div([
        html.H1("Информация о профессии"),
        html.P(
            "Анализ профессии системный администратор на сайте hh.ru."
            "Используйте фильтры, чтобы увидеть результат."
            )
        ], style={
            'backgroundColor': 'rgb(140, 130, 188)',
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
                style={'width': '48%', 'display': 'inline-block'}),
                html.Div(
                    dcc.Graph(id='pie'),
                    style={'width': '100%', 'display': 'inline-block'}),
                html.Div(
                    dcc.Graph(id='scatter'),
                    style={'width': '100%', 'display': 'inline-block'}),
                html.Div(
                    dcc.Graph(id='bar'),
                    style={'width': '100%', 'display': 'inline-block'}),

    ])
], fluid=True)


@callback(
    Output('pie', 'figure'),
    Input('name', 'value'),
)
def update_pie(name):
    filtered_data = df[(df['name'].isin(name))]
    fig = px.pie(filtered_data, values=df.groupby('name')['name'].count(), names=name, hole=.3)
    return fig


@callback(
    Output('scatter', 'figure'),
    Input('name', 'value'),
)
def update_scatter(name):
    fig = px.bar(df,
            y=(df.groupby('name')['salary_to'].mean()-df.groupby('name')['salary_from'].mean()),
            x=df['name'].unique())
    return fig


@callback(
    Output('bar', 'figure'),
    Input('name', 'value'),
)
def update_(name):
    fig = px.bar(df,
            x=df['employer_name'].unique(),
            y=df.groupby('employer_name')['employer_name'].count())
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
