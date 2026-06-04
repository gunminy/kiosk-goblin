import plotly.graph_objects as go

# Custom color palette for a beautiful cyberpunk/neon layout
THEME_COLORS = {
    'primary': '#00f2fe',      # Neon Blue
    'secondary': '#4facfe',    # Sky Blue
    'success': '#10b981',      # Emerald Green
    'warning': '#f59e0b',      # Golden Amber
    'danger': '#f43f5e',       # Rose/Red
    'purple': '#a855f7',       # Electric Purple
    'orange': '#f97316',       # Intense Orange
    'bg': 'rgba(11, 15, 25, 0.6)', # Card background alpha
}

def apply_dark_theme(fig, height=250):
    """
    Applies the custom Kiosk dark theme to any Plotly figure.
    Sets clean grid lines, transparent backgrounds, and neon-friendly colors.
    """
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="'Inter', 'Outfit', sans-serif",
            color='#94a3b8',
            size=11
        ),
        margin=dict(l=10, r=10, t=35, b=10),
        height=height,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10)
        ),
        hoverlabel=dict(
            bgcolor="#1e293b",
            font_size=12,
            font_family="'Fira Code', monospace"
        ),
        dragmode=False # Disable drag to zoom for kiosk usage
    )
    
    # Configure axes if present
    fig.update_xaxes(
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.05)',
        zeroline=False,
        tickfont=dict(color='#64748b'),
        linecolor='rgba(255, 255, 255, 0.1)'
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(255, 255, 255, 0.05)',
        zeroline=False,
        tickfont=dict(color='#64748b'),
        linecolor='rgba(255, 255, 255, 0.1)'
    )
    
    # Hide modebar completely for kiosk presentation
    fig.show = lambda *args, **kwargs: None # Mocking just in case
    return fig
