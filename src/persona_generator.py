import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

# Download necessary NLTK data (run once)
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

def analyze_text_for_keywords(text):
    """Analyzes text to extract keywords and their frequencies."""
    words = nltk.word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stopwords.words("english")]
    return Counter(filtered_words)

def generate_persona(scraped_data):
    """Generates a user persona based on scraped Reddit data with citations."""
    persona = {
        "name": "Reddit User", # Placeholder, can be improved with more advanced analysis
        "age_group": "Unknown",
        "interests": [],
        "sentiment": "Neutral",
        "common_topics": [],
        "citations": []
    }

    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"])
    for post in scraped_data["posts"]:
        all_text.append(post["title"])
        if post["selftext"]:
            all_text.append(post["selftext"])

    combined_text = " ".join(all_text)
    keywords = analyze_text_for_keywords(combined_text)

    # Simple interest and topic extraction (can be expanded with more sophisticated NLP)
    top_keywords = [word for word, count in keywords.most_common(10)]
    persona["common_topics"] = top_keywords

    # Simulate sentiment analysis (very basic, for demonstration)
    positive_words = ["love", "great", "happy", "good", "awesome"]
    negative_words = ["hate", "bad", "sad", "terrible", "worse"]

    sentiment_score = 0
    for word in nltk.word_tokenize(combined_text.lower()):
        if word in positive_words:
            sentiment_score += 1
        elif word in negative_words:
            sentiment_score -= 1

    if sentiment_score > 0:
        persona["sentiment"] = "Positive"
    elif sentiment_score < 0:
        persona["sentiment"] = "Negative"
    else:
        persona["sentiment"] = "Neutral"

    # Generate citations
    citation_id = 1
    for comment in scraped_data["comments"]:
        for keyword in persona["common_topics"]:
            if keyword in comment["body"].lower():
                persona["citations"].append({
                    "id": citation_id,
                    "type": "comment",
                    "content": comment["body"],
                    "permalink": f"https://www.reddit.com{comment['permalink']}"
                })
                citation_id += 1
                break # Cite once per comment for simplicity
        
    for post in scraped_data["posts"]:
        for keyword in persona["common_topics"]:
            if keyword in post["title"].lower() or (post["selftext"] and keyword in post["selftext"].lower()):
                persona["citations"].append({
                    "id": citation_id,
                    "type": "post",
                    "content": post["title"] + " " + (post["selftext"] if post["selftext"] else ""),
                    "permalink": f"https://www.reddit.com{post['permalink']}"
                })
                citation_id += 1
                break # Cite once per post for simplicity

    return persona

if __name__ == '__main__':
    # Example usage with dummy data
    dummy_scraped_data = {
        'comments': [
            {'id': 'c1', 'body': 'I love playing video games, especially RPGs.', 'score': 10, 'created_utc': 1678886400, 'permalink': '/r/gaming/comments/abcde/comment1'},
            {'id': 'c2', 'body': 'Just finished a great book on history. Highly recommend!', 'score': 5, 'created_utc': 1678972800, 'permalink': '/r/books/comments/fghij/comment2'},
            {'id': 'c3', 'body': 'The new movie was terrible, very disappointing.', 'score': 2, 'created_utc': 1679059200, 'permalink': '/r/movies/comments/klmno/comment3'}
        ],
        'posts': [
            {'id': 'p1', 'title': 'My favorite RPGs of all time', 'selftext': 'I enjoy games like The Witcher and Skyrim.', 'score': 20, 'created_utc': 1679145600, 'permalink': '/r/rpg/comments/pqrst', 'url': 'https://www.reddit.com/r/rpg/comments/pqrst'},
            {'id': 'p2', 'title': 'Discussion: Best historical documentaries', 'selftext': 'Looking for recommendations on documentaries about ancient civilizations.', 'score': 15, 'created_utc': 1679232000, 'permalink': '/r/history/comments/uvwxy', 'url': 'https://www.reddit.com/r/history/comments/uvwxy'}
        ]
    }

    persona = generate_persona(dummy_scraped_data)
    print("Generated Persona:")
    print(f"Name: {persona['name']}")
    print(f"Age Group: {persona['age_group']}")
    print(f"Interests: {persona['interests']}")
    print(f"Sentiment: {persona['sentiment']}")
    print(f"Common Topics: {', '.join(persona['common_topics'])}")
    print("\nCitations:")
    for citation in persona['citations']:
        print(f"[{citation['id']}] ({citation['type']}) {citation['content'][:70]}... - {citation['permalink']}")


