import pandas as pd
import plotly.express as px

def prepare_dataframe(articles):
    df = pd.DataFrame(articles)
    df = df[df["fake_label"].notna() & df["bias_label"].notna() & df["sentiment"].notna()]

    df["emotion"] = df["sentiment"].apply(
        lambda x: "happy" if x == "POSITIVE" else "sad" if x == "NEGATIVE" else "neutral"
    )

    if "publishedAt" in df.columns:
        df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")
    else:
        df["publishedAt"] = pd.NaT

    if "fetchedAt" in df.columns:
        df["fetchedAt"] = pd.to_datetime(df["fetchedAt"], errors="coerce")
    else:
        df["fetchedAt"] = pd.NaT

    return df

def plot_sentiment_distribution(df):
    if df.empty:
        return px.pie(title="No sentiment data available")
    return px.pie(df, names="emotion", title="Sentiment Distribution")

def plot_bias_distribution(df):
    if df.empty:
        return px.bar(title="No bias data available")
    bias_counts = df["bias_label"].value_counts().rename_axis("bias").reset_index(name="count")
    return px.bar(bias_counts, x="bias", y="count", title="Bias Classification")

def plot_fake_news_distribution(df):
    if df.empty:
        return px.pie(title="No fake/real news data available")
    return px.pie(df, names="fake_label", title="Fake News Detection")

def plot_sentiment_over_time(df):
    if df.empty or df["publishedAt"].isna().all():
        return px.line(title="No temporal sentiment data available")
    time_df = df.groupby([pd.Grouper(key="publishedAt", freq="D"), "emotion"]).size().reset_index(name="count")
    return px.line(time_df, x="publishedAt", y="count", color="emotion", title="Sentiment Over Time")
