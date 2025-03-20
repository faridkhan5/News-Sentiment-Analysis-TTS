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
    return result[0]['label']

def get_articles_sentiment(articles):
    if not articles:
        return []

    return [
        {
            'title': article.get('title', 'Untitled'),
            'content': article['content'],
            'sentiment': analyze_sentiment(article['content'])   
        }
        for article in articles
    ]

def compare_articles(articles):
    articles_content = []
    for article in articles:
        articles_content.append(article.get('content', ''))

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