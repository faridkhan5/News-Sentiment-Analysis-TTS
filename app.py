from api import ArticleAnalyzer
import utils

import streamlit as st
from dotenv import load_dotenv


def main():
    load_dotenv()

    analyzer = ArticleAnalyzer()


    st.title("News Sentiment Analysis with TTS")

    st.text_input("Enter Company name", key='company')

# Sentiment
    articles = utils.fetch_news_articles(st.session_state.company, 10)
    articles_sentiment = analyzer.get_articles_sentiment(articles)
    sentiment_count = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
}

    for i, article in enumerate(articles_sentiment):
        sentiment_count[article['sentiment'].lower()] += 1
        st.markdown(f"""
            ### Article {i+1}
            ***Title:*** {article['title']}  
            ***Content:*** {article['content']}  
            ***Sentiment:*** <span style="color:{article['sentiment_color']}; font-weight:bold; font-family: 'Courier New', monospace;">{article['sentiment']}</span>
        """, unsafe_allow_html=True)

    st.markdown(f"""
                ### Sentiment Results
                <span style="color: MediumSeaGreen; font-weight: bold; font-family: 'Courier New', monospace;">
                    Positive: {sentiment_count['positive']}
                </span>
                <br>
                <span style="color: DodgerBlue; font-weight: bold; font-family: 'Courier New', monospace;">
                    Neutral: {sentiment_count['neutral']}
                </span>
                <br>
                <span style="color: red; font-weight: bold; font-family: 'Courier New', monospace;">
                    Negative: {sentiment_count['negative']}
                </span>
    """, unsafe_allow_html=True)

    # Comparsion
    st.markdown("### Comparsion Analysis")
    comparsion = analyzer.compare_articles(articles)
    st.markdown(comparsion)

    # TTS
    st.markdown("### Hindi TTS")
    if st.button("Generate Hindi Speech"):
        with st.spinner("Generating audio..."):
            tts_output = analyzer.get_hindi_speech(comparsion)
            if tts_output:
                st.audio(tts_output['audio_file'], format='audio/mp3')

if __name__ == "__main__":
    main()