# Import necessary libraries
import dash
from dash import dcc, html
import plotly.graph_objects as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Data for the waterfall chart
labels = ["Start", "Add", "Subtract", "End"]
values = [100, 20, -15, 105]  # 100 + 20 - 15 = 105

# Create the waterfall figure
fig = go.Figure(go.Waterfall(
    name = "Waterfall",
    orientation = "v",
    measure = ["absolute", "relative", "relative", "absolute"],
    x = labels,
    textposition = "outside",
    y = values,
    connector = {"line": {"color": "rgb(63, 63, 63)"}},
))

# Add custom lines to the start of the first absolute bar
bar_height = values[0]

# Calculate the start and end points for the two lines
start_point1 = [-0.25, 0.05 * bar_height]
end_point1 = [0.25, 0.25 * bar_height]
start_point2 = [-0.25, 0.1 * bar_height]
end_point2 = [0.25, 0.3 * bar_height]

# Add the lines to the figure
fig.add_shape(dict(type="line", x0=start_point1[0], y0=start_point1[1], x1=end_point1[0], y1=end_point1[1],
                   line=dict(color="yellow", width=8)))
fig.add_shape(dict(type="line", x0=start_point2[0], y0=start_point2[1], x1=end_point2[0], y1=end_point2[1],
                   line=dict(color="yellow", width=8)))

# App layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)