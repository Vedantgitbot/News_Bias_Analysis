from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import torch.nn.functional as F
import re

device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")

fake_model_name = "mrm8488/bert-tiny-finetuned-fake-news-detection"
fake_tokenizer = AutoTokenizer.from_pretrained(fake_model_name)
fake_model = AutoModelForSequenceClassification.from_pretrained(fake_model_name).to(device)

nli_model_name = "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
nli_tokenizer = AutoTokenizer.from_pretrained(nli_model_name)
nli_model = AutoModelForSequenceClassification.from_pretrained(nli_model_name).to(device)

sentiment_analyzer = pipeline("sentiment-analysis", device=0 if torch.cuda.is_available() else -1)

def clean_text(text):
    text = str(text or "")
    text = re.sub(r"<.*?>", "", text)
    return text.replace("\n", " ").replace("\r", "").strip()

def detect_fake_news(text):
    text = clean_text(text)
    if not text:
        return "unknown", 0.0
    inputs = fake_tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = fake_model(**inputs)
    probs = F.softmax(outputs.logits, dim=-1)
    pred_class = torch.argmax(probs, dim=1).item()
    labels = ["fake", "real"]
    return labels[pred_class], round(probs[0][pred_class].item(), 3)

def check_bias(article_text, claim_text):
    article_text = clean_text(article_text)
    claim_text = clean_text(claim_text)
    if not article_text or not claim_text:
        return "neutral", 0.0
    inputs = nli_tokenizer(claim_text, article_text, return_tensors="pt", truncation=True, padding=True).to(device)
    outputs = nli_model(**inputs)
    probs = F.softmax(outputs.logits, dim=-1)
    pred_class = torch.argmax(probs, dim=1).item()
    nli_labels = ["entailment", "neutral", "contradiction"]
    nli_result = nli_labels[pred_class]
    if nli_result == "entailment":
        bias_label = "unbiased"
    elif nli_result == "contradiction":
        bias_label = "biased"
    else:
        bias_label = "neutral"
    return bias_label, round(probs[0][pred_class].item(), 3)

def detect_sentiment(text):
    text = clean_text(text)
    if not text:
        return "NEUTRAL"
    try:
        result = sentiment_analyzer(text[:512])[0]
        return result["label"].upper()
    except:
        return "NEUTRAL"

def process_article(article, claim):
    article = clean_text(article)
    claim = clean_text(claim)
    if not article:
        return {
            "title": claim,
            "content": article,
            "fake_label": "unknown",
            "fake_confidence": 0.0,
            "bias_label": "neutral",
            "bias_confidence": 0.0,
            "sentiment": "NEUTRAL"
        }
    fake_label, fake_confidence = detect_fake_news(article)
    bias_label, bias_confidence = check_bias(article, claim)
    sentiment = detect_sentiment(article)
    return {
        "title": claim,
        "content": article,
        "fake_label": fake_label,
        "fake_confidence": fake_confidence,
        "bias_label": bias_label,
        "bias_confidence": bias_confidence,
        "sentiment": sentiment
    }
