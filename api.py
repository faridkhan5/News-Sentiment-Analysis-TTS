import utils
import openai


class ArticleAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI()
    
    def get_articles_sentiment(self, articles):
        if not articles:
            return []

        sentiment_data = []
        for article in articles:
            sentiment = utils.analyze_sentiment(article['content'])
            sentiment_data.append({
                'title': article.get('title', 'Untitled'),
                'content': article['content'],
                'sentiment': sentiment,
                'sentiment_color': utils.get_sentiment_color(sentiment)  
            })
        return sentiment_data

    def compare_articles(self, articles):
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

        response = self.client.chat.completions.create(
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
    
    def get_hindi_speech(self, text):
        output = utils.hindi_speech(self.client, text)
        return output