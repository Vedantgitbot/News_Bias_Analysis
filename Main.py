import dash
from dash import html, dcc
from datetime import datetime
from Api import fetch_news
from Bias import process_article
from Graph import (
    prepare_dataframe,
    plot_sentiment_distribution,
    plot_bias_distribution,
    plot_fake_news_distribution,
    plot_sentiment_over_time
)
from GUI import create_dashboard_layout

raw_articles = fetch_news()

processed_articles = []
now = datetime.utcnow()

for article in raw_articles:
    content = article.get("content") or article.get("description") or article.get("title") or ""
    title = article.get("title") or article.get("description") or ""

    result = process_article(content, title)

    enriched_article = {
        **article,
        "fake_label": result["fake_label"],
        "fake_confidence": result["fake_confidence"],
        "bias_label": result["bias_label"],
        "bias_confidence": result["bias_confidence"],
        "sentiment": result.get("sentiment", "NEUTRAL"),
        "publishedAt": article.get("publishedAt") or now.isoformat(),
        "fetchedAt": article.get("fetchedAt") or now.isoformat()
    }

    print(enriched_article)  
    processed_articles.append(enriched_article)

df = prepare_dataframe(processed_articles)

app = dash.Dash(__name__)
app.title = "News Bias Scope"

app.layout = create_dashboard_layout(df)

if __name__ == "__main__":
    app.run(debug=True)
