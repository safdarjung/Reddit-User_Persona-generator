import streamlit as st
import os
from datetime import datetime
from src.reddit_scraper import initialize_reddit, extract_username_from_url, scrape_redditor_data
from src.persona_generator import generate_persona

# Streamlit app configuration
st.set_page_config(
    page_title="Reddit User Persona Generator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def save_persona_to_file(persona, username):
    """Saves the generated persona to a text file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"persona_{username}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"Reddit User Persona Report\n")
        f.write(f"=" * 50 + "\n\n")
        f.write(f"Username: {username}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write(f"Name: {persona['name']}\n")
        f.write(f"Age Group: {persona['age_group']}\n")
        f.write(f"Sentiment: {persona['sentiment']}\n")
        f.write(f"Common Topics: {', '.join(persona['common_topics'])}\n\n")
        
        f.write("Citations:\n")
        f.write("-" * 20 + "\n")
        for citation in persona['citations']:
            f.write(f"[{citation['id']}] ({citation['type'].upper()}) {citation['content'][:100]}...\n")
            f.write(f"    Source: {citation['permalink']}\n\n")
    
    return filename

def main():
    st.title("🔍 Reddit User Persona Generator")
    st.markdown("Generate detailed user personas from Reddit profiles with citations.")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Reddit API credentials input
    st.sidebar.subheader("Reddit API Credentials")
    client_id = st.sidebar.text_input("Client ID", type="password", help="Your Reddit app client ID")
    client_secret = st.sidebar.text_input("Client Secret", type="password", help="Your Reddit app client secret")
    user_agent = st.sidebar.text_input("User Agent", value="PersonaGenerator/1.0", help="A unique identifier for your app")
    
    # Data scraping options
    st.sidebar.subheader("Scraping Options")
    limit = st.sidebar.slider("Number of posts/comments to analyze", min_value=10, max_value=500, value=100, step=10)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Enter Reddit User Profile URL")
        user_url = st.text_input(
            "Reddit Profile URL",
            placeholder="https://www.reddit.com/user/username/",
            help="Enter the full URL of the Reddit user profile you want to analyze"
        )
        
        if st.button("Generate Persona", type="primary"):
            if not all([client_id, client_secret, user_agent]):
                st.error("Please provide all Reddit API credentials in the sidebar.")
                return
            
            if not user_url:
                st.error("Please enter a Reddit user profile URL.")
                return
            
            username = extract_username_from_url(user_url)
            if not username:
                st.error("Invalid Reddit user URL. Please check the format.")
                return
            
            try:
                with st.spinner(f"Analyzing user: {username}..."):
                    # Initialize Reddit instance
                    reddit = initialize_reddit(client_id, client_secret, user_agent)
                    
                    # Scrape user data
                    st.info("Scraping user data...")
                    scraped_data = scrape_redditor_data(reddit, username, limit=limit)
                    
                    if not scraped_data['comments'] and not scraped_data['posts']:
                        st.warning("No data found for this user. They might have no posts/comments or their profile might be private.")
                        return
                    
                    # Generate persona
                    st.info("Generating persona...")
                    persona = generate_persona(scraped_data)
                    
                    # Display results
                    st.success("Persona generated successfully!")
                    
                    # Display persona details
                    st.header(f"User Persona: {username}")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.subheader("Basic Information")
                        st.write(f"**Name:** {persona['name']}")
                        st.write(f"**Age Group:** {persona['age_group']}")
                        st.write(f"**Sentiment:** {persona['sentiment']}")
                    
                    with col_b:
                        st.subheader("Activity Summary")
                        st.write(f"**Comments Analyzed:** {len(scraped_data['comments'])}")
                        st.write(f"**Posts Analyzed:** {len(scraped_data['posts'])}")
                    
                    st.subheader("Common Topics")
                    if persona['common_topics']:
                        topics_str = ", ".join(persona['common_topics'])
                        st.write(topics_str)
                    else:
                        st.write("No significant topics identified.")
                    
                    # Display citations
                    st.subheader("Citations")
                    if persona['citations']:
                        for citation in persona['citations']:
                            with st.expander(f"Citation [{citation['id']}] - {citation['type'].upper()}"):
                                st.write(f"**Content:** {citation['content'][:200]}...")
                                st.write(f"**Source:** [View on Reddit]({citation['permalink']})")
                    else:
                        st.write("No citations available.")
                    
                    # Save to file
                    filename = save_persona_to_file(persona, username)
                    st.success(f"Persona saved to file: {filename}")
                    
                    # Download button
                    with open(filename, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                    
                    st.download_button(
                        label="Download Persona Report",
                        data=file_content,
                        file_name=filename,
                        mime="text/plain"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your Reddit API credentials and try again.")
    
    with col2:
        st.header("Instructions")
        st.markdown("""
        ### How to use:
        1. **Get Reddit API credentials:**
           - Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
           - Create a new app (script type)
           - Copy the client ID and secret
        
        2. **Enter credentials** in the sidebar
        
        3. **Paste the Reddit user URL** in the format:
           `https://www.reddit.com/user/username/`
        
        4. **Click "Generate Persona"** to start analysis
        
        5. **Download the report** when complete
        
        ### Features:
        - ✅ Analyzes posts and comments
        - ✅ Identifies common topics
        - ✅ Sentiment analysis
        - ✅ Provides citations
        - ✅ Exports to text file
        """)

if __name__ == "__main__":
    main()

