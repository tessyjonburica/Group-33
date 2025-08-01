#!/usr/bin/env python3
"""
Survey Summary Module
Author: Student Developer
Description: Generates summary statistics, response counts, percentages,
and demographic breakdowns for survey data analysis.
"""

import statistics
from typing import List, Dict, Any, Optional
from collections import defaultdict, Counter


class SurveySummary:
    """Handles generation of survey summary statistics and demographic breakdowns."""
    
    def __init__(self, survey_data: List[Dict[str, Any]]):
        """
        Initialize the survey summary analyzer.
        
        Args:
            survey_data: List of dictionaries containing survey responses
        """
        self.survey_data = survey_data
        self.total_responses = len(survey_data)
        self.columns = list(survey_data[0].keys()) if survey_data else []
        
    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics.
        
        Returns:
            Dictionary containing all summary statistics
        """
        if not self.survey_data:
            return {}
            
        summary = {
            'total_responses': self.total_responses,
            'response_rate': self._calculate_response_rate(),
            'demographics': self._analyze_demographics(),
            'question_summaries': self._analyze_questions(),
            'data_quality': self._assess_data_quality()
        }
        
        return summary
    
    def _calculate_response_rate(self) -> float:
        """Calculate the response rate (placeholder for actual calculation)."""
        # In a real scenario, this would compare against expected responses
        # For now, we'll use a placeholder calculation
        return 85.5  # Placeholder response rate
    
    def _analyze_demographics(self) -> Dict[str, Dict[str, int]]:
        """Analyze demographic breakdowns."""
        demographics = {}
        
        # Common demographic fields
        demo_fields = ['age', 'gender', 'region', 'education', 'income']
        
        for field in demo_fields:
            if field in self.columns:
                demographics[field] = self._count_responses_by_field(field)
        
        return demographics
    
    def _analyze_questions(self) -> Dict[str, Dict[str, Any]]:
        """Analyze responses for each question."""
        question_summaries = {}
        
        for column in self.columns:
            if column not in ['age', 'gender', 'region', 'education', 'income']:
                question_summaries[column] = self._analyze_question_responses(column)
        
        return question_summaries
    
    def _count_responses_by_field(self, field: str) -> Dict[str, int]:
        """Count responses for a specific field."""
        counts = Counter()
        
        for row in self.survey_data:
            value = row.get(field)
            if value is not None and str(value).strip():
                # Normalize the value
                normalized_value = str(value).strip().title()
                counts[normalized_value] += 1
        
        return dict(counts)
    
    def _analyze_question_responses(self, question: str) -> Dict[str, Any]:
        """Analyze responses for a specific question."""
        responses = [row.get(question) for row in self.survey_data]
        valid_responses = [r for r in responses if r is not None and str(r).strip()]
        
        if not valid_responses:
            return {
                'total_responses': 0,
                'missing_responses': len(responses),
                'response_rate': 0.0,
                'top_responses': [],
                'response_distribution': {}
            }
        
        # Count responses
        response_counts = Counter(valid_responses)
        
        # Calculate percentages
        total_valid = len(valid_responses)
        response_distribution = {}
        for response, count in response_counts.items():
            percentage = (count / total_valid) * 100
            response_distribution[response] = {
                'count': count,
                'percentage': percentage
            }
        
        # Get top responses
        top_responses = response_counts.most_common(5)
        
        return {
            'total_responses': total_valid,
            'missing_responses': len(responses) - total_valid,
            'response_rate': (total_valid / len(responses)) * 100,
            'top_responses': top_responses,
            'response_distribution': response_distribution
        }
    
    def _assess_data_quality(self) -> Dict[str, Any]:
        """Assess the quality of the survey data."""
        quality_metrics = {
            'total_rows': len(self.survey_data),
            'total_columns': len(self.columns),
            'missing_data': {},
            'completeness': {}
        }
        
        # Analyze missing data for each column
        for column in self.columns:
            values = [row.get(column) for row in self.survey_data]
            missing_count = sum(1 for v in values if v is None or str(v).strip() == '')
            missing_percentage = (missing_count / len(values)) * 100
            
            quality_metrics['missing_data'][column] = {
                'count': missing_count,
                'percentage': missing_percentage
            }
            
            quality_metrics['completeness'][column] = 100 - missing_percentage
        
        return quality_metrics
    
    def get_age_distribution(self) -> Dict[str, int]:
        """Get age distribution if age data is available."""
        if 'age' not in self.columns:
            return {}
        
        age_groups = {
            '18-25': 0,
            '26-35': 0,
            '36-45': 0,
            '46-55': 0,
            '56-65': 0,
            '65+': 0
        }
        
        for row in self.survey_data:
            age_str = row.get('age')
            if age_str and str(age_str).isdigit():
                try:
                    age = int(age_str)
                    if 18 <= age <= 25:
                        age_groups['18-25'] += 1
                    elif 26 <= age <= 35:
                        age_groups['26-35'] += 1
                    elif 36 <= age <= 45:
                        age_groups['36-45'] += 1
                    elif 46 <= age <= 55:
                        age_groups['46-55'] += 1
                    elif 56 <= age <= 65:
                        age_groups['56-65'] += 1
                    elif age > 65:
                        age_groups['65+'] += 1
                except ValueError:
                    continue
        
        return age_groups
    
    def get_gender_distribution(self) -> Dict[str, int]:
        """Get gender distribution if gender data is available."""
        if 'gender' not in self.columns:
            return {}
        
        return self._count_responses_by_field('gender')
    
    def get_regional_distribution(self) -> Dict[str, int]:
        """Get regional distribution if region data is available."""
        if 'region' not in self.columns:
            return {}
        
        return self._count_responses_by_field('region')
    
    def get_education_distribution(self) -> Dict[str, int]:
        """Get education distribution if education data is available."""
        if 'education' not in self.columns:
            return {}
        
        return self._count_responses_by_field('education')
    
    def calculate_average_age(self) -> Optional[float]:
        """Calculate average age if age data is available."""
        if 'age' not in self.columns:
            return None
        
        ages = []
        for row in self.survey_data:
            age_str = row.get('age')
            if age_str and str(age_str).isdigit():
                try:
                    ages.append(int(age_str))
                except ValueError:
                    continue
        
        if ages:
            return statistics.mean(ages)
        return None
    
    def get_response_trends(self) -> Dict[str, Any]:
        """Identify response trends and patterns."""
        trends = {
            'most_common_responses': {},
            'response_patterns': [],
            'outliers': []
        }
        
        # Find most common responses for each question
        for column in self.columns:
            if column not in ['age', 'gender', 'region', 'education', 'income']:
                responses = [row.get(column) for row in self.survey_data]
                valid_responses = [r for r in responses if r is not None and str(r).strip()]
                
                if valid_responses:
                    response_counts = Counter(valid_responses)
                    most_common = response_counts.most_common(1)
                    if most_common:
                        trends['most_common_responses'][column] = {
                            'response': most_common[0][0],
                            'count': most_common[0][1],
                            'percentage': (most_common[0][1] / len(valid_responses)) * 100
                        }
        
        return trends
    
    def generate_demographic_report(self) -> str:
        """Generate a formatted demographic report."""
        if not self.survey_data:
            return "No data available for demographic analysis."
        
        report_lines = []
        report_lines.append("DEMOGRAPHIC ANALYSIS REPORT")
        report_lines.append("=" * 50)
        report_lines.append(f"Total Responses: {self.total_responses}")
        report_lines.append("")
        
        # Age distribution
        age_dist = self.get_age_distribution()
        if age_dist:
            report_lines.append("AGE DISTRIBUTION:")
            for age_group, count in age_dist.items():
                percentage = (count / self.total_responses) * 100
                report_lines.append(f"  {age_group}: {count} ({percentage:.1f}%)")
            report_lines.append("")
        
        # Gender distribution
        gender_dist = self.get_gender_distribution()
        if gender_dist:
            report_lines.append("GENDER DISTRIBUTION:")
            for gender, count in gender_dist.items():
                percentage = (count / self.total_responses) * 100
                report_lines.append(f"  {gender}: {count} ({percentage:.1f}%)")
            report_lines.append("")
        
        # Regional distribution
        region_dist = self.get_regional_distribution()
        if region_dist:
            report_lines.append("REGIONAL DISTRIBUTION:")
            for region, count in region_dist.items():
                percentage = (count / self.total_responses) * 100
                report_lines.append(f"  {region}: {count} ({percentage:.1f}%)")
            report_lines.append("")
        
        # Education distribution
        education_dist = self.get_education_distribution()
        if education_dist:
            report_lines.append("EDUCATION DISTRIBUTION:")
            for education, count in education_dist.items():
                percentage = (count / self.total_responses) * 100
                report_lines.append(f"  {education}: {count} ({percentage:.1f}%)")
            report_lines.append("")
        
        return "\n".join(report_lines) 