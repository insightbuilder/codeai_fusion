import plotly.graph_objects as go
import pandas as pd
import plotly.subplots as sp

# Load the dataset
file_path = "world_and_india_workforce_data.csv"
df = pd.read_csv(file_path)

# Separate World and India data
world_data = df[df["Category"].str.contains("World")]
india_data = df[df["Category"].str.contains("India")]

# Create the figure with increased spacing and height
fig = sp.make_subplots(
    rows=1, cols=2,
    subplot_titles=["Global Workforce Distribution", "Indian Workforce Distribution"],
    horizontal_spacing=0.15
)

# Add World data with improved styling
fig.add_trace(
    go.Bar(
        x=world_data["Category"],
        y=world_data["Count (in Millions)"],
        name="World",
        marker_color="navy",
        text=world_data["Count (in Millions)"].round(1),
        textposition='auto',
    ),
    row=1, col=1
)

# Add India data with improved styling
fig.add_trace(
    go.Bar(
        x=india_data["Category"],
        y=india_data["Count (in Millions)"],
        name="India",
        marker_color="darkorange",
        text=india_data["Count (in Millions)"].round(1),
        textposition='auto',
    ),
    row=1, col=2
)

# Enhanced layout customization
fig.update_layout(
    title=dict(
        text="Global vs Indian Workforce Analysis",
        font=dict(size=24, family="Arial Black"),
        y=0.95
    ),
    height=700,
    showlegend=False,
    template="plotly_white",
    font=dict(family="Arial", size=14),
    plot_bgcolor="rgba(250,250,250,1)",
    paper_bgcolor="rgba(250,250,250,1)",
    title_x=0.5,
)

# Enhanced axes styling
fig.update_xaxes(
    tickangle=-45,
    title_font=dict(size=16, family="Arial"),
    tickfont=dict(size=12),
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(220,220,220,0.5)',
)

fig.update_yaxes(
    title="Count (in Millions)",
    title_font=dict(size=16, family="Arial"),
    tickfont=dict(size=12),
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(220,220,220,0.5)',
)

# Save and show the graph
fig.write_html("world_and_india_readable_dashboard.html")
fig.show()
