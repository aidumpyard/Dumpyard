import plotly.graph_objects as go

# Sample data
x = [1, 2, 3, 4]
y = [10, 11, 12, 13]
labels = ['A', 'B', 'C', 'D']  # Labels for each point

# Create scatter plot
fig = go.Figure(data=go.Scatter(x=x, y=y, mode='markers+text', text=labels,
                                textposition='top center',
                                textfont=dict(family='Arial', size=12, color='blue'),
                                marker=dict(size=12)))

# Customize layout
fig.update_layout(title='Scatter Plot with Labels',
                  xaxis_title='X Axis',
                  yaxis_title='Y Axis')

# Show plot
fig.show()