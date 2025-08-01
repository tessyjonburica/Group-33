#!/usr/bin/env python3
"""
Survey Data Analyzer - Main CLI Application
Author: Student Developer
Description: Main entry point for the Survey Data Analyzer CLI tool.
Provides a menu-driven interface for analyzing survey data from CSV files.
"""

import sys
import os
from typing import Optional, Dict, Any
from data_loader import DataLoader
from survey_summary import SurveySummary
from stats_analyzer import StatsAnalyzer
from sentiment_analyzer import SentimentAnalyzer
from pattern_detector import PatternDetector
from report_generator import ReportGenerator
from utils import clear_screen, print_header, print_menu


class SurveyAnalyzerCLI:
    """Main CLI application class for Survey Data Analyzer."""
    
    def __init__(self):
        """Initialize the CLI application with empty data containers."""
        self.data_loader = DataLoader()
        self.survey_data = None
        self.survey_summary = None
        self.stats_analyzer = None
        self.sentiment_analyzer = None
        self.pattern_detector = None
        self.report_generator = None
        
    def load_survey_data(self) -> bool:
        """Load survey data from CSV file."""
        try:
            print_header("Load Survey Data")
            file_path = input("Enter the path to your CSV file: ").strip()
            
            if not file_path:
                print("ERROR: No file path provided.")
                return False
                
            if not os.path.exists(file_path):
                print(f"ERROR: File not found: {file_path}")
                return False
                
            self.survey_data = self.data_loader.load_csv(file_path)
            if self.survey_data:
                print(f"SUCCESS: Successfully loaded {len(self.survey_data)} survey responses")
                print(f"INFO: Columns: {', '.join(self.survey_data[0].keys())}")
                return True
            else:
                print("ERROR: Failed to load survey data")
                return False
                
        except Exception as e:
            print(f"ERROR: Error loading data: {str(e)}")
            return False
    
    def view_summary_statistics(self):
        """Display summary statistics for the loaded survey data."""
        if not self.survey_data:
            print("ERROR: No survey data loaded. Please load data first.")
            return
            
        try:
            print_header("Survey Summary Statistics")
            self.survey_summary = SurveySummary(self.survey_data)
            summary = self.survey_summary.generate_summary()
            
            print("\nRESPONSE OVERVIEW:")
            print(f"   Total Responses: {summary['total_responses']}")
            print(f"   Response Rate: {summary['response_rate']:.1f}%")
            
            print("\nDEMOGRAPHIC BREAKDOWN:")
            for demo, breakdown in summary['demographics'].items():
                print(f"\n   {demo.upper()}:")
                for category, count in breakdown.items():
                    percentage = (count / summary['total_responses']) * 100
                    print(f"     {category}: {count} ({percentage:.1f}%)")
                    
        except Exception as e:
            print(f"ERROR: Error generating summary: {str(e)}")
    
    def analyze_sentiment(self):
        """Analyze sentiment of text responses."""
        if not self.survey_data:
            print("ERROR: No survey data loaded. Please load data first.")
            return
            
        try:
            print_header("Sentiment Analysis")
            self.sentiment_analyzer = SentimentAnalyzer()
            
            # Find text columns
            text_columns = []
            for col in self.survey_data[0].keys():
                if any(isinstance(row[col], str) and len(str(row[col])) > 20 
                      for row in self.survey_data[:10]):
                    text_columns.append(col)
            
            if not text_columns:
                print("ERROR: No text columns found for sentiment analysis.")
                return
                
            print(f"INFO: Found text columns: {', '.join(text_columns)}")
            
            for column in text_columns:
                print(f"\nANALYZING: Analyzing sentiment for '{column}':")
                sentiment_results = self.sentiment_analyzer.analyze_column(
                    self.survey_data, column
                )
                
                print(f"   Positive responses: {sentiment_results['positive']} ({sentiment_results['positive_pct']:.1f}%)")
                print(f"   Negative responses: {sentiment_results['negative']} ({sentiment_results['negative_pct']:.1f}%)")
                print(f"   Neutral responses: {sentiment_results['neutral']} ({sentiment_results['neutral_pct']:.1f}%)")
                print(f"   Average sentiment score: {sentiment_results['avg_score']:.2f}")
                
        except Exception as e:
            print(f"ERROR: Error analyzing sentiment: {str(e)}")
    
    def cross_tabulate_results(self):
        """Perform cross-tabulation analysis."""
        if not self.survey_data:
            print("ERROR: No survey data loaded. Please load data first.")
            return
            
        try:
            print_header("Cross-Tabulation Analysis")
            self.stats_analyzer = StatsAnalyzer(self.survey_data)
            
            # Get available columns
            columns = list(self.survey_data[0].keys())
            print(f"Available columns: {', '.join(columns)}")
            
            col1 = input("Enter first column name: ").strip()
            col2 = input("Enter second column name: ").strip()
            
            if col1 not in columns or col2 not in columns:
                print("ERROR: Invalid column names.")
                return
                
            crosstab = self.stats_analyzer.cross_tabulate(col1, col2)
            chi_square = self.stats_analyzer.chi_square_test(col1, col2)
            
            print(f"\nCROSS-TABULATION: {col1} vs {col2}")
            print("=" * 50)
            
            # Display crosstab
            for row in crosstab:
                print(" | ".join(f"{cell:>8}" for cell in row))
                
            print(f"\nCHI-SQUARE TEST RESULTS:")
            print(f"   Chi-Square Value: {chi_square['chi_square']:.4f}")
            print(f"   P-Value: {chi_square['p_value']:.4f}")
            print(f"   Degrees of Freedom: {chi_square['df']}")
            print(f"   Significant: {'Yes' if chi_square['significant'] else 'No'}")
            
        except Exception as e:
            print(f"ERROR: Error in cross-tabulation: {str(e)}")
    
    def detect_patterns(self):
        """Detect patterns and correlations in survey responses."""
        if not self.survey_data:
            print("ERROR: No survey data loaded. Please load data first.")
            return
            
        try:
            print_header("Pattern Detection")
            self.pattern_detector = PatternDetector(self.survey_data)
            
            patterns = self.pattern_detector.find_patterns()
            
            print("DETECTED PATTERNS:")
            print("=" * 50)
            
            for pattern in patterns:
                print(f"\nPATTERN: {pattern['description']}")
                print(f"   Confidence: {pattern['confidence']:.1f}%")
                print(f"   Sample size: {pattern['sample_size']}")
                
        except Exception as e:
            print(f"ERROR: Error detecting patterns: {str(e)}")
    
    def generate_report(self):
        """Generate a comprehensive analysis report."""
        if not self.survey_data:
            print("ERROR: No survey data loaded. Please load data first.")
            return
            
        try:
            print_header("Generate Report")
            
            # Initialize all analyzers
            self.survey_summary = SurveySummary(self.survey_data)
            self.stats_analyzer = StatsAnalyzer(self.survey_data)
            self.sentiment_analyzer = SentimentAnalyzer()
            self.pattern_detector = PatternDetector(self.survey_data)
            self.report_generator = ReportGenerator()
            
            output_file = input("Enter output file name (default: survey_report.txt): ").strip()
            if not output_file:
                output_file = "survey_report.txt"
                
            if not output_file.endswith('.txt'):
                output_file += '.txt'
                
            # Generate comprehensive report
            report_data = {
                'summary': self.survey_summary.generate_summary(),
                'sentiment': self.sentiment_analyzer.analyze_all_text_columns(self.survey_data),
                'patterns': self.pattern_detector.find_patterns(),
                'file_path': output_file
            }
            
            success = self.report_generator.generate_report(report_data)
            
            if success:
                print(f"SUCCESS: Report generated successfully: {output_file}")
            else:
                print("ERROR: Failed to generate report")
                
        except Exception as e:
            print(f"ERROR: Error generating report: {str(e)}")
    
    def run(self):
        """Main application loop."""
        while True:
            clear_screen()
            print_header("Survey Data Analyzer")
            
            if self.survey_data:
                print(f"INFO: Loaded: {len(self.survey_data)} responses")
            else:
                print("INFO: No data loaded")
                
            print_menu([
                "Load survey data",
                "View summary statistics",
                "Analyze sentiment",
                "Cross-tabulate results",
                "Detect patterns",
                "Generate report",
                "Exit"
            ])
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.load_survey_data()
            elif choice == '2':
                self.view_summary_statistics()
            elif choice == '3':
                self.analyze_sentiment()
            elif choice == '4':
                self.cross_tabulate_results()
            elif choice == '5':
                self.detect_patterns()
            elif choice == '6':
                self.generate_report()
            elif choice == '7':
                print("\nThank you for using Survey Data Analyzer!")
                sys.exit(0)
            else:
                print("ERROR: Invalid choice. Please try again.")
                
            input("\nPress Enter to continue...")


def main():
    """Main entry point for the application."""
    try:
        app = SurveyAnalyzerCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 