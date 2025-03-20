from scraper import fetch_news_articles

from textblob import TextBlob
from transformers import pipeline
from dotenv import load_dotenv
import os
import openai


load_dotenv()
sentiment_pipeline = pipeline("sentiment-analysis",  model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text):
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
        'content': article['content'],
        'sentiment': sentiment
    }
    return summary

def get_company_articles_sentiment(company_name, max_articles=10):
    articles = fetch_news_articles(company_name, max_articles)
    if not articles:
        return None
    return [get_article_sentiment(article) for article in articles]

def compare_articles(articles):
    articles_content = []
    for article in articles:
        articles_content.append(article['content'])

    merged_articles = ""
    for i, article in enumerate(articles_content):
        curr_article = f"article {i+1}: " + article + "\n"
        merged_articles += curr_article

    prompt = f"""compare the following news articles of a company and provide the response in the given format:
    1. comparsion: highlight the similarities if certain articles are similar or the differences if they are different.
    2. impact: highlight the impact of certain articles on the company.
    3. conclusion: final sentiment analysis after looking at all articles and state the reason for it.
    always mention article number when specifying an article.
    make sure the responses are conscise.

    articles: {merged_articles}
    """

    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                'role': 'system',
                'content': "You are a helpful assistant that analyzes news articles."
            },
            {
                'role': 'user',
                'content': prompt
            },
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()