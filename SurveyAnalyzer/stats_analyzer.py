#!/usr/bin/env python3
"""
Statistical Analyzer Module
Author: Student Developer
Description: Performs statistical analysis including cross-tabulation,
chi-square tests, and correlation analysis on survey data.
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict, Counter
import itertools


class StatsAnalyzer:
    """Handles statistical analysis of survey data including cross-tabulation and chi-square tests."""
    
    def __init__(self, survey_data: List[Dict[str, Any]]):
        """
        Initialize the statistical analyzer.
        
        Args:
            survey_data: List of dictionaries containing survey responses
        """
        self.survey_data = survey_data
        self.total_responses = len(survey_data)
        self.columns = list(survey_data[0].keys()) if survey_data else []
        
    def cross_tabulate(self, col1: str, col2: str) -> List[List]:
        """
        Perform cross-tabulation between two columns.
        
        Args:
            col1: First column name
            col2: Second column name
            
        Returns:
            Cross-tabulation matrix as a list of lists
        """
        if col1 not in self.columns or col2 not in self.columns:
            raise ValueError(f"Column not found: {col1} or {col2}")
        
        # Get unique values for each column
        values1 = set()
        values2 = set()
        
        for row in self.survey_data:
            val1 = row.get(col1)
            val2 = row.get(col2)
            
            if val1 is not None and str(val1).strip():
                values1.add(str(val1).strip())
            if val2 is not None and str(val2).strip():
                values2.add(str(val2).strip())
        
        # Sort values for consistent ordering
        values1 = sorted(list(values1))
        values2 = sorted(list(values2))
        
        # Create cross-tabulation matrix
        crosstab = []
        
        # Header row
        header = [''] + values2
        crosstab.append(header)
        
        # Data rows
        for val1 in values1:
            row = [val1]
            for val2 in values2:
                count = 0
                for survey_row in self.survey_data:
                    if (str(survey_row.get(col1, '')).strip() == val1 and 
                        str(survey_row.get(col2, '')).strip() == val2):
                        count += 1
                row.append(count)
            crosstab.append(row)
        
        return crosstab
    
    def chi_square_test(self, col1: str, col2: str) -> Dict[str, Any]:
        """
        Perform chi-square test of independence between two categorical variables.
        
        Args:
            col1: First column name
            col2: Second column name
            
        Returns:
            Dictionary containing chi-square test results
        """
        # Get cross-tabulation
        crosstab = self.cross_tabulate(col1, col2)
        
        if len(crosstab) < 2 or len(crosstab[0]) < 2:
            return {
                'chi_square': 0.0,
                'p_value': 1.0,
                'df': 0,
                'significant': False,
                'error': 'Insufficient data for chi-square test'
            }
        
        # Extract observed frequencies (skip header row and column)
        observed = []
        for i in range(1, len(crosstab)):
            row = []
            for j in range(1, len(crosstab[i])):
                row.append(int(crosstab[i][j]))
            observed.append(row)
        
        # Check if we have enough data for chi-square test
        total_observations = sum(sum(row) for row in observed)
        if total_observations < 5:  # Chi-square test requires at least 5 observations
            return {
                'chi_square': 0.0,
                'p_value': 1.0,
                'df': 0,
                'significant': False,
                'error': 'Insufficient data for chi-square test'
            }
        
        # Calculate expected frequencies
        expected = self._calculate_expected_frequencies(observed)
        
        # Calculate chi-square statistic
        chi_square = 0.0
        for i in range(len(observed)):
            for j in range(len(observed[i])):
                if expected[i][j] > 0:
                    chi_square += ((observed[i][j] - expected[i][j]) ** 2) / expected[i][j]
        
        # Calculate degrees of freedom
        df = (len(observed) - 1) * (len(observed[0]) - 1)
        
        # Calculate p-value (approximation using chi-square distribution)
        p_value = self._chi_square_p_value(chi_square, df)
        
        # Determine significance (alpha = 0.05)
        significant = p_value < 0.05
        
        return {
            'chi_square': chi_square,
            'p_value': p_value,
            'df': df,
            'significant': significant,
            'observed': observed,
            'expected': expected
        }
    
    def _calculate_expected_frequencies(self, observed: List[List[int]]) -> List[List[float]]:
        """Calculate expected frequencies for chi-square test."""
        if not observed or not observed[0]:
            return []
        
        rows = len(observed)
        cols = len(observed[0])
        
        # Calculate row and column totals
        row_totals = [sum(row) for row in observed]
        col_totals = []
        for j in range(cols):
            col_totals.append(sum(observed[i][j] for i in range(rows)))
        
        total = sum(row_totals)
        
        # Calculate expected frequencies
        expected = []
        for i in range(rows):
            row = []
            for j in range(cols):
                expected_freq = (row_totals[i] * col_totals[j]) / total if total > 0 else 0
                row.append(expected_freq)
            expected.append(row)
        
        return expected
    
    def _chi_square_p_value(self, chi_square: float, df: int) -> float:
        """
        Calculate approximate p-value for chi-square statistic.
        This is a simplified approximation - in practice, you'd use a proper chi-square distribution.
        """
        if df <= 0:
            return 1.0
        
        # Simple approximation for chi-square p-value
        # For small chi-square values, p-value is close to 1
        # For large chi-square values, p-value approaches 0
        if chi_square < df:
            return 1.0 - (chi_square / (df * 2))
        else:
            return max(0.0, 1.0 - (chi_square / (df * 10)))
    
    def correlation_analysis(self, col1: str, col2: str) -> Dict[str, Any]:
        """
        Perform correlation analysis between two variables.
        
        Args:
            col1: First column name
            col2: Second column name
            
        Returns:
            Dictionary containing correlation analysis results
        """
        # Extract numeric values
        values1 = []
        values2 = []
        
        for row in self.survey_data:
            val1 = row.get(col1)
            val2 = row.get(col2)
            
            # Try to convert to numeric
            try:
                if val1 is not None and str(val1).strip():
                    num1 = float(val1)
                    if val2 is not None and str(val2).strip():
                        num2 = float(val2)
                        values1.append(num1)
                        values2.append(num2)
            except (ValueError, TypeError):
                continue
        
        if len(values1) < 2:
            return {
                'correlation': 0.0,
                'sample_size': 0,
                'error': 'Insufficient numeric data for correlation analysis'
            }
        
        # Calculate correlation coefficient
        correlation = self._calculate_correlation(values1, values2)
        
        return {
            'correlation': correlation,
            'sample_size': len(values1),
            'strength': self._interpret_correlation(correlation)
        }
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        
        # Calculate means
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        # Calculate correlation coefficient
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n))
        denominator_y = sum((y[i] - mean_y) ** 2 for i in range(n))
        
        if denominator_x == 0 or denominator_y == 0:
            return 0.0
        
        correlation = numerator / math.sqrt(denominator_x * denominator_y)
        return correlation
    
    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation coefficient strength."""
        abs_corr = abs(correlation)
        
        if abs_corr >= 0.8:
            return "Very Strong"
        elif abs_corr >= 0.6:
            return "Strong"
        elif abs_corr >= 0.4:
            return "Moderate"
        elif abs_corr >= 0.2:
            return "Weak"
        else:
            return "Very Weak"
    
    def analyze_response_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in survey responses."""
        patterns = {
            'common_combinations': [],
            'response_clusters': [],
            'outliers': []
        }
        
        # Find common combinations of responses
        response_combinations = []
        for row in self.survey_data:
            combination = []
            for col in self.columns:
                value = row.get(col)
                if value is not None and str(value).strip():
                    combination.append(f"{col}:{str(value).strip()}")
            if combination:
                response_combinations.append(tuple(sorted(combination)))
        
        # Count combinations
        combination_counts = Counter(response_combinations)
        common_combinations = combination_counts.most_common(5)
        
        patterns['common_combinations'] = [
            {
                'combination': list(combo),
                'count': count,
                'percentage': (count / len(response_combinations)) * 100
            }
            for combo, count in common_combinations
        ]
        
        return patterns
    
    def get_statistical_summary(self) -> Dict[str, Any]:
        """Generate a comprehensive statistical summary."""
        summary = {
            'total_responses': self.total_responses,
            'total_columns': len(self.columns),
            'numeric_columns': [],
            'categorical_columns': [],
            'statistical_tests': []
        }
        
        # Categorize columns
        for column in self.columns:
            numeric_count = 0
            total_count = 0
            
            for row in self.survey_data:
                value = row.get(column)
                if value is not None and str(value).strip():
                    total_count += 1
                    try:
                        float(str(value))
                        numeric_count += 1
                    except (ValueError, TypeError):
                        pass
            
            if total_count > 0 and (numeric_count / total_count) > 0.5:
                summary['numeric_columns'].append(column)
            else:
                summary['categorical_columns'].append(column)
        
        return summary
    
    def perform_multiple_chi_square_tests(self, target_column: str) -> List[Dict[str, Any]]:
        """
        Perform chi-square tests between a target column and all other categorical columns.
        
        Args:
            target_column: The target column to test against
            
        Returns:
            List of chi-square test results
        """
        results = []
        
        for column in self.columns:
            if column != target_column:
                try:
                    test_result = self.chi_square_test(target_column, column)
                    test_result['column1'] = target_column
                    test_result['column2'] = column
                    results.append(test_result)
                except Exception as e:
                    results.append({
                        'column1': target_column,
                        'column2': column,
                        'error': str(e)
                    })
        
        # Sort by significance
        results.sort(key=lambda x: x.get('p_value', 1.0))
        
        return results 