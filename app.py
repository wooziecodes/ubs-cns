import praw
from flask import Flask, render_template, jsonify
from textblob import TextBlob
import json

app = Flask(__name__)


# Function to set up the Reddit API connection
def setup_reddit():
    return praw.Reddit(
        client_id="ztJ9CLtotBA8oS1nzjVxxA",  # Replace with your client id
        client_secret="8jsktMIs5IK_k5McCE1qIso2sjMtjw",  # Replace with your client secret
        user_agent="DealMaleficent5446"  # Replace with your user agent
    )

# Function to fetch submissions and top comments from Reddit based on search query
def fetch_reddit_posts(search_query, reddit):
    posts_data = []
    for submission in reddit.subreddit("all").search(search_query, limit=10):  # Change the limit as needed
        # Get top comments from the submission
        submission.comments.replace_more(limit=None)  # Replace MoreComments objects
        comments = submission.comments.list()
        comments_data = []
        for comment in comments[:10]:  # Limit to top 10 comments for example
            comment_sentiment = analyze_sentiment(comment.body)
            comments_data.append({
                'body': comment.body,
                'sentiment': comment_sentiment.polarity,
                'subjectivity': comment_sentiment.subjectivity
            })
        
        sentiment = analyze_sentiment(submission.title)
        posts_data.append({
            'title': submission.title,
            'link': f"https://www.reddit.com{submission.permalink}",
            'sentiment': sentiment.polarity,
            'subjectivity': sentiment.subjectivity,
            'comments': comments_data
        })
    return posts_data

# Function to analyze sentiment of a text
def analyze_sentiment(text):
    return TextBlob(text).sentiment

# Function to store data in a local JSON file
def store_data(data, filename='reddit_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Function to print submission and comment details
def print_submission_details(post):
    print(f"Title: {post['title']}")
    print(f"Link: {post['link']}")
    print(f"Sentiment Polarity: {post['sentiment']}")
    print(f"Subjectivity: {post['subjectivity']}")
    for comment in post['comments']:
        print(f"\tComment Sentiment Polarity: {comment['sentiment']}")
        print(f"\tComment Subjectivity: {comment['subjectivity']}\n")

# Main function to run the fetch and sentiment analysis
def main(search_queries):
    reddit = setup_reddit()
    all_posts_data = []
    for query in search_queries:
        print(f"Fetching Reddit posts for: {query}")
        posts_data = fetch_reddit_posts(query, reddit)
        for post in posts_data:
            print_submission_details(post)
        all_posts_data.extend(posts_data)
    store_data(all_posts_data)

# Sample name provided by the project sponsors
search_queries = ['Piyush Gupta']

@app.route('/')
def index():
    return render_template('index.html')  # Frontend HTML file

@app.route('/fetch-sentiment/<search_query>')
def fetch_sentiment(search_query):
    reddit = setup_reddit()
    posts_data = fetch_reddit_posts(search_query, reddit)
    return jsonify(posts_data)  # Returns the sentiment data as JSON

if __name__ == '__main__':
    app.run(debug=True)