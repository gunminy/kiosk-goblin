import plotly.graph_objects as go

# Monochrome matrix-green scale
THEME_COLORS = {
    'primary': '#00ff41',      # Classic Matrix green
    'secondary': '#00cc33',    # Standard green
    'success': '#00ff66',      # Neon light green
    'warning': '#008f11',      # Dark Matrix green
    'danger': '#ff3333',       # Warning/Error red (kept minimal)
    'purple': '#005500',       # Very dark green
    'orange': '#00aa00',       # Mid dark green
    'bg': 'rgba(0, 0, 0, 0)',
}

def apply_dark_theme(fig, height=250, width=None):
    """
    Applies the Matrix dark terminal theme to Plotly figures.
    Optimized for container scaling (autosize=True).
    """
    layout_args = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(
            family="'Fira Code', 'Courier New', monospace",
            color='#00ff41',
            size=11
        ),
        margin=dict(l=10, r=10, t=35, b=10),
        height=height,
        autosize=True,  # Let Plotly handle internal resizing smoothly
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=10)
        ),
        hoverlabel=dict(
            bgcolor="#000000",
            font_size=12,
            font_family="'Fira Code', monospace",
            font_color="#00ff41",
            bordercolor="rgba(0, 255, 65, 0.4)"
        ),
        dragmode=False
    )
    
    if width is not None:
        layout_args['width'] = width
        
    fig.update_layout(**layout_args)
    
    # Configure axes with subtle green grid lines
    fig.update_xaxes(
        showgrid=True,
        gridcolor='rgba(0, 255, 65, 0.05)',
        zeroline=False,
        tickfont=dict(color='#008f11'),
        linecolor='rgba(0, 255, 65, 0.2)'
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor='rgba(0, 255, 65, 0.05)',
        zeroline=False,
        tickfont=dict(color='#008f11'),
        linecolor='rgba(0, 255, 65, 0.2)'
    )
    
    return fig
