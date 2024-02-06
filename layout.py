import plotly.express as px
import pandas as pd

# Sample DataFrame with a datetime column
df = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=12, freq='M'),
    'Value': range(1, 13)
})

# Create a scatter plot
fig = px.scatter(df, x='Date', y='Value')

# Generate tickvals and ticktext
tickvals = df['Date']
ticktext = df['Date'].dt.strftime('%b')

# Update layout to show all months on x-axis
fig.update_layout(
    xaxis = dict(
        tickvals=tickvals,
        ticktext=ticktext
    )
)

# Show the figure
fig.show()