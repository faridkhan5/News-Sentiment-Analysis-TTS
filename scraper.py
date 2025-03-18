import requests
from bs4 import BeautifulSoup


def fetch_news_articles(company_name, max_articles=10):
    # url = f"https://www.google.com/search?q={company}&tbm=nws"
    base_url = f"https://news.google.com/rss/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"
    response = requests.get(base_url)

    if response.status_code != 200:
        print("Failed to fetch news articles")
        return

    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')[:max_articles]

    articles = []
    for item in items:
        title = item.title.text
        link = item.link.text
        pub_date = item.pubDate.text
        source = item.source.text if item.source else "Unknown"
        articles.append({
            'title': title,
            'link': link,
            'pub_date': pub_date,
            'source': source
        })
    
    return articles