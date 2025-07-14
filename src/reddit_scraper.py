import praw
import re

def initialize_reddit(client_id, client_secret, user_agent):
    """Initializes and returns a Reddit instance using PRAW."""
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    return reddit

def extract_username_from_url(url):
    """Extracts the username from a Reddit profile URL."""
    match = re.search(r'reddit\.com/user/([^/]+)', url)
    if match:
        return match.group(1)
    return None

def scrape_redditor_data(reddit, username, limit=None):
    """Scrapes comments and posts from a given Redditor."""
    redditor = reddit.redditor(username)
    scraped_data = {
        'comments': [],
        'posts': []
    }

    # Scrape comments
    for comment in redditor.comments.new(limit=limit):
        scraped_data['comments'].append({
            'id': comment.id,
            'body': comment.body,
            'score': comment.score,
            'created_utc': comment.created_utc,
            'permalink': comment.permalink
        })

    # Scrape posts
    for submission in redditor.submissions.new(limit=limit):
        scraped_data['posts'].append({
            'id': submission.id,
            'title': submission.title,
            'selftext': submission.selftext,
            'score': submission.score,
            'created_utc': submission.created_utc,
            'permalink': submission.permalink,
            'url': submission.url
        })
    return scraped_data

if __name__ == '__main__':
    # This is for testing purposes. Replace with your actual credentials.
    # It's recommended to use environment variables or a config file for production.
    CLIENT_ID = 'YOUR_CLIENT_ID'
    CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
    USER_AGENT = 'YOUR_USER_AGENT'

    reddit_instance = initialize_reddit(CLIENT_ID, CLIENT_SECRET, USER_AGENT)

    # Example usage:
    user_url = 'https://www.reddit.com/user/kojied/'
    username = extract_username_from_url(user_url)

    if username:
        print(f"Scraping data for user: {username}")
        data = scrape_redditor_data(reddit_instance, username, limit=10) # Limit to 10 for testing
        print("Scraped Comments:")
        for comment in data['comments']:
            print(f"- {comment['body'][:50]}... (Score: {comment['score']})")
        print("\nScraped Posts:")
        for post in data['posts']:
            print(f"- {post['title'][:50]}... (Score: {post['score']})")
    else:
        print("Invalid Reddit user URL.")


