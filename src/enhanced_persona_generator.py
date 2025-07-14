import nltk
from nltk.corpus import stopwords
from collections import Counter
import re
import random
from datetime import datetime

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

def extract_demographics(scraped_data, username):
    """Extract demographic information from Reddit data."""
    # Basic demographic inference (can be enhanced with more sophisticated analysis)
    age_indicators = {
        'teen': ['school', 'homework', 'parents', 'teenager', 'high school'],
        'young_adult': ['college', 'university', 'student', 'graduation', 'first job'],
        'adult': ['work', 'job', 'career', 'mortgage', 'marriage', 'kids'],
        'middle_aged': ['retirement', 'children', 'family', 'house', 'savings'],
        'senior': ['grandchildren', 'pension', 'retired', 'medicare']
    }
    
    location_indicators = {
        'US': ['america', 'usa', 'united states', 'dollar', 'fahrenheit'],
        'UK': ['britain', 'england', 'uk', 'pound', 'celsius', 'london'],
        'Canada': ['canada', 'toronto', 'vancouver', 'canadian'],
        'Australia': ['australia', 'sydney', 'melbourne', 'aussie']
    }
    
    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"].lower())
    for post in scraped_data["posts"]:
        all_text.append(post["title"].lower())
        if post["selftext"]:
            all_text.append(post["selftext"].lower())
    
    combined_text = " ".join(all_text)
    
    # Age estimation
    age_group = "Unknown"
    age_scores = {}
    for age, indicators in age_indicators.items():
        score = sum(combined_text.count(indicator) for indicator in indicators)
        age_scores[age] = score
    
    if age_scores:
        age_group = max(age_scores, key=age_scores.get)
        if age_scores[age_group] == 0:
            age_group = "Unknown"
    
    # Location estimation
    location = "Unknown"
    location_scores = {}
    for loc, indicators in location_indicators.items():
        score = sum(combined_text.count(indicator) for indicator in indicators)
        location_scores[loc] = score
    
    if location_scores:
        location = max(location_scores, key=location_scores.get)
        if location_scores[location] == 0:
            location = "Unknown"
    
    return {
        'age_group': age_group,
        'location': location
    }

def analyze_personality_traits(scraped_data):
    """Analyze personality traits based on Reddit activity."""
    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"].lower())
    for post in scraped_data["posts"]:
        all_text.append(post["title"].lower())
        if post["selftext"]:
            all_text.append(post["selftext"].lower())
    
    combined_text = " ".join(all_text)
    
    # MBTI-style personality analysis
    personality_indicators = {
        'extrovert': ['party', 'social', 'friends', 'meeting', 'group', 'people'],
        'introvert': ['alone', 'quiet', 'home', 'solitude', 'reading', 'myself'],
        'thinking': ['logic', 'analysis', 'rational', 'facts', 'data', 'objective'],
        'feeling': ['emotions', 'feelings', 'empathy', 'heart', 'care', 'love'],
        'judging': ['plan', 'schedule', 'organized', 'structure', 'deadline'],
        'perceiving': ['flexible', 'spontaneous', 'adapt', 'open', 'explore'],
        'sensing': ['practical', 'realistic', 'details', 'facts', 'experience'],
        'intuition': ['creative', 'imagination', 'possibilities', 'future', 'ideas']
    }
    
    trait_scores = {}
    for trait, indicators in personality_indicators.items():
        score = sum(combined_text.count(indicator) for indicator in indicators)
        trait_scores[trait] = score
    
    # Determine dominant traits
    personality = {
        'extrovert_introvert': 'extrovert' if trait_scores.get('extrovert', 0) > trait_scores.get('introvert', 0) else 'introvert',
        'thinking_feeling': 'thinking' if trait_scores.get('thinking', 0) > trait_scores.get('feeling', 0) else 'feeling',
        'judging_perceiving': 'judging' if trait_scores.get('judging', 0) > trait_scores.get('perceiving', 0) else 'perceiving',
        'sensing_intuition': 'sensing' if trait_scores.get('sensing', 0) > trait_scores.get('intuition', 0) else 'intuition'
    }
    
    return personality

def analyze_motivations(scraped_data):
    """Analyze user motivations based on Reddit activity."""
    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"].lower())
    for post in scraped_data["posts"]:
        all_text.append(post["title"].lower())
        if post["selftext"]:
            all_text.append(post["selftext"].lower())
    
    combined_text = " ".join(all_text)
    
    motivation_indicators = {
        'convenience': ['easy', 'quick', 'simple', 'convenient', 'fast', 'efficient'],
        'wellness': ['health', 'fitness', 'exercise', 'diet', 'wellness', 'healthy'],
        'speed': ['fast', 'quick', 'rapid', 'immediate', 'instant', 'speed'],
        'preferences': ['like', 'prefer', 'favorite', 'enjoy', 'love', 'choose'],
        'comfort': ['comfort', 'cozy', 'relaxing', 'peaceful', 'calm', 'safe'],
        'dietary_needs': ['diet', 'nutrition', 'food', 'eating', 'meal', 'recipe']
    }
    
    motivation_scores = {}
    for motivation, indicators in motivation_indicators.items():
        score = sum(combined_text.count(indicator) for indicator in indicators)
        motivation_scores[motivation] = score
    
    # Normalize scores to 0-100 scale
    max_score = max(motivation_scores.values()) if motivation_scores.values() else 1
    normalized_scores = {k: int((v / max_score) * 100) if max_score > 0 else 0 
                        for k, v in motivation_scores.items()}
    
    return normalized_scores

