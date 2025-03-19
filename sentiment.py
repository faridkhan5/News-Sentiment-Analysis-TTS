from textblob import TextBlob
import requests
from bs4 import BeautifulSoup
from scraper import fetch_news_articles


def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'

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

def get_company_sentiment(company_name, max_articles):
    articles = fetch_news_articles(company_name, max_articles)
    if not articles:
        return None
    return [get_article_sentiment(article) for article in articles]