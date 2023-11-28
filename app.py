from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go

def load_forest_land_use_data():
    """Loads forest land use change data."""
    return pd.read_csv("static/data/LandUseChange_Forest_1990_2016.csv")

def prepare_forest_land_use_chart_data(data_df):
    """Prepares data for the forest land use pie chart."""
    land_use_data = data_df.iloc[0, 3:]  # land use columns start from the 4th column
    labels = land_use_data.index.tolist()
    values = land_use_data.values.tolist()
    return labels, values

def create_forest_land_use_pie_chart(labels, values):
    """Creates a pie chart for forest land use data."""
    sector_colors = ['#ff7f0e', '#2ca02c', '#1f77b4', '#d62728', '#9467bd', '#8c564b']

    pie_chart = go.Pie(
        labels=labels, 
        values=values, 
        marker=dict(colors=sector_colors, line=dict(color='#ffffff', width=2)), 
        textinfo='label+percent',
        textposition='outside', 
        texttemplate='%{label}: %{percent:.0%}',
        outsidetextfont=dict(color=sector_colors),  
        automargin=True
    )

    fig = go.Figure(data=[pie_chart])

    # Add a title at the bottom
    fig.update_layout(
        title={
            'text': "Land uses converted from forestland since 1990",
            'y': 0.1,  # Adjust the vertical position
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'bottom'
        },
        
    )

    return fig


def setup_dash_layout(app, fig_pie_chart):
    """Sets up the layout of the Dash app."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='forest-land-use-pie-chart', figure=fig_pie_chart)
        ])
    ],id='forest-land-use-pie-chart-layout')

def create_app():
    """Creates and configures the Dash app."""
    app = Dash(__name__)

    # Load and prepare data
    data_df = load_forest_land_use_data()
    labels, values = prepare_forest_land_use_chart_data(data_df)

    # Create pie chart
    fig_pie_chart = create_forest_land_use_pie_chart(labels, values)

    # Setup layout
    setup_dash_layout(app, fig_pie_chart)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)
