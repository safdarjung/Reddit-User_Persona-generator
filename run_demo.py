#!/usr/bin/env python3
"""
Demo runner for the Reddit Persona Generator.
This script demonstrates the core functionality without the Streamlit interface.
"""

from src.reddit_scraper import initialize_reddit, extract_username_from_url, scrape_redditor_data
from src.enhanced_persona_generator import generate_enhanced_persona
from demo_credentials import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, SAMPLE_URLS

def run_demo():
    """Run a demonstration of the persona generation."""
    print("Reddit Persona Generator - Demo Mode")
    print("=" * 50)
    
    # Check if credentials are configured
    if REDDIT_CLIENT_ID == "YOUR_CLIENT_ID_HERE":
        print("❌ Please configure your Reddit API credentials in demo_credentials.py")
        print("Visit https://www.reddit.com/prefs/apps to get your credentials")
        return
    
    try:
        # Initialize Reddit instance
        print("🔧 Initializing Reddit API connection...")
        reddit = initialize_reddit(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT)
        print("✅ Reddit API connection established")
        
        # Use first sample URL or ask for input
        if SAMPLE_URLS and SAMPLE_URLS[0] != "https://www.reddit.com/user/kojied/":
            user_url = SAMPLE_URLS[0]
        else:
            user_url = input("\nEnter Reddit user URL (or press Enter for demo): ").strip()
            if not user_url:
                user_url = "https://www.reddit.com/user/spez/"  # Reddit CEO as demo
        
        print(f"\n🔍 Analyzing user: {user_url}")
        
        # Extract username
        username = extract_username_from_url(user_url)
        if not username:
            print("❌ Invalid Reddit user URL")
            return
        
        print(f"👤 Username: {username}")
        
        # Scrape user data
        print("📊 Scraping user data...")
        scraped_data = scrape_redditor_data(reddit, username, limit=50)  # Limit for demo
        
        if not scraped_data['comments'] and not scraped_data['posts']:
            print("❌ No data found for this user")
            return
        
        print(f"✅ Found {len(scraped_data['comments'])} comments and {len(scraped_data['posts'])} posts")
        
        # Generate persona
        print("🧠 Generating persona...")
        persona = generate_enhanced_persona(scraped_data, username)
        
        # Display results
        print("\n" + "=" * 60)
        print("GENERATED PERSONA")
        print("=" * 60)
        
        print(f"\n👤 NAME: {persona['name']}")
        print(f"🎂 AGE: {persona['age']}")
        print(f"💼 OCCUPATION: {persona['occupation']}")
        print(f"📍 LOCATION: {persona['location']}")
        print(f"🏷️ ARCHETYPE: {persona['archetype']}")
        
        print(f"\n🧠 PERSONALITY:")
        for trait, value in persona['personality'].items():
            print(f"   • {trait.replace('_', ' ').title()}: {value.title()}")
        
        print(f"\n🎯 TOP MOTIVATIONS:")
        sorted_motivations = sorted(persona['motivations'].items(), key=lambda x: x[1], reverse=True)
        for motivation, score in sorted_motivations[:3]:
            print(f"   • {motivation.replace('_', ' ').title()}: {score}/100")
        
        print(f"\n📝 BEHAVIORS & HABITS:")
        for behavior in persona['behaviors_habits'][:3]:
            print(f"   • {behavior}")
        
        print(f"\n🎯 GOALS & NEEDS:")
        for goal in persona['goals_needs'][:3]:
            print(f"   • {goal}")
        
        print(f"\n😤 FRUSTRATIONS:")
        for frustration in persona['frustrations'][:3]:
            print(f"   • {frustration}")
        
        print(f"\n🏷️ COMMON TOPICS:")
        print(f"   {', '.join(persona['common_topics'][:10])}")
        
        print(f"\n💭 SENTIMENT: {persona['sentiment']}")
        
        print(f"\n📚 CITATIONS: {len(persona['citations'])} sources available")
        
        print(f"\n💬 QUOTE: \"{persona['quote']}\"")
        
        print("\n" + "=" * 60)
        print("Demo completed successfully! 🎉")
        print("Run 'streamlit run enhanced_app.py' for the full interactive experience.")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print("Please check your Reddit API credentials and internet connection.")

if __name__ == "__main__":
    run_demo()

