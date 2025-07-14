"""
Demo credentials file for testing the Reddit Persona Generator.

IMPORTANT: Replace these with your actual Reddit API credentials.
To get credentials:
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Choose "script" as the app type
4. Copy the client ID and secret

For security, consider using environment variables in production.
"""

# Replace these with your actual Reddit API credentials
REDDIT_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
REDDIT_CLIENT_SECRET = "YOUR_CLIENT_SECRET_HERE"
REDDIT_USER_AGENT = "PersonaGenerator/2.0 by YourUsername"

# Replace with your Google AI Studio API Key
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"

# Example Reddit user URLs for testing
SAMPLE_URLS = [
    "https://www.reddit.com/user/kojied/",
    "https://www.reddit.com/user/Hungry-Move-6603/",
    # Add more sample URLs here
]