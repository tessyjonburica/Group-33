#!/usr/bin/env python3
"""
Unit Tests for Statistical Analyzer Module
Author: Student Developer
Description: Comprehensive unit tests for statistical analysis functionality.
"""

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from stats_analyzer import StatsAnalyzer


class TestStatsAnalyzer(unittest.TestCase):
    """Test cases for the StatsAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = [
            {'age': '25', 'gender': 'Male', 'region': 'North', 'satisfaction': 'High'},
            {'age': '30', 'gender': 'Female', 'region': 'South', 'satisfaction': 'Medium'},
            {'age': '35', 'gender': 'Male', 'region': 'East', 'satisfaction': 'Low'},
            {'age': '28', 'gender': 'Female', 'region': 'North', 'satisfaction': 'High'},
            {'age': '42', 'gender': 'Male', 'region': 'South', 'satisfaction': 'Medium'},
            {'age': '33', 'gender': 'Female', 'region': 'East', 'satisfaction': 'Low'}
        ]
        self.stats_analyzer = StatsAnalyzer(self.test_data)
    
    def test_initialization(self):
        """Test StatsAnalyzer initialization."""
        self.assertEqual(self.stats_analyzer.total_responses, 6)
        self.assertEqual(len(self.stats_analyzer.columns), 4)
        self.assertIn('age', self.stats_analyzer.columns)
        self.assertIn('gender', self.stats_analyzer.columns)
        self.assertIn('region', self.stats_analyzer.columns)
        self.assertIn('satisfaction', self.stats_analyzer.columns)
    
    def test_cross_tabulate_valid_columns(self):
        """Test cross-tabulation with valid columns."""
        crosstab = self.stats_analyzer.cross_tabulate('gender', 'satisfaction')
        
        self.assertIsInstance(crosstab, list)
        self.assertGreater(len(crosstab), 1)  # Should have header + data rows
        
        # Check header row
        header = crosstab[0]
        self.assertIn('', header)  # First column should be empty (row labels)
        
        # Check data rows
        for row in crosstab[1:]:
            self.assertIsInstance(row, list)
            self.assertEqual(len(row), len(header))
    
    def test_cross_tabulate_invalid_columns(self):
        """Test cross-tabulation with invalid columns."""
        with self.assertRaises(ValueError):
            self.stats_analyzer.cross_tabulate('invalid_column', 'gender')
    
    def test_chi_square_test_valid_data(self):
        """Test chi-square test with valid data."""
        result = self.stats_analyzer.chi_square_test('gender', 'satisfaction')
        
        self.assertIsInstance(result, dict)
        self.assertIn('chi_square', result)
        self.assertIn('p_value', result)
        self.assertIn('df', result)
        self.assertIn('significant', result)
        
        # Check data types
        self.assertIsInstance(result['chi_square'], float)
        self.assertIsInstance(result['p_value'], float)
        self.assertIsInstance(result['df'], int)
        self.assertIsInstance(result['significant'], bool)
    
    def test_chi_square_test_insufficient_data(self):
        """Test chi-square test with insufficient data."""
        # Create data with only one value per category
        limited_data = [
            {'gender': 'Male', 'satisfaction': 'High'},
            {'gender': 'Female', 'satisfaction': 'Low'}
        ]
        limited_analyzer = StatsAnalyzer(limited_data)
        
        result = limited_analyzer.chi_square_test('gender', 'satisfaction')
        
        self.assertIn('error', result)
        self.assertEqual(result['chi_square'], 0.0)
        self.assertEqual(result['p_value'], 1.0)
    
    def test_correlation_analysis_numeric_data(self):
        """Test correlation analysis with numeric data."""
        numeric_data = [
            {'age': '25', 'satisfaction_score': '8'},
            {'age': '30', 'satisfaction_score': '7'},
            {'age': '35', 'satisfaction_score': '6'},
            {'age': '28', 'satisfaction_score': '9'},
            {'age': '42', 'satisfaction_score': '5'}
        ]
        numeric_analyzer = StatsAnalyzer(numeric_data)
        
        result = numeric_analyzer.correlation_analysis('age', 'satisfaction_score')
        
        self.assertIsInstance(result, dict)
        self.assertIn('correlation', result)
        self.assertIn('sample_size', result)
        self.assertIn('strength', result)
        
        self.assertIsInstance(result['correlation'], float)
        self.assertIsInstance(result['sample_size'], int)
        self.assertIsInstance(result['strength'], str)
    
    def test_correlation_analysis_insufficient_data(self):
        """Test correlation analysis with insufficient data."""
        insufficient_data = [
            {'age': '25', 'score': '8'}
        ]
        insufficient_analyzer = StatsAnalyzer(insufficient_data)
        
        result = insufficient_analyzer.correlation_analysis('age', 'score')
        
        self.assertIn('error', result)
        self.assertEqual(result['correlation'], 0.0)
        self.assertEqual(result['sample_size'], 0)
    
    def test_calculate_correlation(self):
        """Test correlation calculation."""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]  # Perfect positive correlation
        
        correlation = self.stats_analyzer._calculate_correlation(x, y)
        self.assertAlmostEqual(correlation, 1.0, places=5)
    
    def test_calculate_correlation_negative(self):
        """Test negative correlation calculation."""
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]  # Perfect negative correlation
        
        correlation = self.stats_analyzer._calculate_correlation(x, y)
        self.assertAlmostEqual(correlation, -1.0, places=5)
    
    def test_calculate_correlation_no_correlation(self):
        """Test correlation calculation with no correlation."""
        x = [1, 2, 3, 4, 5]
        y = [1, 1, 1, 1, 1]  # No variation in y
        
        correlation = self.stats_analyzer._calculate_correlation(x, y)
        self.assertEqual(correlation, 0.0)
    
    def test_interpret_correlation(self):
        """Test correlation interpretation."""
        # Test very strong positive correlation
        strength = self.stats_analyzer._interpret_correlation(0.9)
        self.assertEqual(strength, "Very Strong")
        
        # Test strong positive correlation
        strength = self.stats_analyzer._interpret_correlation(0.7)
        self.assertEqual(strength, "Strong")
        
        # Test moderate correlation
        strength = self.stats_analyzer._interpret_correlation(0.5)
        self.assertEqual(strength, "Moderate")
        
        # Test weak correlation
        strength = self.stats_analyzer._interpret_correlation(0.3)
        self.assertEqual(strength, "Weak")
        
        # Test very weak correlation
        strength = self.stats_analyzer._interpret_correlation(0.1)
        self.assertEqual(strength, "Very Weak")
    
    def test_analyze_response_patterns(self):
        """Test response pattern analysis."""
        patterns = self.stats_analyzer.analyze_response_patterns()
        
        self.assertIsInstance(patterns, dict)
        self.assertIn('common_combinations', patterns)
        self.assertIn('response_clusters', patterns)
        self.assertIn('outliers', patterns)
        
        self.assertIsInstance(patterns['common_combinations'], list)
        self.assertIsInstance(patterns['response_clusters'], list)
        self.assertIsInstance(patterns['outliers'], list)
    
    def test_get_statistical_summary(self):
        """Test statistical summary generation."""
        summary = self.stats_analyzer.get_statistical_summary()
        
        self.assertIsInstance(summary, dict)
        self.assertIn('total_responses', summary)
        self.assertIn('total_columns', summary)
        self.assertIn('numeric_columns', summary)
        self.assertIn('categorical_columns', summary)
        self.assertIn('statistical_tests', summary)
        
        self.assertEqual(summary['total_responses'], 6)
        self.assertEqual(summary['total_columns'], 4)
        self.assertIsInstance(summary['numeric_columns'], list)
        self.assertIsInstance(summary['categorical_columns'], list)
    
    def test_perform_multiple_chi_square_tests(self):
        """Test multiple chi-square tests."""
        results = self.stats_analyzer.perform_multiple_chi_square_tests('gender')
        
        self.assertIsInstance(results, list)
        
        for result in results:
            self.assertIn('column1', result)
            self.assertIn('column2', result)
            self.assertEqual(result['column1'], 'gender')
            self.assertNotEqual(result['column2'], 'gender')
    
    def test_calculate_expected_frequencies(self):
        """Test expected frequency calculation."""
        observed = [[2, 1], [1, 2]]  # 2x2 contingency table
        
        expected = self.stats_analyzer._calculate_expected_frequencies(observed)
        
        self.assertIsInstance(expected, list)
        self.assertEqual(len(expected), 2)
        self.assertEqual(len(expected[0]), 2)
        
        # Check that expected frequencies sum to total
        total_observed = sum(sum(row) for row in observed)
        total_expected = sum(sum(row) for row in expected)
        self.assertAlmostEqual(total_expected, total_observed, places=5)
    
    def test_chi_square_p_value(self):
        """Test chi-square p-value calculation."""
        # Test with small chi-square value
        p_value = self.stats_analyzer._chi_square_p_value(1.0, 2)
        self.assertGreater(p_value, 0.0)
        self.assertLessEqual(p_value, 1.0)
        
        # Test with large chi-square value
        p_value = self.stats_analyzer._chi_square_p_value(10.0, 2)
        self.assertGreaterEqual(p_value, 0.0)
        self.assertLess(p_value, 1.0)
        
        # Test with zero degrees of freedom
        p_value = self.stats_analyzer._chi_square_p_value(5.0, 0)
        self.assertEqual(p_value, 1.0)


if __name__ == '__main__':
    unittest.main() 