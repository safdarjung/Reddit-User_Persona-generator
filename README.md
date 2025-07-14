# Reddit User Persona Generator

A comprehensive Streamlit application that generates professional user personas from Reddit profiles, complete with behavioral analysis, personality traits, motivations, and visual representations.

## 🌟 Features

- **Professional Persona Layout**: Generates personas in a format similar to professional UX research documents
- **Comprehensive Analysis**: Analyzes posts, comments, and user behavior patterns
- **Visual Representations**: Interactive charts for motivations and personality traits
- **MBTI-Style Personality Analysis**: Extracts personality dimensions (Introvert/Extrovert, Thinking/Feeling, etc.)
- **Behavioral Pattern Recognition**: Identifies habits, goals, needs, and frustrations
- **Citation System**: Provides source links for all persona characteristics
- **Export Functionality**: Download detailed reports as text files
- **Responsive Design**: Professional UI with custom styling

## 📋 Requirements

- Python 3.7+
- Reddit API credentials (Client ID, Client Secret)
- Internet connection for Reddit API access

## 🚀 Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd reddit_persona_generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Reddit API credentials:**
   - Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Choose "script" as the app type
   - Note down the client ID (under the app name) and secret

## 🎯 Usage

### Basic Application
Run the basic version:
```bash
streamlit run app.py
```

### Enhanced Application (Recommended)
Run the enhanced version with professional formatting:
```bash
streamlit run enhanced_app.py
```

### Using the Application

1. **Enter Reddit API Credentials** in the sidebar:
   - Client ID
   - Client Secret
   - User Agent (default provided)

2. **Configure Analysis Options:**
   - Set the number of posts/comments to analyze (10-500)

3. **Enter Reddit User URL:**
   - Format: `https://www.reddit.com/user/username/`
   - Examples:
     - `https://www.reddit.com/user/kojied/`
     - `https://www.reddit.com/user/Hungry-Move-6603/`

4. **Generate Persona:**
   - Click "Generate Enhanced Persona"
   - Wait for analysis to complete
   - Review the comprehensive persona report

5. **Download Report:**
   - Use the download button to save the detailed report
   - File includes all analysis with citations

## 📊 Persona Output Format

The generated persona includes:

### Basic Information
- **Name**: Reddit username
- **Age**: Estimated age group
- **Occupation**: Inferred from content (when possible)
- **Status**: Relationship status (when identifiable)
- **Location**: Geographic location hints
- **Tier**: User activity level
- **Archetype**: User type classification

### Personality Analysis
- **MBTI-Style Traits**: Introvert/Extrovert, Thinking/Feeling, Judging/Perceiving, Sensing/Intuition
- **Visual Representation**: Interactive personality chart

### Motivations (Scored 0-100)
- Convenience
- Wellness
- Speed
- Preferences
- Comfort
- Dietary Needs

### Behavioral Patterns
- Technology usage patterns
- Social engagement levels
- Content creation vs. consumption habits
- Activity timing and frequency

### Goals & Needs
- Learning objectives
- Health and wellness goals
- Career aspirations
- Relationship goals
- Financial objectives

### Frustrations
- Common pain points
- Negative sentiment analysis
- Problem areas identified from content

### Citations
- Source posts and comments
- Reddit links for verification
- Score and engagement metrics

## 🏗️ Project Structure

```
reddit_persona_generator/
├── src/
│   ├── reddit_scraper.py          # Reddit data scraping module
│   ├── persona_generator.py       # Basic persona generation
│   └── enhanced_persona_generator.py  # Advanced persona generation
├── app.py                         # Basic Streamlit application
├── enhanced_app.py               # Enhanced Streamlit application
├── test_app.py                   # Unit tests
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── todo.md                       # Development checklist
```

## 🧪 Testing

Run the unit tests:
```bash
python -m unittest test_app.py -v
```

Tests cover:
- URL parsing functionality
- Reddit data scraping (mocked)
- Persona generation logic
- Text analysis functions

## 🔧 Configuration Options

### Reddit API Settings
- **Client ID**: Your Reddit app client ID
- **Client Secret**: Your Reddit app client secret
- **User Agent**: Identifier for your application

### Analysis Parameters
- **Limit**: Number of posts/comments to analyze (10-500)
- **Depth**: How far back to look in user history

### Output Customization
- **File Format**: Text file with structured sections
- **Citation Style**: Reddit permalink format
- **Visual Charts**: Plotly interactive charts

## 🎨 Customization

### Styling
The enhanced app includes custom CSS for professional appearance:
- Color scheme matching UX research standards
- Responsive layout for different screen sizes
- Interactive elements with hover effects

### Analysis Algorithms
You can customize the analysis by modifying:
- `enhanced_persona_generator.py`: Core analysis logic
- Personality trait indicators
- Motivation scoring algorithms
- Behavioral pattern recognition

## 🚨 Limitations

- **Privacy**: Only analyzes public Reddit content
- **Accuracy**: Persona generation is based on available data and may not be 100% accurate
- **Rate Limits**: Reddit API has rate limiting; large analyses may take time
- **Content Availability**: Some users may have limited public content

## 🔒 Privacy & Ethics

- Only accesses publicly available Reddit data
- No personal information is stored permanently
- Generated personas are for research/analysis purposes
- Respects Reddit's API terms of service
- Users should obtain consent before analyzing others' profiles

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid Reddit user URL"**
   - Ensure URL format: `https://www.reddit.com/user/username/`
   - Check that the username exists

2. **"No data found for this user"**
   - User may have no public posts/comments
   - Profile might be private or suspended

3. **API Authentication Errors**
   - Verify Reddit API credentials
   - Check that the app is configured as "script" type
   - Ensure user agent is unique

4. **NLTK Download Errors**
   - The app automatically downloads required NLTK data
   - Ensure internet connection for first run

### Performance Tips

- Start with smaller limits (50-100) for faster results
- Larger limits (200-500) provide more comprehensive analysis
- Consider user activity level when setting limits

## 📈 Future Enhancements

- **Image Analysis**: Profile picture and posted image analysis
- **Temporal Analysis**: Activity patterns over time
- **Subreddit Analysis**: Community engagement patterns
- **Sentiment Trends**: Mood changes over time
- **Comparison Features**: Compare multiple users
- **Export Formats**: PDF, JSON, CSV export options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please respect Reddit's API terms of service and user privacy.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Reddit API documentation
3. Ensure all dependencies are installed correctly
4. Verify Python version compatibility (3.7+)

---

**Note**: This tool is designed for legitimate research and analysis purposes. Always respect user privacy and obtain appropriate consent when analyzing others' social media profiles.

