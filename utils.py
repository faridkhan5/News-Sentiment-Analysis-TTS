import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from dotenv import load_dotenv
from deep_translator import GoogleTranslator


sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def fetch_news_articles(company_name, max_articles=10):
    base_url = f"https://economictimes.indiatimes.com/topic/{company_name}"
    response = requests.get(base_url)

    if response.status_code != 200:
        print("Failed to fetch news articles")
        return

    soup = BeautifulSoup(response.content, 'html5lib')
    titles = soup.find_all('a', class_="wrapLines l2")[:max_articles]
    contents = soup.find_all('p', class_="wrapLines l3")[:max_articles]
    dates = soup.find_all('time')[:max_articles]

    articles = []
    for i in range(len(titles)):
        title = titles[i].get_text()
        content = contents[i].get_text()
        date = dates[i].get_text()
        articles.append({
            'title': title,
            'content': content,
            'date': date,
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
    # Translate to Hindi
    hindi_text = translate_to_hindi(text)
    
    # Create speech using OpenAI's TTS
    speech_file = convert_to_speech(client, hindi_text, output_file)
    
    return {
        'original_text': text,
        'hindi_text': hindi_text,
        'audio_file': speech_file
    }