import requests
from datetime import datetime

GNEWS_API_KEY = "79c3b31329341a977b29df7da05ed6e6"
GNEWS_BASE_URL = "https://gnews.io/api/v4/search"

NEWSAPI_KEY = "your_newsapi_key_here"
NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(query="politics", lang="en", country="us", max_articles=20):
    articles = fetch_from_gnews(query, lang, country, max_articles)
    if not articles:
        articles = fetch_from_newsapi(query, lang, max_articles)
    return articles or get_sample_article()

def fetch_from_gnews(query, lang, country, max_articles):
    params = {
        "q": query,
        "lang": lang,
        "country": country,
        "token": GNEWS_API_KEY,
        "max": max_articles
    }
    try:
        response = requests.get(GNEWS_BASE_URL, params=params)
        print("GNews API Status:", response.status_code)
        print("GNews Response:", response.text)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        return [{
            "title": a.get("title"),
            "content": a.get("content"),
            "description": a.get("description"),
            "url": a.get("url"),
            "source": a.get("source", {}).get("name"),
            "publishedAt": a.get("publishedAt"),
            "fetchedAt": datetime.utcnow().isoformat()
        } for a in articles]
    except requests.RequestException as e:
        print("GNews fetch error:", str(e))
        return []


def fetch_from_newsapi(query, lang, max_articles):
    params = {
        "q": query,
        "language": lang,
        "apiKey": NEWSAPI_KEY,
        "pageSize": max_articles
    }
    try:
        response = requests.get(NEWSAPI_BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])
        return [{
            "title": a.get("title"),
            "content": a.get("content"),
            "description": a.get("description"),
            "url": a.get("url"),
            "source": a.get("source", {}).get("name"),
            "publishedAt": a.get("publishedAt"),
            "fetchedAt": datetime.utcnow().isoformat()
        } for a in articles]
    except requests.RequestException:
        return []

def get_sample_article():
    return [{
        "title": "Sample News",
        "content": "This is a fallback article due to API error.",
        "description": "Fallback description",
        "url": "#",
        "source": "Local",
        "publishedAt": datetime.utcnow().isoformat(),
        "fetchedAt": datetime.utcnow().isoformat()
    }]