def extract_behaviors_and_habits(scraped_data):
    """Extract behavior patterns and habits from Reddit data."""
    behaviors = []
    
    # Analyze posting patterns
    post_count = len(scraped_data["posts"])
    comment_count = len(scraped_data["comments"])
    
    if post_count > comment_count:
        behaviors.append("Tends to create original content rather than just commenting on others' posts.")
    elif comment_count > post_count * 2:
        behaviors.append("More likely to engage in discussions and comment on others' content.")
    
    # Analyze content themes
    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"].lower())
    for post in scraped_data["posts"]:
        all_text.append(post["title"].lower())
        if post["selftext"]:
            all_text.append(post["selftext"].lower())
    
    combined_text = " ".join(all_text)
    
    # Technology usage patterns
    tech_indicators = ['online', 'app', 'website', 'digital', 'internet', 'computer']
    if any(indicator in combined_text for indicator in tech_indicators):
        behaviors.append("Shows high comfort level with technology and digital platforms.")
    
    # Social patterns
    social_indicators = ['friends', 'family', 'social', 'party', 'meeting']
    if any(indicator in combined_text for indicator in social_indicators):
        behaviors.append("Demonstrates active social engagement and relationship building.")
    
    # Work patterns
    work_indicators = ['work', 'job', 'office', 'career', 'professional']
    if any(indicator in combined_text for indicator in work_indicators):
        behaviors.append("Frequently discusses work-related topics and professional development.")
    
    return behaviors

def extract_goals_and_needs(scraped_data):
    """Extract user goals and needs from Reddit activity."""
    goals = []
    
    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"].lower())
    for post in scraped_data["posts"]:
        all_text.append(post["title"].lower())
        if post["selftext"]:
            all_text.append(post["selftext"].lower())
    
    combined_text = " ".join(all_text)
    
    # Goal indicators
    goal_patterns = {
        'learning': ['learn', 'study', 'education', 'knowledge', 'skill'],
        'health': ['health', 'fitness', 'exercise', 'diet', 'wellness'],
        'career': ['career', 'job', 'promotion', 'professional', 'work'],
        'relationships': ['relationship', 'dating', 'marriage', 'family', 'friends'],
        'financial': ['money', 'savings', 'investment', 'financial', 'budget']
    }
    
    for goal_type, indicators in goal_patterns.items():
        if any(indicator in combined_text for indicator in indicators):
            if goal_type == 'learning':
                goals.append("To continuously learn and develop new skills.")
            elif goal_type == 'health':
                goals.append("To maintain a healthy lifestyle and improve physical well-being.")
            elif goal_type == 'career':
                goals.append("To advance professionally and achieve career goals.")
            elif goal_type == 'relationships':
                goals.append("To build and maintain meaningful relationships.")
            elif goal_type == 'financial':
                goals.append("To achieve financial stability and security.")
    
    return goals

def extract_frustrations(scraped_data):
    """Extract user frustrations from Reddit activity."""
    frustrations = []
    
    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"].lower())
    for post in scraped_data["posts"]:
        all_text.append(post["title"].lower())
        if post["selftext"]:
            all_text.append(post["selftext"].lower())
    
    combined_text = " ".join(all_text)
    
    # Frustration indicators
    frustration_indicators = ['annoying', 'frustrating', 'hate', 'terrible', 'awful', 'worst', 'problem', 'issue']
    negative_sentiment_phrases = []
    
    sentences = nltk.sent_tokenize(combined_text)
    for sentence in sentences:
        if any(indicator in sentence for indicator in frustration_indicators):
            negative_sentiment_phrases.append(sentence.strip())
    
    # Convert to user-friendly frustration statements
    if negative_sentiment_phrases:
        for phrase in negative_sentiment_phrases[:3]:  # Limit to top 3
            frustrations.append(f"Experiences difficulty with: {phrase[:100]}...")
    
    return frustrations

