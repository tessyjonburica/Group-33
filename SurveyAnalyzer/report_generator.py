#!/usr/bin/env python3
"""
Report Generator Module
Description: Generates comprehensive analysis reports from survey data
and saves them to text files with proper formatting and structure.
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class ReportGenerator:
    """Handles generation of comprehensive survey analysis reports."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.report_sections = []
        self.current_datetime = datetime.now()
        
    def generate_report(self, report_data: Dict[str, Any]) -> bool:
        """
        Generate a comprehensive survey analysis report.
        
        Args:
            report_data: Dictionary containing all analysis results
            
        Returns:
            True if report was generated successfully, False otherwise
        """
        try:
            # Extract data from report_data
            summary = report_data.get('summary', {})
            sentiment = report_data.get('sentiment', {})
            patterns = report_data.get('patterns', [])
            file_path = report_data.get('file_path', 'survey_report.txt')
            
            # Build report content
            report_content = self._build_report_content(summary, sentiment, patterns)
            
            # Write report to file
            success = self._write_report_to_file(report_content, file_path)
            
            return success
            
        except Exception as e:
            print(f"Error generating report: {str(e)}")
            return False
    
    def _build_report_content(self, summary: Dict[str, Any], sentiment: Dict[str, Any], patterns: List[Dict[str, Any]]) -> str:
        """Build the complete report content."""
        report_lines = []
        
        # Header
        report_lines.extend(self._generate_header())
        
        # Executive Summary
        report_lines.extend(self._generate_executive_summary(summary))
        
        # Survey Overview
        report_lines.extend(self._generate_survey_overview(summary))
        
        # Demographic Analysis
        report_lines.extend(self._generate_demographic_analysis(summary))
        
        # Sentiment Analysis
        report_lines.extend(self._generate_sentiment_analysis(sentiment))
        
        # Pattern Analysis
        report_lines.extend(self._generate_pattern_analysis(patterns))
        
        # Statistical Analysis
        report_lines.extend(self._generate_statistical_analysis(summary))
        
        # Key Findings
        report_lines.extend(self._generate_key_findings(summary, sentiment, patterns))
        
        # Recommendations
        report_lines.extend(self._generate_recommendations(summary, sentiment, patterns))
        
        # Footer
        report_lines.extend(self._generate_footer())
        
        return "\n".join(report_lines)
    
    def _generate_header(self) -> List[str]:
        """Generate the report header."""
        header = [
            "=" * 80,
            "SURVEY DATA ANALYSIS REPORT",
            "=" * 80,
            f"Generated on: {self.current_datetime.strftime('%B %d, %Y at %I:%M %p')}",
            f"Report ID: SUR-{self.current_datetime.strftime('%Y%m%d-%H%M%S')}",
            "",
            "This report provides a comprehensive analysis of survey responses including",
            "demographic breakdowns, sentiment analysis, pattern detection, and",
            "statistical insights to support data-driven decision making.",
            "",
            "=" * 80,
            ""
        ]
        return header
    
    def _generate_executive_summary(self, summary: Dict[str, Any]) -> List[str]:
        """Generate the executive summary section."""
        lines = [
            "EXECUTIVE SUMMARY",
            "-" * 50,
            ""
        ]
        
        if summary:
            total_responses = summary.get('total_responses', 0)
            response_rate = summary.get('response_rate', 0)
            
            lines.extend([
                            f"Total Survey Responses: {total_responses:,}",
            f"Response Rate: {response_rate:.1f}%",
                "",
                "Key Highlights:",
                            "- Comprehensive analysis of survey data across multiple dimensions",
            "- Demographic breakdowns reveal respondent characteristics",
            "- Sentiment analysis provides insights into respondent attitudes",
            "- Pattern detection identifies correlations and trends",
            "- Statistical analysis supports evidence-based conclusions",
                ""
            ])
        
        return lines
    
    def _generate_survey_overview(self, summary: Dict[str, Any]) -> List[str]:
        """Generate the survey overview section."""
        lines = [
            "SURVEY OVERVIEW",
            "-" * 50,
            ""
        ]
        
        if summary:
            total_responses = summary.get('total_responses', 0)
            data_quality = summary.get('data_quality', {})
            
            lines.extend([
                f"Survey Details:",
                f"   - Total Responses: {total_responses:,}",
                f"   - Data Quality: {self._assess_data_quality(data_quality)}",
                ""
            ])
            
            # Data quality metrics
            if data_quality:
                completeness = data_quality.get('completeness', {})
                if completeness:
                    lines.append("Data Completeness by Column:")
                    for column, completeness_pct in completeness.items():
                        lines.append(f"   - {column}: {completeness_pct:.1f}%")
                    lines.append("")
        
        return lines
    
    def _generate_demographic_analysis(self, summary: Dict[str, Any]) -> List[str]:
        """Generate the demographic analysis section."""
        lines = [
            "DEMOGRAPHIC ANALYSIS",
            "-" * 50,
            ""
        ]
        
        demographics = summary.get('demographics', {})
        
        if demographics:
            lines.append("👥 Respondent Demographics:")
            lines.append("")
            
            for demo_field, breakdown in demographics.items():
                if breakdown:
                    lines.append(f"{demo_field.title()}:")
                    total_demo = sum(breakdown.values())
                    
                    for category, count in breakdown.items():
                        percentage = (count / total_demo) * 100
                        lines.append(f"   - {category}: {count} ({percentage:.1f}%)")
                    
                    lines.append("")
        else:
            lines.append("No demographic data available for analysis.")
            lines.append("")
        
        return lines
    
    def _generate_sentiment_analysis(self, sentiment: Dict[str, Any]) -> List[str]:
        """Generate the sentiment analysis section."""
        lines = [
            "SENTIMENT ANALYSIS",
            "-" * 50,
            ""
        ]
        
        if sentiment:
            lines.append("💭 Text Response Sentiment Analysis:")
            lines.append("")
            
            for column, results in sentiment.items():
                if isinstance(results, dict) and 'total_responses' in results:
                    lines.append(f"{column}:")
                    lines.append(f"   - Total Responses: {results['total_responses']}")
                    lines.append(f"   - Positive: {results['positive']} ({results['positive_pct']:.1f}%)")
                    lines.append(f"   - Negative: {results['negative']} ({results['negative_pct']:.1f}%)")
                    lines.append(f"   - Neutral: {results['neutral']} ({results['neutral_pct']:.1f}%)")
                    lines.append(f"   - Average Sentiment Score: {results['avg_score']:.2f}")
                    lines.append("")
        else:
            lines.append("No text responses available for sentiment analysis.")
            lines.append("")
        
        return lines
    
    def _generate_pattern_analysis(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate the pattern analysis section."""
        lines = [
            "PATTERN ANALYSIS",
            "-" * 50,
            ""
        ]
        
        if patterns:
            lines.append("Detected Patterns and Correlations:")
            lines.append("")
            
            # Group patterns by type
            pattern_types = {}
            for pattern in patterns:
                pattern_type = pattern.get('type', 'unknown')
                if pattern_type not in pattern_types:
                    pattern_types[pattern_type] = []
                pattern_types[pattern_type].append(pattern)
            
            for pattern_type, type_patterns in pattern_types.items():
                lines.append(f"{pattern_type.replace('_', ' ').title()} Patterns:")
                for pattern in type_patterns:
                    lines.append(f"   - {pattern['description']}")
                    lines.append(f"     Confidence: {pattern['confidence']:.1f}%")
                    lines.append(f"     Sample Size: {pattern['sample_size']}")
                    lines.append("")
        else:
            lines.append("No significant patterns detected in the survey data.")
            lines.append("")
        
        return lines
    
    def _generate_statistical_analysis(self, summary: Dict[str, Any]) -> List[str]:
        """Generate the statistical analysis section."""
        lines = [
            "STATISTICAL ANALYSIS",
            "-" * 50,
            ""
        ]
        
        question_summaries = summary.get('question_summaries', {})
        
        if question_summaries:
            lines.append("Response Distribution Analysis:")
            lines.append("")
            
            for question, q_summary in question_summaries.items():
                if isinstance(q_summary, dict):
                    lines.append(f"{question}:")
                    lines.append(f"   - Total Responses: {q_summary.get('total_responses', 0)}")
                    lines.append(f"   - Response Rate: {q_summary.get('response_rate', 0):.1f}%")
                    
                    top_responses = q_summary.get('top_responses', [])
                    if top_responses:
                        lines.append("   - Top Responses:")
                        for response, count in top_responses[:3]:
                            percentage = (count / q_summary['total_responses']) * 100
                            lines.append(f"     - {response}: {count} ({percentage:.1f}%)")
                    
                    lines.append("")
        else:
            lines.append("No question response data available for statistical analysis.")
            lines.append("")
        
        return lines
    
    def _generate_key_findings(self, summary: Dict[str, Any], sentiment: Dict[str, Any], patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate the key findings section."""
        lines = [
            "KEY FINDINGS",
            "-" * 50,
            ""
        ]
        
        findings = []
        
        # Demographic findings
        demographics = summary.get('demographics', {})
        if demographics:
            for demo_field, breakdown in demographics.items():
                if breakdown:
                    most_common = max(breakdown.items(), key=lambda x: x[1])
                    findings.append(f"- {demo_field.title()}: {most_common[0]} is the most common category ({most_common[1]} responses)")
        
        # Sentiment findings
        if sentiment:
            for column, results in sentiment.items():
                if isinstance(results, dict):
                    dominant_sentiment = self._get_dominant_sentiment(results)
                    findings.append(f"- {column}: {dominant_sentiment} sentiment dominates the responses")
        
        # Pattern findings
        if patterns:
            high_confidence_patterns = [p for p in patterns if p.get('confidence', 0) >= 80]
            if high_confidence_patterns:
                findings.append(f"- {len(high_confidence_patterns)} high-confidence patterns detected in the data")
        
        if findings:
            lines.extend(findings)
        else:
            lines.append("No significant findings to report at this time.")
        
        lines.append("")
        return lines
    
    def _generate_recommendations(self, summary: Dict[str, Any], sentiment: Dict[str, Any], patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate the recommendations section."""
        lines = [
            "RECOMMENDATIONS",
            "-" * 50,
            ""
        ]
        
        recommendations = []
        
        # Data quality recommendations
        data_quality = summary.get('data_quality', {})
        if data_quality:
            completeness = data_quality.get('completeness', {})
            low_completeness = [col for col, comp in completeness.items() if comp < 80]
            if low_completeness:
                recommendations.append(f"- Improve data collection for columns with low completeness: {', '.join(low_completeness)}")
        
        # Sentiment-based recommendations
        if sentiment:
            negative_sentiment_columns = []
            for column, results in sentiment.items():
                if isinstance(results, dict) and results.get('negative_pct', 0) > 30:
                    negative_sentiment_columns.append(column)
            
            if negative_sentiment_columns:
                recommendations.append(f"- Address concerns in columns with high negative sentiment: {', '.join(negative_sentiment_columns)}")
        
        # Pattern-based recommendations
        if patterns:
            high_confidence_patterns = [p for p in patterns if p.get('confidence', 0) >= 80]
            if high_confidence_patterns:
                recommendations.append(f"- Investigate {len(high_confidence_patterns)} high-confidence patterns for actionable insights")
        
        # General recommendations
        recommendations.extend([
            "- Consider conducting follow-up surveys to validate findings",
            "- Implement targeted improvements based on demographic insights",
            "- Monitor sentiment trends over time for continuous improvement",
            "- Use statistical insights to inform decision-making processes"
        ])
        
        lines.extend(recommendations)
        lines.append("")
        
        return lines
    
    def _generate_footer(self) -> List[str]:
        """Generate the report footer."""
        footer = [
            "=" * 80,
            "REPORT END",
            "=" * 80,
            "",
            "This report was generated automatically by the Survey Data Analyzer.",
            "For questions or additional analysis, please contact the development team.",
            "",
            f"Report generated on: {self.current_datetime.strftime('%B %d, %Y at %I:%M %p')}",
            "=" * 80
        ]
        return footer
    
    def _assess_data_quality(self, data_quality: Dict[str, Any]) -> str:
        """Assess overall data quality."""
        if not data_quality:
            return "Unknown"
        
        completeness = data_quality.get('completeness', {})
        if not completeness:
            return "Unknown"
        
        avg_completeness = sum(completeness.values()) / len(completeness)
        
        if avg_completeness >= 90:
            return "Excellent"
        elif avg_completeness >= 80:
            return "Good"
        elif avg_completeness >= 70:
            return "Fair"
        else:
            return "Poor"
    
    def _get_dominant_sentiment(self, sentiment_results: Dict[str, Any]) -> str:
        """Get the dominant sentiment from results."""
        positive_pct = sentiment_results.get('positive_pct', 0)
        negative_pct = sentiment_results.get('negative_pct', 0)
        neutral_pct = sentiment_results.get('neutral_pct', 0)
        
        if positive_pct > negative_pct and positive_pct > neutral_pct:
            return "Positive"
        elif negative_pct > positive_pct and negative_pct > neutral_pct:
            return "Negative"
        else:
            return "Neutral"
    
    def _write_report_to_file(self, content: str, file_path: str) -> bool:
        """Write the report content to a file."""
        try:
            # Ensure directory exists
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Write content to file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return True
            
        except Exception as e:
            print(f"Error writing report to file: {str(e)}")
            return False
    
    def generate_summary_report(self, summary_data: Dict[str, Any], file_path: str = "summary_report.txt") -> bool:
        """Generate a simplified summary report."""
        try:
            lines = [
                "SURVEY SUMMARY REPORT",
                "=" * 50,
                f"Generated: {self.current_datetime.strftime('%B %d, %Y')}",
                "",
                f"Total Responses: {summary_data.get('total_responses', 0)}",
                f"Response Rate: {summary_data.get('response_rate', 0):.1f}%",
                "",
                "Key Metrics:",
                            "- Data quality assessment",
            "- Demographic breakdowns",
            "- Response distributions",
            "- Pattern detection results",
                "",
                "=" * 50
            ]
            
            content = "\n".join(lines)
            return self._write_report_to_file(content, file_path)
            
        except Exception as e:
            print(f"Error generating summary report: {str(e)}")
            return False 