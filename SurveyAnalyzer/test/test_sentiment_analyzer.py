#!/usr/bin/env python3
"""
Unit Tests for Sentiment Analyzer Module
Author: Student Developer
Description: Comprehensive unit tests for sentiment analysis functionality.
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sentiment_analyzer import SentimentAnalyzer


class TestSentimentAnalyzer(unittest.TestCase):
    """Test cases for the SentimentAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sentiment_analyzer = SentimentAnalyzer()
        self.test_data = [
            {'feedback': 'This is excellent! I love it.', 'satisfaction': 'Very Satisfied'},
            {'feedback': 'Terrible experience, very bad service.', 'satisfaction': 'Dissatisfied'},
            {'feedback': 'It was okay, nothing special.', 'satisfaction': 'Neutral'},
            {'feedback': 'Great product and amazing support!', 'satisfaction': 'Very Satisfied'},
            {'feedback': 'Poor quality and bad service.', 'satisfaction': 'Dissatisfied'}
        ]
    
    def test_initialization(self):
        """Test SentimentAnalyzer initialization."""
        self.assertIsInstance(self.sentiment_analyzer.positive_keywords, dict)
        self.assertIsInstance(self.sentiment_analyzer.negative_keywords, dict)
        self.assertIsInstance(self.sentiment_analyzer.neutral_keywords, dict)
        self.assertIsInstance(self.sentiment_analyzer.negation_words, set)
        self.assertIsInstance(self.sentiment_analyzer.intensifier_words, dict)
        
        # Check that keywords are loaded
        self.assertGreater(len(self.sentiment_analyzer.positive_keywords), 0)
        self.assertGreater(len(self.sentiment_analyzer.negative_keywords), 0)
    
    def test_analyze_text_positive(self):
        """Test sentiment analysis with positive text."""
        text = "This is excellent! I love the product."
        result = self.sentiment_analyzer.analyze_text(text)
        
        self.assertIsInstance(result, dict)
        self.assertIn('sentiment', result)
        self.assertIn('score', result)
        self.assertIn('positive_words', result)
        self.assertIn('negative_words', result)
        self.assertIn('confidence', result)
        
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['score'], 0)
        self.assertGreater(len(result['positive_words']), 0)
    
    def test_analyze_text_negative(self):
        """Test sentiment analysis with negative text."""
        text = "This is terrible! I hate the service."
        result = self.sentiment_analyzer.analyze_text(text)
        
        self.assertEqual(result['sentiment'], 'negative')
        self.assertLess(result['score'], 0)
        self.assertGreater(len(result['negative_words']), 0)
    
    def test_analyze_text_neutral(self):
        """Test sentiment analysis with neutral text."""
        text = "It was okay, nothing special."
        result = self.sentiment_analyzer.analyze_text(text)
        
        self.assertEqual(result['sentiment'], 'neutral')
        self.assertAlmostEqual(result['score'], 0, places=1)
    
    def test_analyze_text_with_negation(self):
        """Test sentiment analysis with negation."""
        text = "This is not good at all."
        result = self.sentiment_analyzer.analyze_text(text)
        
        # Should be negative due to negation
        self.assertEqual(result['sentiment'], 'negative')
        self.assertLess(result['score'], 0)
    
    def test_analyze_text_with_intensifier(self):
        """Test sentiment analysis with intensifier."""
        text = "This is very excellent!"
        result = self.sentiment_analyzer.analyze_text(text)
        
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['score'], 0)
    
    def test_analyze_text_empty(self):
        """Test sentiment analysis with empty text."""
        result = self.sentiment_analyzer.analyze_text("")
        
        self.assertEqual(result['sentiment'], 'neutral')
        self.assertEqual(result['score'], 0)
        self.assertEqual(len(result['positive_words']), 0)
        self.assertEqual(len(result['negative_words']), 0)
    
    def test_analyze_text_none(self):
        """Test sentiment analysis with None text."""
        result = self.sentiment_analyzer.analyze_text(None)
        
        self.assertEqual(result['sentiment'], 'neutral')
        self.assertEqual(result['score'], 0)
    
    def test_analyze_column(self):
        """Test sentiment analysis for a column."""
        result = self.sentiment_analyzer.analyze_column(self.test_data, 'feedback')
        
        self.assertIsInstance(result, dict)
        self.assertIn('positive', result)
        self.assertIn('negative', result)
        self.assertIn('neutral', result)
        self.assertIn('positive_pct', result)
        self.assertIn('negative_pct', result)
        self.assertIn('neutral_pct', result)
        self.assertIn('avg_score', result)
        self.assertIn('total_responses', result)
        
        # Check that percentages sum to approximately 100
        total_pct = result['positive_pct'] + result['negative_pct'] + result['neutral_pct']
        self.assertAlmostEqual(total_pct, 100.0, places=1)
    
    def test_analyze_column_empty_data(self):
        """Test sentiment analysis with empty data."""
        result = self.sentiment_analyzer.analyze_column([], 'feedback')
        
        self.assertEqual(result['positive'], 0)
        self.assertEqual(result['negative'], 0)
        self.assertEqual(result['neutral'], 0)
        self.assertEqual(result['total_responses'], 0)
    
    def test_analyze_column_missing_column(self):
        """Test sentiment analysis with missing column."""
        result = self.sentiment_analyzer.analyze_column(self.test_data, 'nonexistent_column')
        
        self.assertEqual(result['positive'], 0)
        self.assertEqual(result['negative'], 0)
        self.assertEqual(result['neutral'], 0)
        self.assertEqual(result['total_responses'], 0)
    
    def test_analyze_all_text_columns(self):
        """Test sentiment analysis for all text columns."""
        result = self.sentiment_analyzer.analyze_all_text_columns(self.test_data)
        
        self.assertIsInstance(result, dict)
        self.assertIn('feedback', result)
        
        feedback_result = result['feedback']
        self.assertIn('positive', feedback_result)
        self.assertIn('negative', feedback_result)
        self.assertIn('neutral', feedback_result)
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        dirty_text = "  This   is   a   TEST!!!   "
        cleaned = self.sentiment_analyzer._clean_text(dirty_text)
        
        self.assertEqual(cleaned, "this is a test")
    
    def test_extract_words(self):
        """Test word extraction."""
        text = "This is a test sentence."
        words = self.sentiment_analyzer._extract_words(text)
        
        self.assertIsInstance(words, list)
        self.assertEqual(len(words), 5)
        self.assertIn('This', words)
        self.assertIn('is', words)
        self.assertIn('a', words)
        self.assertIn('test', words)
        self.assertIn('sentence.', words)
    
    def test_is_negated(self):
        """Test negation detection."""
        words = ['This', 'is', 'not', 'good']
        
        # Check if 'good' is negated
        is_negated = self.sentiment_analyzer._is_negated(words, 3)  # Index of 'good'
        self.assertTrue(is_negated)
        
        # Check if 'This' is negated (should not be)
        is_negated = self.sentiment_analyzer._is_negated(words, 0)  # Index of 'This'
        self.assertFalse(is_negated)
    
    def test_categorize_sentiment(self):
        """Test sentiment categorization."""
        # Test positive sentiment
        sentiment = self.sentiment_analyzer._categorize_sentiment(2.0)
        self.assertEqual(sentiment, 'positive')
        
        # Test negative sentiment
        sentiment = self.sentiment_analyzer._categorize_sentiment(-2.0)
        self.assertEqual(sentiment, 'negative')
        
        # Test neutral sentiment
        sentiment = self.sentiment_analyzer._categorize_sentiment(0.5)
        self.assertEqual(sentiment, 'neutral')
        
        sentiment = self.sentiment_analyzer._categorize_sentiment(-0.5)
        self.assertEqual(sentiment, 'neutral')
    
    def test_get_sentiment_summary(self):
        """Test sentiment summary generation."""
        # Create sentiment results
        sentiment_results = [
            {'sentiment': 'positive', 'score': 2.0, 'positive_words': ['excellent'], 'negative_words': [], 'confidence': 0.8},
            {'sentiment': 'negative', 'score': -1.5, 'positive_words': [], 'negative_words': ['terrible'], 'confidence': 0.7},
            {'sentiment': 'neutral', 'score': 0.0, 'positive_words': [], 'negative_words': [], 'confidence': 0.5}
        ]
        
        summary = self.sentiment_analyzer.get_sentiment_summary(sentiment_results)
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_responses', summary)
        self.assertIn('sentiment_distribution', summary)
        self.assertIn('top_positive_words', summary)
        self.assertIn('top_negative_words', summary)
        self.assertIn('average_confidence', summary)
        self.assertIn('average_score', summary)
        
        self.assertEqual(summary['total_responses'], 3)
        self.assertEqual(summary['sentiment_distribution']['positive']['count'], 1)
        self.assertEqual(summary['sentiment_distribution']['negative']['count'], 1)
        self.assertEqual(summary['sentiment_distribution']['neutral']['count'], 1)
    
    def test_export_sentiment_report(self):
        """Test sentiment report export."""
        sentiment_results = {
            'feedback': {
                'positive': 2,
                'negative': 2,
                'neutral': 1,
                'positive_pct': 40.0,
                'negative_pct': 40.0,
                'neutral_pct': 20.0,
                'avg_score': 0.2,
                'total_responses': 5
            }
        }
        
        # Test successful export
        result = self.sentiment_analyzer.export_sentiment_report(sentiment_results, "test_sentiment_report.txt")
        self.assertTrue(result)
        
        # Clean up
        import os
        if os.path.exists("test_sentiment_report.txt"):
            os.remove("test_sentiment_report.txt")
    
    def test_analyze_text_complex_sentence(self):
        """Test sentiment analysis with complex sentence."""
        text = "This product is absolutely fantastic and I would highly recommend it to everyone!"
        result = self.sentiment_analyzer.analyze_text(text)
        
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['score'], 0)
        self.assertGreater(len(result['positive_words']), 0)
    
    def test_analyze_text_mixed_sentiment(self):
        """Test sentiment analysis with mixed sentiment."""
        text = "The product is good but the service is terrible."
        result = self.sentiment_analyzer.analyze_text(text)
        
        # Should have both positive and negative words
        self.assertGreater(len(result['positive_words']), 0)
        self.assertGreater(len(result['negative_words']), 0)
    
    def test_analyze_text_no_sentiment_words(self):
        """Test sentiment analysis with no sentiment words."""
        text = "The product arrived on time and was delivered to the correct address."
        result = self.sentiment_analyzer.analyze_text(text)
        
        self.assertEqual(result['sentiment'], 'neutral')
        self.assertEqual(len(result['positive_words']), 0)
        self.assertEqual(len(result['negative_words']), 0)


if __name__ == '__main__':
    unittest.main() 