def generate_enhanced_persona(scraped_data, username):
    """Generates a comprehensive user persona based on scraped Reddit data."""
    demographics = extract_demographics(scraped_data, username)
    personality = analyze_personality_traits(scraped_data)
    motivations = analyze_motivations(scraped_data)
    behaviors = extract_behaviors_and_habits(scraped_data)
    goals = extract_goals_and_needs(scraped_data)
    frustrations = extract_frustrations(scraped_data)
    
    # Generate common topics
    all_text = []
    for comment in scraped_data["comments"]:
        all_text.append(comment["body"])
    for post in scraped_data["posts"]:
        all_text.append(post["title"])
        if post["selftext"]:
            all_text.append(post["selftext"])
    
    combined_text = " ".join(all_text)
    keywords = analyze_text_for_keywords(combined_text)
    top_keywords = [word for word, count in keywords.most_common(10)]
    
    # Sentiment analysis
    positive_words = ["love", "great", "happy", "good", "awesome", "excellent", "amazing"]
    negative_words = ["hate", "bad", "sad", "terrible", "worse", "awful", "horrible"]
    
    sentiment_score = 0
    for word in nltk.word_tokenize(combined_text.lower()):
        if word in positive_words:
            sentiment_score += 1
        elif word in negative_words:
            sentiment_score -= 1
    
    if sentiment_score > 0:
        sentiment = "Positive"
    elif sentiment_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    # Generate citations
    citations = []
    citation_id = 1
    
    for comment in scraped_data["comments"][:5]:  # Limit citations
        citations.append({
            "id": citation_id,
            "type": "comment",
            "content": comment["body"],
            "permalink": f"https://www.reddit.com{comment['permalink']}",
            "score": comment["score"]
        })
        citation_id += 1
    
    for post in scraped_data["posts"][:5]:  # Limit citations
        citations.append({
            "id": citation_id,
            "type": "post",
            "content": post["title"] + " " + (post["selftext"] if post["selftext"] else ""),
            "permalink": f"https://www.reddit.com{post['permalink']}",
            "score": post["score"]
        })
        citation_id += 1
    
    # Estimate age and occupation based on content
    age_mapping = {
        'teen': '16-19',
        'young_adult': '20-25',
        'adult': '26-40',
        'middle_aged': '41-55',
        'senior': '55+'
    }
    
    estimated_age = age_mapping.get(demographics['age_group'], 'Unknown')
    
    # Generate archetype based on activity patterns
    archetypes = ['The Creator', 'The Explorer', 'The Analyst', 'The Connector', 'The Helper']
    archetype = random.choice(archetypes)  # Can be enhanced with more sophisticated analysis
    
    persona = {
        "name": username.title(),
        "age": estimated_age,
        "occupation": "Unknown",  # Would need more sophisticated analysis
        "status": "Unknown",      # Would need more sophisticated analysis
        "location": demographics['location'],
        "tier": "Regular User",   # Based on activity level
        "archetype": archetype,
        "personality": personality,
        "motivations": motivations,
        "behaviors_habits": behaviors,
        "goals_needs": goals,
        "frustrations": frustrations,
        "common_topics": top_keywords,
        "sentiment": sentiment,
        "citations": citations,
        "quote": f"Based on {len(scraped_data['comments'])} comments and {len(scraped_data['posts'])} posts analyzed."
    }
    
    return persona

if __name__ == '__main__':
    # Example usage with dummy data
    dummy_scraped_data = {
        'comments': [
            {'id': 'c1', 'body': 'I love playing video games, especially RPGs. They help me relax after work.', 'score': 10, 'created_utc': 1678886400, 'permalink': '/r/gaming/comments/abcde/comment1'},
            {'id': 'c2', 'body': 'Just finished a great book on history. Highly recommend for anyone interested in learning!', 'score': 5, 'created_utc': 1678972800, 'permalink': '/r/books/comments/fghij/comment2'},
            {'id': 'c3', 'body': 'The new movie was terrible, very disappointing. Wasted my time and money.', 'score': 2, 'created_utc': 1679059200, 'permalink': '/r/movies/comments/klmno/comment3'}
        ],
        'posts': [
            {'id': 'p1', 'title': 'My favorite RPGs of all time', 'selftext': 'I enjoy games like The Witcher and Skyrim. They offer great escapism.', 'score': 20, 'created_utc': 1679145600, 'permalink': '/r/rpg/comments/pqrst', 'url': 'https://www.reddit.com/r/rpg/comments/pqrst'},
            {'id': 'p2', 'title': 'Discussion: Best historical documentaries', 'selftext': 'Looking for recommendations on documentaries about ancient civilizations.', 'score': 15, 'created_utc': 1679232000, 'permalink': '/r/history/comments/uvwxy', 'url': 'https://www.reddit.com/r/history/comments/uvwxy'}
        ]
    }
    
    persona = generate_enhanced_persona(dummy_scraped_data, "testuser")
    print("Generated Enhanced Persona:")
    print(f"Name: {persona['name']}")
    print(f"Age: {persona['age']}")
    print(f"Location: {persona['location']}")
    print(f"Archetype: {persona['archetype']}")
    print(f"Personality: {persona['personality']}")
    print(f"Motivations: {persona['motivations']}")

