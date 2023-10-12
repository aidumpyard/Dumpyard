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
x_values = [-0.25, 0.25]
y_values1 = [0.05 * bar_height, 0.25 * bar_height]
y_values2 = [0.1 * bar_height, 0.3 * bar_height]

# Add the area fill between the two lines
fig.add_trace(go.Scatter(x=x_values + x_values[::-1],  # x values for both lines
                         y=y_values1 + y_values2[::-1],  # y values for line1 followed by y values for line2 (in reverse order)
                         fill='toself',
                         fillcolor='white',
                         line=dict(color='white'),
                         mode='lines'))

# App layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)