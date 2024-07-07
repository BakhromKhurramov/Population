import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output 

data = pd.read_excel('Population.xlsx', 'city')

filtered_df = data[data['fact'].notnull()]
cities = filtered_df['Город'].unique().tolist()

fig = px.line(filtered_df, x='year', y=['fact', 'Модель'], title='Line Chart with Plotly Express')

app = dash.Dash(__name__)
app.server=server

app.layout = html.Div([
    html.Label('Select City:'),
    dcc.Dropdown(
        id='city-dropdown',
        options=[{'label': city, 'value': city} for city in cities],
        value=None  # Set initial selected city
    ),
    dcc.Graph(id='line-chart', figure=fig)
])
@app.callback(
    Output('line-chart', 'figure'),
    [Input('city-dropdown', 'value')]
)
def update_chart(selected_city):
    if selected_city is None:
        df_groupby = filtered_df.groupby('year')[['fact', 'Модель']].sum().reset_index()
        fig = px.line(df_groupby, x='year', y=['fact', 'Модель'], title='Line Chart with Plotly Express')
    else:
        dff = filtered_df[filtered_df['Город'] == selected_city]  # Filter data based on selected city
        fig = px.line(dff, x='year', y=['fact', 'Модель'], title='Line Chart with Plotly Express')
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)