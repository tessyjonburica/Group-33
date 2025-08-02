#!/usr/bin/env python3
"""
Pattern Detector Module
Description: Identifies correlations, patterns, and trends in survey responses
using statistical analysis and pattern recognition techniques.
"""

import math
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict, Counter
import itertools


class PatternDetector:
    """Handles pattern detection and correlation analysis in survey data."""
    
    def __init__(self, survey_data: List[Dict[str, Any]]):
        """
        Initialize the pattern detector.
        
        Args:
            survey_data: List of dictionaries containing survey responses
        """
        self.survey_data = survey_data
        self.total_responses = len(survey_data)
        self.columns = list(survey_data[0].keys()) if survey_data else []
        
    def find_patterns(self) -> List[Dict[str, Any]]:
        """
        Find patterns and correlations in survey responses.
        
        Returns:
            List of detected patterns with descriptions and confidence levels
        """
        if not self.survey_data:
            return []
        
        patterns = []
        
        # Find demographic patterns
        patterns.extend(self._find_demographic_patterns())
        
        # Find response correlation patterns
        patterns.extend(self._find_correlation_patterns())
        
        # Find response combination patterns
        patterns.extend(self._find_combination_patterns())
        
        # Find outlier patterns
        patterns.extend(self._find_outlier_patterns())
        
        # Sort patterns by confidence
        patterns.sort(key=lambda x: x['confidence'], reverse=True)
        
        return patterns
    
    def _find_demographic_patterns(self) -> List[Dict[str, Any]]:
        """Find patterns related to demographics."""
        patterns = []
        
        # Age-based patterns
        if 'age' in self.columns:
            age_patterns = self._analyze_age_patterns()
            patterns.extend(age_patterns)
        
        # Gender-based patterns
        if 'gender' in self.columns:
            gender_patterns = self._analyze_gender_patterns()
            patterns.extend(gender_patterns)
        
        # Regional patterns
        if 'region' in self.columns:
            regional_patterns = self._analyze_regional_patterns()
            patterns.extend(regional_patterns)
        
        # Education-based patterns
        if 'education' in self.columns:
            education_patterns = self._analyze_education_patterns()
            patterns.extend(education_patterns)
        
        return patterns
    
    def _analyze_age_patterns(self) -> List[Dict[str, Any]]:
        """Analyze patterns based on age groups."""
        patterns = []
        
        # Group responses by age
        age_groups = {
            '18-25': [],
            '26-35': [],
            '36-45': [],
            '46-55': [],
            '56-65': [],
            '65+': []
        }
        
        for row in self.survey_data:
            age_str = row.get('age')
            if age_str and str(age_str).isdigit():
                try:
                    age = int(age_str)
                    if 18 <= age <= 25:
                        age_groups['18-25'].append(row)
                    elif 26 <= age <= 35:
                        age_groups['26-35'].append(row)
                    elif 36 <= age <= 45:
                        age_groups['36-45'].append(row)
                    elif 46 <= age <= 55:
                        age_groups['46-55'].append(row)
                    elif 56 <= age <= 65:
                        age_groups['56-65'].append(row)
                    elif age > 65:
                        age_groups['65+'].append(row)
                except ValueError:
                    continue
        
        # Analyze patterns for each question
        for column in self.columns:
            if column not in ['age', 'gender', 'region', 'education']:
                column_patterns = self._analyze_column_by_age_groups(column, age_groups)
                patterns.extend(column_patterns)
        
        return patterns
    
    def _analyze_column_by_age_groups(self, column: str, age_groups: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Analyze a specific column's responses by age groups."""
        patterns = []
        
        # Get most common response for each age group
        age_group_responses = {}
        for age_group, responses in age_groups.items():
            if responses:
                values = [r.get(column) for r in responses if r.get(column)]
                if values:
                    value_counts = Counter(values)
                    most_common = value_counts.most_common(1)[0]
                    age_group_responses[age_group] = {
                        'response': most_common[0],
                        'count': most_common[1],
                        'percentage': (most_common[1] / len(values)) * 100
                    }
        
        # Find patterns
        if len(age_group_responses) > 1:
            # Find age groups with similar responses
            response_groups = defaultdict(list)
            for age_group, data in age_group_responses.items():
                response_groups[data['response']].append(age_group)
            
            for response, age_groups_list in response_groups.items():
                if len(age_groups_list) > 1:
                    confidence = min(90, len(age_groups_list) * 20)
                    patterns.append({
                        'type': 'age_pattern',
                        'description': f"Age groups {', '.join(age_groups_list)} most commonly responded '{response}' to {column}",
                        'confidence': confidence,
                        'sample_size': sum(len(age_groups[ag]) for ag in age_groups_list),
                        'response': response,
                        'affected_groups': age_groups_list
                    })
        
        return patterns
    
    def _analyze_gender_patterns(self) -> List[Dict[str, Any]]:
        """Analyze patterns based on gender."""
        patterns = []
        
        # Group responses by gender
        gender_groups = defaultdict(list)
        for row in self.survey_data:
            gender = row.get('gender')
            if gender and str(gender).strip():
                gender_groups[str(gender).strip().title()].append(row)
        
        # Analyze patterns for each question
        for column in self.columns:
            if column not in ['age', 'gender', 'region', 'education']:
                column_patterns = self._analyze_column_by_gender(column, gender_groups)
                patterns.extend(column_patterns)
        
        return patterns
    
    def _analyze_column_by_gender(self, column: str, gender_groups: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Analyze a specific column's responses by gender."""
        patterns = []
        
        # Get most common response for each gender
        gender_responses = {}
        for gender, responses in gender_groups.items():
            if responses:
                values = [r.get(column) for r in responses if r.get(column)]
                if values:
                    value_counts = Counter(values)
                    most_common = value_counts.most_common(1)[0]
                    gender_responses[gender] = {
                        'response': most_common[0],
                        'count': most_common[1],
                        'percentage': (most_common[1] / len(values)) * 100
                    }
        
        # Find gender differences
        if len(gender_responses) > 1:
            responses = list(gender_responses.values())
            if len(set(r['response'] for r in responses)) > 1:
                # Different genders have different most common responses
                confidence = 75
                patterns.append({
                    'type': 'gender_pattern',
                    'description': f"Gender differences detected in {column} responses",
                    'confidence': confidence,
                    'sample_size': sum(len(gender_groups[g]) for g in gender_responses.keys()),
                    'details': gender_responses
                })
        
        return patterns
    
    def _analyze_regional_patterns(self) -> List[Dict[str, Any]]:
        """Analyze patterns based on region."""
        patterns = []
        
        # Group responses by region
        regional_groups = defaultdict(list)
        for row in self.survey_data:
            region = row.get('region')
            if region and str(region).strip():
                regional_groups[str(region).strip().title()].append(row)
        
        # Analyze patterns for each question
        for column in self.columns:
            if column not in ['age', 'gender', 'region', 'education']:
                column_patterns = self._analyze_column_by_region(column, regional_groups)
                patterns.extend(column_patterns)
        
        return patterns
    
    def _analyze_column_by_region(self, column: str, regional_groups: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Analyze a specific column's responses by region."""
        patterns = []
        
        # Get most common response for each region
        regional_responses = {}
        for region, responses in regional_groups.items():
            if responses:
                values = [r.get(column) for r in responses if r.get(column)]
                if values:
                    value_counts = Counter(values)
                    most_common = value_counts.most_common(1)[0]
                    regional_responses[region] = {
                        'response': most_common[0],
                        'count': most_common[1],
                        'percentage': (most_common[1] / len(values)) * 100
                    }
        
        # Find regional patterns
        if len(regional_responses) > 1:
            # Find regions with similar responses
            response_groups = defaultdict(list)
            for region, data in regional_responses.items():
                response_groups[data['response']].append(region)
            
            for response, regions_list in response_groups.items():
                if len(regions_list) > 1:
                    confidence = min(85, len(regions_list) * 25)
                    patterns.append({
                        'type': 'regional_pattern',
                        'description': f"Regions {', '.join(regions_list)} most commonly responded '{response}' to {column}",
                        'confidence': confidence,
                        'sample_size': sum(len(regional_groups[r]) for r in regions_list),
                        'response': response,
                        'affected_regions': regions_list
                    })
        
        return patterns
    
    def _analyze_education_patterns(self) -> List[Dict[str, Any]]:
        """Analyze patterns based on education level."""
        patterns = []
        
        # Group responses by education
        education_groups = defaultdict(list)
        for row in self.survey_data:
            education = row.get('education')
            if education and str(education).strip():
                education_groups[str(education).strip().title()].append(row)
        
        # Analyze patterns for each question
        for column in self.columns:
            if column not in ['age', 'gender', 'region', 'education']:
                column_patterns = self._analyze_column_by_education(column, education_groups)
                patterns.extend(column_patterns)
        
        return patterns
    
    def _analyze_column_by_education(self, column: str, education_groups: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Analyze a specific column's responses by education level."""
        patterns = []
        
        # Get most common response for each education level
        education_responses = {}
        for education, responses in education_groups.items():
            if responses:
                values = [r.get(column) for r in responses if r.get(column)]
                if values:
                    value_counts = Counter(values)
                    most_common = value_counts.most_common(1)[0]
                    education_responses[education] = {
                        'response': most_common[0],
                        'count': most_common[1],
                        'percentage': (most_common[1] / len(values)) * 100
                    }
        
        # Find education-based patterns
        if len(education_responses) > 1:
            # Find education levels with similar responses
            response_groups = defaultdict(list)
            for education, data in education_responses.items():
                response_groups[data['response']].append(education)
            
            for response, education_levels in response_groups.items():
                if len(education_levels) > 1:
                    confidence = min(80, len(education_levels) * 20)
                    patterns.append({
                        'type': 'education_pattern',
                        'description': f"Education levels {', '.join(education_levels)} most commonly responded '{response}' to {column}",
                        'confidence': confidence,
                        'sample_size': sum(len(education_groups[e]) for e in education_levels),
                        'response': response,
                        'affected_education_levels': education_levels
                    })
        
        return patterns
    
    def _find_correlation_patterns(self) -> List[Dict[str, Any]]:
        """Find correlation patterns between different questions."""
        patterns = []
        
        # Analyze correlations between categorical variables
        categorical_columns = [col for col in self.columns if col not in ['age', 'gender', 'region', 'education']]
        
        for i, col1 in enumerate(categorical_columns):
            for col2 in categorical_columns[i+1:]:
                correlation_pattern = self._analyze_correlation(col1, col2)
                if correlation_pattern:
                    patterns.append(correlation_pattern)
        
        return patterns
    
    def _analyze_correlation(self, col1: str, col2: str) -> Optional[Dict[str, Any]]:
        """Analyze correlation between two columns."""
        # Get unique values for both columns
        values1 = set()
        values2 = set()
        
        for row in self.survey_data:
            val1 = row.get(col1)
            val2 = row.get(col2)
            
            if val1 is not None and str(val1).strip():
                values1.add(str(val1).strip())
            if val2 is not None and str(val2).strip():
                values2.add(str(val2).strip())
        
        if len(values1) < 2 or len(values2) < 2:
            return None
        
        # Calculate correlation strength
        total_responses = 0
        matching_responses = 0
        
        for row in self.survey_data:
            val1 = row.get(col1)
            val2 = row.get(col2)
            
            if val1 is not None and str(val1).strip() and val2 is not None and str(val2).strip():
                total_responses += 1
                # Check if responses are related (simplified correlation)
                if self._are_responses_related(str(val1).strip(), str(val2).strip()):
                    matching_responses += 1
        
        if total_responses == 0:
            return None
        
        correlation_strength = matching_responses / total_responses
        
        if correlation_strength > 0.6:  # Strong correlation threshold
            return {
                'type': 'correlation_pattern',
                'description': f"Strong correlation detected between {col1} and {col2}",
                'confidence': min(90, correlation_strength * 100),
                'sample_size': total_responses,
                'correlation_strength': correlation_strength,
                'columns': [col1, col2]
            }
        
        return None
    
    def _are_responses_related(self, response1: str, response2: str) -> bool:
        """Check if two responses are related (simplified logic)."""
        # This is a simplified correlation check
        # In a real implementation, you might use more sophisticated methods
        
        # Check for similar sentiment
        positive_words = ['good', 'great', 'excellent', 'satisfied', 'happy', 'like', 'love']
        negative_words = ['bad', 'poor', 'terrible', 'dissatisfied', 'unhappy', 'dislike', 'hate']
        
        response1_lower = response1.lower()
        response2_lower = response2.lower()
        
        # Check if both responses have similar sentiment
        response1_positive = any(word in response1_lower for word in positive_words)
        response1_negative = any(word in response1_lower for word in negative_words)
        response2_positive = any(word in response2_lower for word in positive_words)
        response2_negative = any(word in response2_lower for word in negative_words)
        
        if response1_positive and response2_positive:
            return True
        if response1_negative and response2_negative:
            return True
        
        # Check for exact matches
        if response1_lower == response2_lower:
            return True
        
        return False
    
    def _find_combination_patterns(self) -> List[Dict[str, Any]]:
        """Find patterns in response combinations."""
        patterns = []
        
        # Find common response combinations
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
        common_combinations = combination_counts.most_common(3)
        
        for combo, count in common_combinations:
            if count > 1:  # Only report if combination appears more than once
                percentage = (count / len(response_combinations)) * 100
                if percentage > 10:  # Only report if more than 10% of responses
                    patterns.append({
                        'type': 'combination_pattern',
                        'description': f"Common response combination: {', '.join(combo)}",
                        'confidence': min(85, percentage * 2),
                        'sample_size': count,
                        'percentage': percentage,
                        'combination': list(combo)
                    })
        
        return patterns
    
    def _find_outlier_patterns(self) -> List[Dict[str, Any]]:
        """Find outlier patterns in responses."""
        patterns = []
        
        # Find responses that are significantly different from the norm
        for column in self.columns:
            if column not in ['age', 'gender', 'region', 'education']:
                outlier_pattern = self._analyze_outliers(column)
                if outlier_pattern:
                    patterns.append(outlier_pattern)
        
        return patterns
    
    def _analyze_outliers(self, column: str) -> Optional[Dict[str, Any]]:
        """Analyze outliers in a specific column."""
        values = [row.get(column) for row in self.survey_data if row.get(column)]
        
        if not values:
            return None
        
        # Count responses
        value_counts = Counter(values)
        total_responses = len(values)
        
        # Find responses that appear very rarely (outliers)
        outlier_threshold = total_responses * 0.05  # 5% threshold
        
        outliers = []
        for value, count in value_counts.items():
            if count <= outlier_threshold and count > 0:
                outliers.append({
                    'value': value,
                    'count': count,
                    'percentage': (count / total_responses) * 100
                })
        
        if outliers:
            return {
                'type': 'outlier_pattern',
                'description': f"Outlier responses detected in {column}",
                'confidence': 70,
                'sample_size': total_responses,
                'outliers': outliers
            }
        
        return None
    
    def get_pattern_summary(self) -> Dict[str, Any]:
        """Generate a summary of detected patterns."""
        patterns = self.find_patterns()
        
        summary = {
            'total_patterns': len(patterns),
            'pattern_types': Counter(p['type'] for p in patterns),
            'high_confidence_patterns': [p for p in patterns if p['confidence'] >= 80],
            'medium_confidence_patterns': [p for p in patterns if 60 <= p['confidence'] < 80],
            'low_confidence_patterns': [p for p in patterns if p['confidence'] < 60]
        }
        
        return summary 