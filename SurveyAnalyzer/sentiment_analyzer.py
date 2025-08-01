#!/usr/bin/env python3
"""
Sentiment Analyzer Module
Description: Performs basic sentiment analysis on text responses using
keyword matching and scoring systems without external libraries.
"""

import re
from typing import List, Dict, Any, Optional
from collections import Counter


class SentimentAnalyzer:
    """Handles sentiment analysis of text responses using keyword-based approach."""
    
    def __init__(self):
        """Initialize the sentiment analyzer with keyword dictionaries."""
        # Positive keywords and their weights
        self.positive_keywords = {
            'excellent': 3, 'amazing': 3, 'great': 2, 'good': 2, 'wonderful': 3,
            'fantastic': 3, 'outstanding': 3, 'perfect': 3, 'love': 2, 'like': 1,
            'enjoy': 2, 'happy': 2, 'satisfied': 2, 'pleased': 2, 'impressed': 2,
            'recommend': 2, 'helpful': 2, 'useful': 1, 'effective': 2, 'quality': 1,
            'best': 2, 'awesome': 3, 'brilliant': 3, 'superb': 3, 'terrific': 3,
            'delighted': 3, 'thrilled': 3, 'excited': 2, 'positive': 1, 'successful': 2,
            'improved': 1, 'better': 1, 'exceeded': 2, 'surpassed': 2, 'outstanding': 3
        }
        
        # Negative keywords and their weights
        self.negative_keywords = {
            'terrible': 3, 'awful': 3, 'horrible': 3, 'bad': 2, 'poor': 2,
            'disappointing': 2, 'frustrated': 2, 'angry': 2, 'upset': 2, 'annoyed': 2,
            'hate': 3, 'dislike': 2, 'worst': 3, 'useless': 2, 'waste': 2,
            'problem': 1, 'issue': 1, 'difficult': 1, 'confusing': 1, 'complicated': 1,
            'broken': 2, 'failed': 2, 'error': 1, 'bug': 1, 'crash': 2,
            'slow': 1, 'expensive': 1, 'overpriced': 2, 'cheap': 1, 'low quality': 2,
            'unreliable': 2, 'unstable': 2, 'inconsistent': 1, 'disorganized': 1,
            'messy': 1, 'chaotic': 2, 'stressful': 2, 'overwhelming': 2
        }
        
        # Neutral keywords (used for context)
        self.neutral_keywords = {
            'okay': 0, 'fine': 0, 'average': 0, 'normal': 0, 'standard': 0,
            'usual': 0, 'typical': 0, 'regular': 0, 'common': 0, 'basic': 0,
            'simple': 0, 'straightforward': 0, 'clear': 0, 'understandable': 0,
            'adequate': 0, 'sufficient': 0, 'acceptable': 0, 'reasonable': 0
        }
        
        # Negation words that can flip sentiment
        self.negation_words = {
            'not', 'no', 'never', 'none', 'neither', 'nor', 'nobody', 'nothing',
            'nowhere', 'hardly', 'barely', 'scarcely', 'doesn\'t', 'don\'t',
            'didn\'t', 'won\'t', 'can\'t', 'couldn\'t', 'wouldn\'t', 'shouldn\'t',
            'isn\'t', 'aren\'t', 'wasn\'t', 'weren\'t', 'hasn\'t', 'haven\'t',
            'hadn\'t', 'doesnt', 'dont', 'didnt', 'wont', 'cant', 'couldnt',
            'wouldnt', 'shouldnt', 'isnt', 'arent', 'wasnt', 'werent', 'hasnt',
            'havent', 'hadnt'
        }
        
        # Intensifier words that amplify sentiment
        self.intensifier_words = {
            'very': 1.5, 'really': 1.5, 'extremely': 2.0, 'absolutely': 2.0,
            'completely': 2.0, 'totally': 2.0, 'entirely': 2.0, 'thoroughly': 1.5,
            'highly': 1.5, 'incredibly': 2.0, 'amazingly': 2.0, 'exceptionally': 2.0,
            'particularly': 1.2, 'especially': 1.2, 'notably': 1.2, 'remarkably': 1.5
        }
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of a single text response.
        
        Args:
            text: Text string to analyze
            
        Returns:
            Dictionary containing sentiment analysis results
        """
        if not text or not isinstance(text, str):
            return {
                'sentiment': 'neutral',
                'score': 0,
                'positive_words': [],
                'negative_words': [],
                'confidence': 0.0
            }
        
        # Clean and normalize text
        cleaned_text = self._clean_text(text)
        
        # Extract words
        words = self._extract_words(cleaned_text)
        
        # Analyze sentiment
        sentiment_score = 0
        positive_words = []
        negative_words = []
        intensifier_count = 0
        
        for i, word in enumerate(words):
            word_lower = word.lower()
            
            # Check for intensifiers
            if word_lower in self.intensifier_words:
                intensifier_count += 1
                continue
            
            # Check for negations
            is_negated = self._is_negated(words, i)
            
            # Check positive keywords
            if word_lower in self.positive_keywords:
                weight = self.positive_keywords[word_lower]
                if is_negated:
                    sentiment_score -= weight
                    negative_words.append(word)
                else:
                    sentiment_score += weight
                    positive_words.append(word)
            
            # Check negative keywords
            elif word_lower in self.negative_keywords:
                weight = self.negative_keywords[word_lower]
                if is_negated:
                    sentiment_score += weight
                    positive_words.append(word)
                else:
                    sentiment_score -= weight
                    negative_words.append(word)
        
        # Apply intensifier multiplier
        if intensifier_count > 0:
            sentiment_score *= (1 + (intensifier_count * 0.2))
        
        # Determine sentiment category
        sentiment = self._categorize_sentiment(sentiment_score)
        
        # Calculate confidence
        total_words = len(words)
        sentiment_words = len(positive_words) + len(negative_words)
        confidence = min(1.0, sentiment_words / max(total_words, 1))
        
        return {
            'sentiment': sentiment,
            'score': sentiment_score,
            'positive_words': positive_words,
            'negative_words': negative_words,
            'confidence': confidence,
            'total_words': total_words,
            'sentiment_words': sentiment_words
        }
    
    def analyze_column(self, survey_data: List[Dict[str, Any]], column: str) -> Dict[str, Any]:
        """
        Analyze sentiment for all responses in a specific column.
        
        Args:
            survey_data: List of survey responses
            column: Column name to analyze
            
        Returns:
            Dictionary containing aggregated sentiment analysis results
        """
        if not survey_data or column not in survey_data[0]:
            return {
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'positive_pct': 0.0,
                'negative_pct': 0.0,
                'neutral_pct': 0.0,
                'avg_score': 0.0,
                'total_responses': 0
            }
        
        sentiment_results = []
        total_responses = 0
        
        for row in survey_data:
            text = row.get(column)
            if text is not None and str(text).strip():
                result = self.analyze_text(str(text))
                sentiment_results.append(result)
                total_responses += 1
        
        if not sentiment_results:
            return {
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'positive_pct': 0.0,
                'negative_pct': 0.0,
                'neutral_pct': 0.0,
                'avg_score': 0.0,
                'total_responses': 0
            }
        
        # Count sentiments
        positive_count = sum(1 for r in sentiment_results if r['sentiment'] == 'positive')
        negative_count = sum(1 for r in sentiment_results if r['sentiment'] == 'negative')
        neutral_count = sum(1 for r in sentiment_results if r['sentiment'] == 'neutral')
        
        # Calculate percentages
        total = len(sentiment_results)
        positive_pct = (positive_count / total) * 100
        negative_pct = (negative_count / total) * 100
        neutral_pct = (neutral_count / total) * 100
        
        # Calculate average score
        avg_score = sum(r['score'] for r in sentiment_results) / total
        
        return {
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'positive_pct': positive_pct,
            'negative_pct': negative_pct,
            'neutral_pct': neutral_pct,
            'avg_score': avg_score,
            'total_responses': total_responses,
            'detailed_results': sentiment_results
        }
    
    def analyze_all_text_columns(self, survey_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze sentiment for all text columns in the survey data.
        
        Args:
            survey_data: List of survey responses
            
        Returns:
            Dictionary containing sentiment analysis for all text columns
        """
        if not survey_data:
            return {}
        
        text_columns = []
        for col in survey_data[0].keys():
            # Check if column contains text data
            text_count = 0
            total_count = 0
            
            for row in survey_data[:10]:  # Sample first 10 rows
                value = row.get(col)
                if value is not None and str(value).strip():
                    total_count += 1
                    if len(str(value)) > 20:  # Consider it text if longer than 20 chars
                        text_count += 1
            
            if total_count > 0 and (text_count / total_count) > 0.3:
                text_columns.append(col)
        
        results = {}
        for column in text_columns:
            results[column] = self.analyze_column(survey_data, column)
        
        return results
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for analysis."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove punctuation (keep apostrophes for contractions)
        text = re.sub(r'[^\w\s\']', ' ', text)
        
        return text.strip()
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text."""
        return text.split()
    
    def _is_negated(self, words: List[str], current_index: int) -> bool:
        """Check if current word is negated by previous words."""
        # Look back up to 3 words for negation
        start_index = max(0, current_index - 3)
        
        for i in range(start_index, current_index):
            if i < len(words) and words[i].lower() in self.negation_words:
                return True
        
        return False
    
    def _categorize_sentiment(self, score: float) -> str:
        """Categorize sentiment based on score."""
        if score > 1.0:
            return 'positive'
        elif score < -1.0:
            return 'negative'
        else:
            return 'neutral'
    
    def get_sentiment_summary(self, sentiment_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of sentiment analysis results."""
        if not sentiment_results:
            return {}
        
        total_responses = len(sentiment_results)
        positive_count = sum(1 for r in sentiment_results if r['sentiment'] == 'positive')
        negative_count = sum(1 for r in sentiment_results if r['sentiment'] == 'negative')
        neutral_count = sum(1 for r in sentiment_results if r['sentiment'] == 'neutral')
        
        # Most common positive and negative words
        all_positive_words = []
        all_negative_words = []
        
        for result in sentiment_results:
            all_positive_words.extend(result['positive_words'])
            all_negative_words.extend(result['negative_words'])
        
        positive_word_counts = Counter(all_positive_words)
        negative_word_counts = Counter(all_negative_words)
        
        return {
            'total_responses': total_responses,
            'sentiment_distribution': {
                'positive': {'count': positive_count, 'percentage': (positive_count / total_responses) * 100},
                'negative': {'count': negative_count, 'percentage': (negative_count / total_responses) * 100},
                'neutral': {'count': neutral_count, 'percentage': (neutral_count / total_responses) * 100}
            },
            'top_positive_words': positive_word_counts.most_common(5),
            'top_negative_words': negative_word_counts.most_common(5),
            'average_confidence': sum(r['confidence'] for r in sentiment_results) / total_responses,
            'average_score': sum(r['score'] for r in sentiment_results) / total_responses
        }
    
    def export_sentiment_report(self, sentiment_results: Dict[str, Any], filename: str = "sentiment_report.txt") -> bool:
        """Export sentiment analysis results to a text file."""
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write("SENTIMENT ANALYSIS REPORT\n")
                file.write("=" * 50 + "\n\n")
                
                for column, results in sentiment_results.items():
                    file.write(f"Column: {column}\n")
                    file.write("-" * 30 + "\n")
                    file.write(f"Total Responses: {results['total_responses']}\n")
                    file.write(f"Positive: {results['positive']} ({results['positive_pct']:.1f}%)\n")
                    file.write(f"Negative: {results['negative']} ({results['negative_pct']:.1f}%)\n")
                    file.write(f"Neutral: {results['neutral']} ({results['neutral_pct']:.1f}%)\n")
                    file.write(f"Average Score: {results['avg_score']:.2f}\n\n")
                
            return True
            
        except Exception as e:
            print(f"Error exporting sentiment report: {str(e)}")
            return False 