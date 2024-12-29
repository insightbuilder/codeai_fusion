import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots

# Load the data
df = pd.read_csv("world_and_india_workforce_data.csv")

# Prepare hierarchical structure for World data with clean labels
world_data = {
    'Category': [
        'Total Population',
        'Working-Age Population',
        'Labor Force',
        'Professional Workforce (Formal)',
        'Professional Workforce (Informal)'
    ],
    'Count (Millions)': [
        df[df['Category'] == 'Total Population (World)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Working-Age Population (World)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Labor Force (World)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Professional Workforce (World - Formal Sector)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Professional Workforce (World - Informal Sector)']['Count (in Millions)'].iloc[0]
    ],
    'Level': [0, 1, 2, 3, 3]
}

# Prepare hierarchical structure for India data with clean labels
india_data = {
    'Category': [
        'Total Population',
        'Working-Age Population',
        'Labor Force',
        'Professional Workforce (Formal)',
        'Professional Workforce (Informal)',
        'Agriculture Workforce',
        'High-Skilled Professionals'
    ],
    'Count (Millions)': [
        df[df['Category'] == 'Total Population (India)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Working-Age Population (India)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Labor Force (India)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Professional Workforce (India - Formal Sector)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Professional Workforce (India - Informal Sector)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'Agriculture Workforce (India)']['Count (in Millions)'].iloc[0],
        df[df['Category'] == 'High-Skilled Professionals (India)']['Count (in Millions)'].iloc[0]
    ],
    'Level': [0, 1, 2, 3, 3, 3, 3]
}

df_world = pd.DataFrame(world_data)
df_india = pd.DataFrame(india_data)

# Create subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Global Workforce Hierarchy", "Indian Workforce Hierarchy"),
    horizontal_spacing=0.15,
    specs=[[{"secondary_y": False}, {"secondary_y": True}]]
)

# Define colors for World and India
world_color = '#004182'  # Darker LinkedIn Blue
india_color = '#D93F3F'  # Darker Red

# Add World data (left subplot)
for level in df_world['Level'].unique():
    level_data = df_world[df_world['Level'] == level]
    opacity = 1 - (level * 0.15)
    fig.add_trace(
        go.Bar(
            name="Global" if level == 0 else "Global_hidden",
            x=level_data['Count (Millions)'],
            y=level_data['Category'],
            orientation='h',
            marker_color=world_color,
            marker_opacity=opacity,
            text=level_data['Count (Millions)'].apply(lambda x: f'{x:,.0f}M'),
            textposition='auto',
            showlegend=bool(level == 0),  # Explicitly convert to Python boolean
            legendgroup="Global"
        ),
        row=1, col=1
    )

# Add India data (right subplot)
for level in df_india['Level'].unique():
    level_data = df_india[df_india['Level'] == level]
    opacity = 1 - (level * 0.15)
    fig.add_trace(
        go.Bar(
            name="India" if level == 0 else "India_hidden",
            x=level_data['Count (Millions)'],
            y=level_data['Category'],
            orientation='h',
            marker_color=india_color,
            marker_opacity=opacity,
            text=level_data['Count (Millions)'].apply(lambda x: f'{x:,.0f}M'),
            textposition='auto',
            showlegend=bool(level == 0),  # Explicitly convert to Python boolean
            legendgroup="India"
        ),
        row=1, col=2
    )

# Update layout
fig.update_layout(
    title=dict(
        text='Global vs Indian Workforce Distribution',
        font=dict(size=24, family='Arial Black'),
        y=0.95
    ),
    height=700,
    template='plotly_white',
    font=dict(family='Arial', size=14),
    plot_bgcolor='rgba(245,245,245,1)',  # Slightly darker background
    paper_bgcolor='rgba(245,245,245,1)',  # Matching paper background
    margin=dict(l=250, r=250, t=130, b=50),
    legend=dict(
        yanchor="bottom",
        y=1.12,
        xanchor="center",
        x=0.5,
        orientation="h",
        bgcolor='rgba(255,255,255,0.9)',  # White background for legend
        bordercolor='rgba(0,0,0,0.1)',    # Light border for legend
        borderwidth=1
    ),
    annotations=[
        dict(
            text="Source: world_and_india_workforce_data.csv",
            xref="paper", yref="paper",
            x=1, y=-0.1,
            showarrow=False,
            font=dict(size=10)
        )
    ]
)

# Update axes with slightly darker grid
fig.update_xaxes(
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(200,200,200,0.5)',  # Darker grid lines
    title_text='Population Count (Millions)'
)

# Update y-axes
fig.update_yaxes(
    showgrid=False,
    autorange="reversed",
    side="left",
    row=1, col=1
)

fig.update_yaxes(
    showgrid=False,
    autorange="reversed",
    side="right",
    row=1, col=2
)

# Add indentation to categories using spaces
def add_indentation(df):
    df['Category'] = df.apply(lambda row: "   " * row['Level'] + row['Category'], axis=1)
    return df

df_world = add_indentation(df_world)
df_india = add_indentation(df_india)

# Save and show the visualization
fig.write_html('global_india_workforce_hierarchy.html')
fig.show() 