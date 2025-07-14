import streamlit as st
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from src.reddit_scraper import initialize_reddit, extract_username_from_url, scrape_redditor_data
from src.enhanced_persona_generator import generate_enhanced_persona

# Streamlit app configuration
st.set_page_config(
    page_title="Reddit User Persona Generator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Darker background for persona card */
    .persona-card {
        background-color: #2c2f33;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #d9822b; /* softer muted orange */
        color: #ddd; /* lighter text */
    }
    /* Softer header color */
    .persona-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #d9822b; /* muted orange */
        margin-bottom: 20px;
    }
    /* Section headers with lighter gray */
    .section-header {
        font-size: 1.2em;
        font-weight: bold;
        color: #bbb;
        margin-top: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    /* Personality trait tags with subtle background and text */
    .personality-trait {
        background-color: #444c56;
        color: #ccc;
        padding: 5px 10px;
        margin: 2px;
        border-radius: 15px;
        display: inline-block;
        font-size: 0.9em;
    }
    /* Quote box with softer background and text */
    .quote-box {
        background-color: #d9822b;
        color: #222;
        padding: 20px;
        border-radius: 10px;
        font-style: italic;
        font-size: 1.1em;
        text-align: center;
        margin: 20px 0;
    }
    /* Metric box with dark background and subtle border */
    .metric-box {
        background-color: #222;
        color: #ccc;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #444c56;
        text-align: center;
        margin: 5px;
    }
</style>
""", unsafe_allow_html=True)

def create_motivation_chart(motivations):
    """Create a horizontal bar chart for motivations."""
    labels = list(motivations.keys())
    values = list(motivations.values())
    
    # Create color scale
    colors = ['#ff6b35', '#f7931e', '#ffd23f', '#06d6a0', '#118ab2', '#073b4c']
    
    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker_color=colors[:len(labels)],
        text=values,
        textposition='inside',
        textfont=dict(color='white', size=12)
    ))
    
    fig.update_layout(
        title="Motivations",
        xaxis_title="Strength",
        yaxis_title="",
        height=300,
        margin=dict(l=100, r=50, t=50, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(range=[0, 100], showgrid=True, gridcolor='lightgray')
    fig.update_yaxes(showgrid=False)
    
    return fig

def create_personality_chart(personality):
    """Create personality trait visualization."""
    traits = []
    positions = []
    
    # Map personality traits to positions (0-100 scale)
    trait_mapping = {
        'extrovert': ('Extrovert', 'Introvert', 75 if personality['extrovert_introvert'] == 'extrovert' else 25),
        'thinking': ('Thinking', 'Feeling', 75 if personality['thinking_feeling'] == 'thinking' else 25),
        'judging': ('Judging', 'Perceiving', 75 if personality['judging_perceiving'] == 'judging' else 25),
        'sensing': ('Sensing', 'Intuition', 75 if personality['sensing_intuition'] == 'sensing' else 25)
    }
    
    labels = []
    values = []
    
    for key, (trait1, trait2, value) in trait_mapping.items():
        labels.append(f"{trait1} ← → {trait2}")
        values.append(value)
    
    fig = go.Figure()
    
    for i, (label, value) in enumerate(zip(labels, values)):
        fig.add_trace(go.Scatter(
            x=[0, 100],
            y=[i, i],
            mode='lines',
            line=dict(color='lightgray', width=8),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=[value],
            y=[i],
            mode='markers',
            marker=dict(color='#ff6b35', size=15),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        title="Personality",
        xaxis=dict(range=[-5, 105], showgrid=False, showticklabels=False),
        yaxis=dict(tickmode='array', tickvals=list(range(len(labels))), ticktext=labels),
        height=250,
        margin=dict(l=150, r=50, t=50, b=50),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def save_enhanced_persona_to_file(persona, username):
    """Saves the enhanced persona to a formatted text file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enhanced_persona_{username}_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(f"REDDIT USER PERSONA REPORT\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"USERNAME: {persona['name']}\n")
        f.write(f"GENERATED ON: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Basic Information
        f.write("BASIC INFORMATION\n")
        f.write("-" * 40 + "\n")
        f.write(f"Age: {persona['age']}\n")
        f.write(f"Occupation: {persona['occupation']}\n")
        f.write(f"Status: {persona['status']}\n")
        f.write(f"Location: {persona['location']}\n")
        f.write(f"Tier: {persona['tier']}\n")
        f.write(f"Archetype: {persona['archetype']}\n\n")
        
        # Personality
        f.write("PERSONALITY\n")
        f.write("-" * 40 + "\n")
        for trait, value in persona['personality'].items():
            f.write(f"{trait.replace('_', ' ').title()}: {value.title()}\n")
        f.write("\n")
        
        # Motivations
        f.write("MOTIVATIONS\n")
        f.write("-" * 40 + "\n")
        for motivation, score in persona['motivations'].items():
            f.write(f"{motivation.replace('_', ' ').title()}: {score}/100\n")
        f.write("\n")
        
        # Behavior & Habits
        f.write("BEHAVIOR & HABITS\n")
        f.write("-" * 40 + "\n")
        for behavior in persona['behaviors_habits']:
            f.write(f"• {behavior}\n")
        f.write("\n")
        
        # Goals & Needs
        f.write("GOALS & NEEDS\n")
        f.write("-" * 40 + "\n")
        for goal in persona['goals_needs']:
            f.write(f"• {goal}\n")
        f.write("\n")
        
        # Frustrations
        f.write("FRUSTRATIONS\n")
        f.write("-" * 40 + "\n")
        for frustration in persona['frustrations']:
            f.write(f"• {frustration}\n")
        f.write("\n")
        
        # Common Topics
        f.write("COMMON TOPICS\n")
        f.write("-" * 40 + "\n")
        f.write(f"{', '.join(persona['common_topics'])}\n\n")
        
        # Quote
        f.write("REPRESENTATIVE QUOTE\n")
        f.write("-" * 40 + "\n")
        f.write(f'"{persona["quote"]}"\n\n')
        
        # Citations
        f.write("CITATIONS & SOURCES\n")
        f.write("-" * 40 + "\n")
        for citation in persona['citations']:
            f.write(f"[{citation['id']}] ({citation['type'].upper()}) Score: {citation['score']}\n")
            f.write(f"Content: {citation['content'][:150]}...\n")
            f.write(f"Source: {citation['permalink']}\n\n")
    
    return filename

def main():
    st.title("🔍 Reddit User Persona Generator")
    st.markdown("Generate comprehensive user personas from Reddit profiles with professional formatting and visualizations.")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Reddit API credentials input
    st.sidebar.subheader("Reddit API Credentials")
    client_id = st.sidebar.text_input("Client ID", type="password", help="Enter your Reddit app client ID (found in your Reddit app settings).")
    client_secret = st.sidebar.text_input("Client Secret", type="password", help="Enter your Reddit app client secret (found in your Reddit app settings).")
    user_agent = st.sidebar.text_input("User Agent", value="PersonaGenerator/2.0", help="A unique identifier for your app, e.g., 'MyApp/1.0'.")
    
    # Data scraping options
    st.sidebar.subheader("Scraping Options")
    limit = st.sidebar.slider("Number of posts/comments to analyze", min_value=10, max_value=500, value=100, step=10, help="Select how many posts and comments to analyze for persona generation.")
    
    # Main content area
    st.header("Enter Reddit User Profile URL")
    user_url = st.text_input(
        "Reddit Profile URL",
        placeholder="https://www.reddit.com/user/username/",
        help="Enter the full URL of the Reddit user profile you want to analyze, e.g., https://www.reddit.com/user/kojied/"
    )
    
    if st.button("Generate Enhanced Persona", type="primary"):
        if not all([client_id, client_secret, user_agent]):
            st.error("Please provide all required Reddit API credentials in the sidebar to proceed.")
            return
        
        if not user_url:
            st.error("Please enter a valid Reddit user profile URL to proceed.")
            return
        
        username = extract_username_from_url(user_url)
        if not username:
            st.error("Invalid Reddit user URL format detected. Please ensure the URL matches 'https://www.reddit.com/user/username/'.")
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
                
                # Generate enhanced persona
                st.info("Generating enhanced persona...")
                persona = generate_enhanced_persona(scraped_data, username)
                
                # Display results in professional format
                st.success("Enhanced persona generated successfully!")
                
                # Main persona display
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col2:
                    st.markdown(f'<div class="persona-header">{persona["name"]}</div>', unsafe_allow_html=True)
                
                # Basic information section
                col_left, col_right = st.columns([1, 2])
                
                with col_left:
                    st.markdown('<div class="persona-card">', unsafe_allow_html=True)
                    st.markdown("**BASIC INFORMATION**")
                    st.write(f"**Age:** {persona['age']}")
                    st.write(f"**Occupation:** {persona['occupation']}")
                    st.write(f"**Status:** {persona['status']}")
                    st.write(f"**Location:** {persona['location']}")
                    st.write(f"**Tier:** {persona['tier']}")
                    st.write(f"**Archetype:** {persona['archetype']}")
                    
                    # Personality traits as tags
                    st.markdown("**PERSONALITY TRAITS**")
                    traits_html = ""
                    for trait, value in persona['personality'].items():
                        traits_html += f'<span class="personality-trait">{value.title()}</span> '
                    st.markdown(traits_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_right:
                    # Behavior & Habits
                    st.markdown('<div class="section-header">BEHAVIOUR & HABITS</div>', unsafe_allow_html=True)
                    for behavior in persona['behaviors_habits']:
                        st.write(f"• {behavior}")
                    
                    # Goals & Needs
                    st.markdown('<div class="section-header">GOALS & NEEDS</div>', unsafe_allow_html=True)
                    for goal in persona['goals_needs']:
                        st.write(f"• {goal}")
                    
                    # Frustrations
                    st.markdown('<div class="section-header">FRUSTRATIONS</div>', unsafe_allow_html=True)
                    for frustration in persona['frustrations']:
                        st.write(f"• {frustration}")
                
                # Visualizations
                col_viz1, col_viz2 = st.columns(2)
                
                with col_viz1:
                    # Motivations chart
                    if persona['motivations']:
                        fig_motivations = create_motivation_chart(persona['motivations'])
                        st.plotly_chart(fig_motivations, use_container_width=True)
                        # Add download button for motivation chart
                        img_bytes = fig_motivations.to_image(format="png")
                        st.download_button(
                            label="📥 Download Motivation Chart as PNG",
                            data=img_bytes,
                            file_name="motivation_chart.png",
                            mime="image/png"
                        )
                
                with col_viz2:
                    # Personality chart
                    fig_personality = create_personality_chart(persona['personality'])
                    st.plotly_chart(fig_personality, use_container_width=True)
                    # Add download button for personality chart
                    img_bytes_personality = fig_personality.to_image(format="png")
                    st.download_button(
                        label="📥 Download Personality Chart as PNG",
                        data=img_bytes_personality,
                        file_name="personality_chart.png",
                        mime="image/png"
                    )
                
                # Quote section
                if persona.get('quote'):
                    st.markdown(f'<div class="quote-box">"{persona["quote"]}"</div>', unsafe_allow_html=True)
                
                # Activity metrics
                st.markdown("### Activity Summary")
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                with col_m1:
                    st.metric("Comments Analyzed", len(scraped_data['comments']))
                with col_m2:
                    st.metric("Posts Analyzed", len(scraped_data['posts']))
                with col_m3:
                    st.metric("Common Topics", len(persona['common_topics']))
                with col_m4:
                    st.metric("Overall Sentiment", persona['sentiment'])
                
                # Citations section
                with st.expander("📚 View Citations & Sources"):
                    st.markdown("### Citations")
                    for citation in persona['citations']:
                        with st.container():
                            st.write(f"**[{citation['id']}] {citation['type'].upper()}** (Score: {citation['score']})")
                            st.write(f"Content: {citation['content'][:200]}...")
                            st.write(f"[View on Reddit]({citation['permalink']})")
                            st.divider()
                
                # Save to file
                filename = save_enhanced_persona_to_file(persona, username)
                st.success(f"Enhanced persona saved to file: {filename}")
                
                # Download button
                with open(filename, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                st.download_button(
                    label="📄 Download Enhanced Persona Report",
                    data=file_content,
                    file_name=filename,
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please check your Reddit API credentials and try again.")
    
    # Instructions section
    with st.expander("📖 How to Use This Application"):
        st.markdown("""
        ### Getting Started:
        
        1. **Obtain Reddit API Credentials:**
           - Visit [Reddit Apps](https://www.reddit.com/prefs/apps)
           - Click "Create App" or "Create Another App"
           - Choose "script" as the app type
           - Copy the client ID (under the app name) and secret
        
        2. **Configure the Application:**
           - Enter your credentials in the sidebar
           - Adjust the number of posts/comments to analyze
        
        3. **Generate Persona:**
           - Paste a Reddit user URL (format: `https://www.reddit.com/user/username/`)
           - Click "Generate Enhanced Persona"
           - Wait for analysis to complete
        
        4. **Review Results:**
           - View the comprehensive persona with visualizations
           - Check citations and sources
           - Download the detailed report
        
        ### Features:
        - ✅ Professional persona layout
        - ✅ Personality trait analysis
        - ✅ Motivation scoring with charts
        - ✅ Behavioral pattern identification
        - ✅ Goals and frustrations extraction
        - ✅ Interactive visualizations
        - ✅ Comprehensive citations
        - ✅ Downloadable reports
        
        ### Sample Output Includes:
        - Basic demographic information
        - MBTI-style personality traits
        - Motivation levels (Convenience, Wellness, Speed, etc.)
        - Behavioral patterns and habits
        - Goals and needs identification
        - Frustration points
        - Representative quotes
        - Source citations with links
        """)

if __name__ == "__main__":
    main()

