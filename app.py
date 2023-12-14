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
    colors = {
        'Production grassland': '#1AA881',       #green
        'Built-up area': '#D186B0',              #pink
        'Wetland': '#1A80BA',                    # Dark blue
        'Cropland': '#F2E755',                   # Yellow
        'Grassland with woody biomass': '#DD7E33'  # Orange
    }

    # Map labels to colors
    pie_colors = [colors[label] for label in labels]

    pie_chart = go.Pie(
        labels=labels, 
        values=values, 
        textinfo='percent',
        textposition='outside',
        insidetextorientation='auto',
        texttemplate='%{percent:.0%}',
        hoverinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{percent:.0%}<br>Total: %{value} ha<extra></extra>',
        hole=.6,
        marker=dict(colors=pie_colors),  # Apply custom colors
        showlegend=False
    )

    fig = go.Figure(data=[pie_chart])
    
    # Add scatter plot traces to mimic circular legend markers
    for label, color in zip(labels, pie_colors):
        fig.add_trace(go.Scatter(
            x=[None],  # No actual data points
            y=[None],
            mode='markers',
            marker=dict(color=color, size=10),
            name=label
        ))

    # Update the layout to remove the background and add a light gray background
    fig.update_layout(
        legend=dict(
            orientation="h",
            x=0.15,
            y=-0.3,
            xanchor="left",
            yanchor="bottom"
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Making the plot background transparent
        paper_bgcolor='#f0f0f0',  # Light gray background for the entire graph
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
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
