import requests
from textblob import TextBlob
import json

# Function to fetch news articles from a News API
def fetch_news(search_query):

    # uses gnews api
    url = f"https://gnews.io/api/v4/search?q={search_query}&token=44d6a6d956e58c35d26ba83dfa50fa70"
    response = requests.get(url)
    articles = response.json().get('articles', [])

    news_data = []
    for article in articles:
        title = article['title']
        link = article['url']
        sentiment = analyze_sentiment(title)
        news_data.append({
            'title': title,
            'link': link,
            'sentiment': sentiment.polarity,
            'subjectivity': sentiment.subjectivity
        })
    return news_data

# Function to analyze sentiment of a text
def analyze_sentiment(text):
    return TextBlob(text).sentiment

# Function to store data in a local JSON file
def store_data(data, filename='news_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def print_article_details(article):
    print(f"Title: {article['title']}")
    print(f"Link: {article['link']}")
    print(f"Sentiment Polarity: {article['sentiment']}")
    print(f"Subjectivity: {article['subjectivity']}\n")

# Main function to run the fetch and sentiment analysis
def main(search_queries):
    all_news_data = []
    for query in search_queries:
        print(f"Fetching news for: {query}")
        news_data = fetch_news(query)
        for article in news_data:
            print_article_details(article)
        all_news_data.extend(news_data)
    store_data(all_news_data)


# Sample name provided by the project sponsors
search_queries = ['Piyush Gupta']

if __name__ == "__main__":
    main(search_queries)
