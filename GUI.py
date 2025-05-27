from dash import html, dcc
from Graph import (
    plot_sentiment_distribution,
    plot_bias_distribution,
    plot_fake_news_distribution,
    plot_sentiment_over_time
)

def create_dashboard_layout(df):
    return html.Div(
        style={
            "fontFamily": "'Georgia', serif",
            "backgroundColor": "#fdfdfd",
            "color": "#111",
            "padding": "20px 40px",
            "maxWidth": "1200px",
            "margin": "auto",
        },
        children=[
            html.Div(
                "NewsBiasScope",
                style={
                    "textAlign": "center",
                    "fontSize": "48px",
                    "fontWeight": "bold",
                    "marginBottom": "10px",
                    "borderBottom": "2px solid #333",
                    "paddingBottom": "10px",
                }
            ),
            html.Div("News Insight Dashboard", style={"textAlign": "center", "fontSize": "20px", "marginBottom": "40px"}),
            
            html.Div(style={"marginBottom": "40px", "boxShadow": "0 2px 8px rgba(0,0,0,0.05)", "padding": "20px", "backgroundColor": "#fff", "border": "1px solid #ddd"}, children=[
                dcc.Graph(figure=plot_sentiment_distribution(df))
            ]),
            
            html.Div(style={"marginBottom": "40px", "boxShadow": "0 2px 8px rgba(0,0,0,0.05)", "padding": "20px", "backgroundColor": "#fff", "border": "1px solid #ddd"}, children=[
                dcc.Graph(figure=plot_bias_distribution(df))
            ]),
            
            html.Div(style={"marginBottom": "40px", "boxShadow": "0 2px 8px rgba(0,0,0,0.05)", "padding": "20px", "backgroundColor": "#fff", "border": "1px solid #ddd"}, children=[
                dcc.Graph(figure=plot_fake_news_distribution(df))
            ]),
            
            html.Div(style={"marginBottom": "40px", "boxShadow": "0 2px 8px rgba(0,0,0,0.05)", "padding": "20px", "backgroundColor": "#fff", "border": "1px solid #ddd"}, children=[
                dcc.Graph(figure=plot_sentiment_over_time(df))
            ])
        ]
    )
