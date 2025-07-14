import google.generativeai as genai
import json
import re

def generate_enhanced_persona(scraped_data, username, google_api_key):
    """Generates a comprehensive user persona using the Gemini LLM."""
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    all_comments = [comment['body'] for comment in scraped_data['comments']]
    all_posts = []
    for post in scraped_data['posts']:
        all_posts.append(post['title'])
        if post['selftext']:
            all_posts.append(post['selftext'])

    combined_text = " ".join(all_comments + all_posts)

    # Prepare the prompt for the LLM
    prompt = f"""
    Analyze the following Reddit user's comments and posts to generate a detailed user persona.
    The persona should be returned as a JSON object with the following structure:

    {{
        "name": "string", // The Reddit username, capitalized
        "age": "string", // Estimated age range (e.g., "20-25", "30-40", "Unknown")
        "occupation": "string", // Estimated occupation (e.g., "Software Engineer", "Student", "Unknown")
        "status": "string", // Estimated relationship status or general life status (e.g., "Single", "Married", "Student", "Working Professional", "Unknown")
        "location": "string", // Estimated general location (e.g., "North America", "Europe", "Unknown")
        "tier": "string", // User activity tier (e.g., "Casual User", "Active Contributor", "Power User")
        "archetype": "string", // A user archetype (e.g., "The Explorer", "The Analyst", "The Helper")
        "personality": {{
            "extrovert_introvert": "string", // "extrovert" or "introvert"
            "thinking_feeling": "string", // "thinking" or "feeling"
            "judging_perceiving": "string", // "judging" or "perceiving"
            "sensing_intuition": "string" // "sensing" or "intuition"
        }},
        "motivations": {{
            "convenience": "integer", // Score 0-100
            "wellness": "integer", // Score 0-100
            "speed": "integer", // Score 0-100
            "preferences": "integer", // Score 0-100
            "comfort": "integer", // Score 0-100
            "dietary_needs": "integer" // Score 0-100
        }},
        "behaviors_habits": ["string"], // List of observed behaviors and habits
        "goals_needs": ["string"], // List of inferred goals and needs
        "frustrations": ["string"], // List of inferred frustrations
        "common_topics": ["string"], // List of top 5-10 common topics
        "sentiment": "string", // Overall sentiment ("Positive", "Negative", "Neutral")
        "quote": "string", // A representative quote from their content
        "citations": [ // Up to 5 relevant citations (comments/posts)
            {{
                "id": "integer",
                "type": "string", // "comment" or "post"
                "content": "string", // Snippet of the content
                "permalink": "string", // Full permalink to the Reddit content
                "score": "integer" // Score of the comment/post
            }}
        ]
    }}

    Reddit Username: {username}

    User's Comments:
    {all_comments}

    User's Posts:
    {all_posts}

    Combined Text for Analysis:
    {combined_text}
    """

    try:
        response = model.generate_content(prompt)
        persona_json_str = response.text
        
        # Clean the response to ensure it's valid JSON
        # Sometimes the LLM might add markdown or extra text
        persona_json_str = persona_json_str.strip()
        if persona_json_str.startswith("```json"):
            persona_json_str = persona_json_str[len("```json"):].strip()
        if persona_json_str.endswith("```"):
            persona_json_str = persona_json_str[:-len("```")].strip()

        persona = json.loads(persona_json_str)

        # Ensure citations are properly formatted and limited
        citations = []
        citation_id = 1
        for comment in scraped_data['comments'][:5]: # Limit to 5 comments
            citations.append({
                "id": citation_id,
                "type": "comment",
                "content": comment['body'][:200], # Truncate content for brevity
                "permalink": f"https://www.reddit.com{comment['permalink']}",
                "score": comment['score']
            })
            citation_id += 1
        for post in scraped_data['posts'][:5]: # Limit to 5 posts
            citations.append({
                "id": citation_id,
                "type": "post",
                "content": (post['title'] + " " + post['selftext'])[:200], # Truncate content
                "permalink": f"https://www.reddit.com{post['permalink']}",
                "score": post['score']
            })
            citation_id += 1
        persona['citations'] = citations

        return persona
    except Exception as e:
        print(f"Error generating persona with LLM: {e}")
        # Fallback or raise an error
        raise Exception(f"Failed to generate persona using LLM: {e}")

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
    
    # You would need to provide a real API key here for testing
    try:
        persona = generate_enhanced_persona(dummy_scraped_data, "testuser", "YOUR_GOOGLE_API_KEY")
        print("Generated Enhanced Persona:")
        print(json.dumps(persona, indent=2))
    except Exception as e:
        print(f"Test failed: {e}")