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

# Define points for the lines
x = [0]  # x position for the first bar
y1_start = 0
y1_end = 0.05 * bar_height
y2_start = 0.1 * bar_height
y2_end = 0.3 * bar_height

# Add the filled area between the two lines
fig.add_shape(
    type="path",
    path=f"M {x[0]-0.25} {y1_start} L {x[0]+0.25} {y1_end} L {x[0]+0.25} {y2_end} L {x[0]-0.25} {y2_start} Z",
    fillcolor="white",
    line=dict(color="white"),
)

# Add the yellow lines
fig.add_shape(dict(type="line", x0=x[0]-0.25, y0=y1_start, x1=x[0]+0.25, y1=y1_end, line=dict(color="yellow", width=8)))
fig.add_shape(dict(type="line", x0=x[0]-0.25, y0=y2_start, x1=x[0]+0.25, y1=y2_end, line=dict(color="yellow", width=8)))

# App layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)