# New_Bias_Analysis

New_Bias_Analysis is a dashboard-powered Python app that detects **bias**, **fake news**, and **sentiment** in real-time political news articles. It leverages NLP models from HuggingFace and visualizes insights using Plotly Dash.

## 🔍 Features

- **Sentiment Analysis** — Detects the tone (happy/sad) of news content.
- **Bias Classification** — Classifies articles as neutral, left, or right-leaning.
- **Fake News Detection** — Distinguishes between fake and real articles.
- **Interactive Dashboard** — Visualizes data across time and categories.

## 🛠️ Tech Stack

- `Python`
- `Plotly Dash`
- `Transformers (HuggingFace)`
- `GNews API` (fallback to sample articles if inactive)
- `Pandas`, `Plotly`, `Requests`

## ⚙️ How to Run

```bash
git clone https://github.com/your-username/NewsBiasScope.git
cd NewsBiasScope
pip install -r requirements.txt
python Main.py
