import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
import torch


# to avoid torch "path doesn't exist error"
torch.classes.__path__ = []

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def fetch_news_articles(company_name, max_articles=10):
    base_url = f"https://indianexpress.com/about/{company_name}/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html5lib')
    
    articles = []
    for div in soup.find_all('div', class_="img-context")[:max_articles]:
        title = div.find('h3').find('a').text
        date_p = div.find('p')
        date = date_p.text
        content = date_p.find_next_sibling('p').text

        articles.append({
            'title': title,
            'content': content,
            'date': date
        })
        
    return articles

def analyze_sentiment(text):
    result = sentiment_pipeline(text)
    return result[0]['label']

def get_sentiment_color(sentiment):
    sentiment = sentiment.lower()
    if sentiment == 'positive':
        return 'MediumSeaGreen'
    elif sentiment == 'neutral':
        return 'DodgerBlue'
    else:
        return 'red'
    
def translate_to_hindi(text):
    """Translate English text to Hindi"""
    translator = GoogleTranslator(source='en', target='hi')
    translation = translator.translate(text)
    return translation

def convert_to_speech(client, text, output_file="output.mp3", model="gpt-4o-mini-tts", voice="alloy"):
    """Convert text to speech using OpenAI's TTS API"""
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    response.stream_to_file(output_file)
    return output_file

def hindi_speech(client, text, output_file="comparison_hindi.mp3"):
    """Convert English text to Hindi speech"""
    # translate to hindi text
    hindi_text = translate_to_hindi(text)
    
    # create speech
    speech_file = convert_to_speech(client, hindi_text, output_file)
    
    return {
        'original_text': text,
        'hindi_text': hindi_text,
        'audio_file': speech_file
    }