from scraper import fetch_news_articles

from textblob import TextBlob
from transformers import pipeline


def analyze_sentiment(text):
    sentiment_pipeline = pipeline("sentiment-analysis",  model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")
    result = sentiment_pipeline(text)
    sentiment = result[0]['label']
    return sentiment

def get_article_sentiment(article):
    content = article['content']
    if not content:
        return None

    sentiment = analyze_sentiment(content)
    summary = {
        'title': article['title'],
        'sentiment': sentiment
    }
    return summary

def get_company_sentiment(company_name, max_articles=10):
    articles = fetch_news_articles(company_name, max_articles)
    if not articles:
        return None
    return [get_article_sentiment(article) for article in articles]