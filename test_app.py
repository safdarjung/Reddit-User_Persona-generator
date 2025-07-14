import unittest
from unittest.mock import Mock, patch
from src.reddit_scraper import extract_username_from_url, scrape_redditor_data
from src.persona_generator import generate_persona, analyze_text_for_keywords

class TestRedditScraper(unittest.TestCase):
    
    def test_extract_username_from_url(self):
        """Test username extraction from various URL formats."""
        test_cases = [
            ("https://www.reddit.com/user/kojied/", "kojied"),
            ("https://www.reddit.com/user/Hungry-Move-6603/", "Hungry-Move-6603"),
            ("https://reddit.com/user/testuser", "testuser"),
            ("invalid_url", None),
            ("https://www.reddit.com/r/python/", None)
        ]
        
        for url, expected in test_cases:
            with self.subTest(url=url):
                result = extract_username_from_url(url)
                self.assertEqual(result, expected)
    
    @patch('src.reddit_scraper.praw.Reddit')
    def test_scrape_redditor_data(self, mock_reddit):
        """Test scraping redditor data with mocked PRAW."""
        # Mock Reddit instance and redditor
        mock_reddit_instance = Mock()
        mock_redditor = Mock()
        mock_reddit_instance.redditor.return_value = mock_redditor
        
        # Mock comments
        mock_comment = Mock()
        mock_comment.id = "comment1"
        mock_comment.body = "This is a test comment"
        mock_comment.score = 5
        mock_comment.created_utc = 1678886400
        mock_comment.permalink = "/r/test/comments/comment1"
        mock_redditor.comments.new.return_value = [mock_comment]
        
        # Mock submissions
        mock_submission = Mock()
        mock_submission.id = "post1"
        mock_submission.title = "Test Post"
        mock_submission.selftext = "This is a test post"
        mock_submission.score = 10
        mock_submission.created_utc = 1678886400
        mock_submission.permalink = "/r/test/comments/post1"
        mock_submission.url = "https://www.reddit.com/r/test/comments/post1"
        mock_redditor.submissions.new.return_value = [mock_submission]
        
        # Test the function
        result = scrape_redditor_data(mock_reddit_instance, "testuser", limit=1)
        
        # Assertions
        self.assertEqual(len(result['comments']), 1)
        self.assertEqual(len(result['posts']), 1)
        self.assertEqual(result['comments'][0]['body'], "This is a test comment")
        self.assertEqual(result['posts'][0]['title'], "Test Post")

class TestPersonaGenerator(unittest.TestCase):
    
    def test_analyze_text_for_keywords(self):
        """Test keyword analysis function."""
        text = "I love programming and coding in Python. Python is great for data science."
        keywords = analyze_text_for_keywords(text)
        
        # Check that common words are filtered out and Python appears twice
        self.assertIn("python", keywords)
        self.assertIn("programming", keywords)
        self.assertEqual(keywords["python"], 2)
        self.assertNotIn("and", keywords)  # Stop word should be filtered
    
    def test_generate_persona(self):
        """Test persona generation with sample data."""
        sample_data = {
            'comments': [
                {
                    'id': 'c1',
                    'body': 'I love playing video games, especially RPGs.',
                    'score': 10,
                    'created_utc': 1678886400,
                    'permalink': '/r/gaming/comments/c1'
                }
            ],
            'posts': [
                {
                    'id': 'p1',
                    'title': 'My favorite RPGs',
                    'selftext': 'I enjoy games like The Witcher.',
                    'score': 20,
                    'created_utc': 1678886400,
                    'permalink': '/r/rpg/comments/p1',
                    'url': 'https://www.reddit.com/r/rpg/comments/p1'
                }
            ]
        }
        
        persona = generate_persona(sample_data)
        
        # Basic assertions
        self.assertIn('name', persona)
        self.assertIn('sentiment', persona)
        self.assertIn('common_topics', persona)
        self.assertIn('citations', persona)
        self.assertIsInstance(persona['common_topics'], list)
        self.assertIsInstance(persona['citations'], list)

if __name__ == '__main__':
    unittest.main()

