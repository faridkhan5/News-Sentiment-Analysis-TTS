import requests
from bs4 import BeautifulSoup


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