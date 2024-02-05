import plotly.graph_objs as go

# Sample data for demonstration
x_data = [1, 2, 3, 4, 5]
y_data = [2, 3, 4, 5, 6]

# Create a scatter plot
fig = go.Figure(data=[go.Scatter(x=x_data, y=y_data, mode='markers')])

# Define the chart title with some space below for the underline annotation
fig.update_layout(
    title_text='Your Chart Title Here<br><br>',  # Add breaks for space under the title
    title_x=0.5,  # Center the title
    annotations=[{
        'x': 0.5,
        'y': 1.085,
        'xref': 'paper',
        'yref': 'paper',
        'showarrow': False,
        'text': '<span style="font-size: 20px; text-decoration: underline;">' + '-'*100 + '</span>',  # Underline effect
        'font': {'size': 20},
        'align': 'center'
    }]
)

# Show the figure
fig.show()