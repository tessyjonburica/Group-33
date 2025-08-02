#!/usr/bin/env python3
"""
Survey Data Loader Module
Author: Student Developer
Description: Handles CSV file loading, validation, and data preprocessing.
Provides robust error handling and data consistency checks.
"""

import csv
import os
import sys
from typing import List, Dict, Any, Optional
from collections import defaultdict


class DataLoader:
    """Handles loading and validation of survey data from CSV files."""
    
    def __init__(self):
        """Initialize the data loader with validation settings."""
        self.required_fields = ['age', 'gender', 'region']  # Common required fields
        self.max_file_size = 50 * 1024 * 1024  # 50MB limit
        self.supported_encodings = ['utf-8', 'latin-1', 'cp1252']
        
    def load_csv(self, file_path: str) -> Optional[List[Dict[str, Any]]]:
        """
        Load and validate CSV survey data.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            List of dictionaries representing survey responses, or None if failed
        """
        try:
            # Validate file exists and is readable
            if not self._validate_file(file_path):
                return None
                
            # Try different encodings
            data = None
            for encoding in self.supported_encodings:
                try:
                    data = self._read_csv_with_encoding(file_path, encoding)
                    if data:
                        break
                except UnicodeDecodeError:
                    continue
                    
            if not data:
                print("ERROR: Could not read file with any supported encoding")
                return None
                
            # Validate and clean data
            cleaned_data = self._clean_and_validate_data(data)
            if not cleaned_data:
                return None
                
            print(f"SUCCESS: Data validation completed successfully")
            return cleaned_data
            
        except Exception as e:
            print(f"ERROR: Error loading CSV file: {str(e)}")
            return None
    
    def _validate_file(self, file_path: str) -> bool:
        """Validate that the file exists and is accessible."""
        try:
            if not os.path.exists(file_path):
                print(f"ERROR: File not found: {file_path}")
                return False
                
            if not os.path.isfile(file_path):
                print(f"ERROR: Path is not a file: {file_path}")
                return False
                
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                print(f"ERROR: File too large: {file_size / (1024*1024):.1f}MB (max: 50MB)")
                return False
                
            if file_size == 0:
                print("ERROR: File is empty")
                return False
                
            return True
            
        except Exception as e:
            print(f"ERROR: Error validating file: {str(e)}")
            return False
    
    def _read_csv_with_encoding(self, file_path: str, encoding: str) -> Optional[List[Dict[str, Any]]]:
        """Read CSV file with specified encoding."""
        try:
            with open(file_path, 'r', encoding=encoding, newline='') as file:
                # Try to detect delimiter
                sample = file.read(1024)
                file.seek(0)
                
                # Common delimiters to try
                delimiters = [',', ';', '\t', '|']
                detected_delimiter = ','
                
                for delimiter in delimiters:
                    if delimiter in sample:
                        detected_delimiter = delimiter
                        break
                
                reader = csv.DictReader(file, delimiter=detected_delimiter)
                data = list(reader)
                
                if not data:
                    print("ERROR: No data found in CSV file")
                    return None
                    
                print(f"SUCCESS: Loaded {len(data)} rows with {len(data[0])} columns")
                print(f"INFO: Columns: {', '.join(data[0].keys())}")
                
                return data
                
        except Exception as e:
            print(f"ERROR: Error reading CSV with {encoding} encoding: {str(e)}")
            return None
    
    def _clean_and_validate_data(self, data: List[Dict[str, Any]]) -> Optional[List[Dict[str, Any]]]:
        """Clean and validate the loaded data."""
        try:
            if not data:
                return None
                
            cleaned_data = []
            validation_errors = []
            
            for i, row in enumerate(data, 1):
                cleaned_row = {}
                row_errors = []
                
                for key, value in row.items():
                    # Clean the key (remove whitespace, normalize)
                    if key is None:
                        continue  # Skip rows with None keys
                    clean_key = str(key).strip().lower().replace(' ', '_')
                    
                    # Clean the value
                    if value is None or value == '':
                        cleaned_value = None
                    else:
                        cleaned_value = str(value).strip()
                        if cleaned_value.lower() in ['na', 'n/a', 'null', 'none']:
                            cleaned_value = None
                    
                    cleaned_row[clean_key] = cleaned_value
                
                # Basic validation
                if self._validate_row(cleaned_row, i):
                    cleaned_data.append(cleaned_row)
                else:
                    validation_errors.append(f"Row {i}: Invalid data")
            
            # Report validation results
            total_rows = len(data)
            valid_rows = len(cleaned_data)
            invalid_rows = total_rows - valid_rows
            
            print(f"INFO: Data validation results:")
            print(f"   Total rows: {total_rows}")
            print(f"   Valid rows: {valid_rows}")
            print(f"   Invalid rows: {invalid_rows}")
            
            if invalid_rows > 0:
                print(f"WARNING: {invalid_rows} rows had validation issues")
            
            if valid_rows == 0:
                print("ERROR: No valid data found")
                return None
                
            return cleaned_data
            
        except Exception as e:
            print(f"ERROR: Error cleaning data: {str(e)}")
            return None
    
    def _validate_row(self, row: Dict[str, Any], row_num: int) -> bool:
        """Validate a single row of data."""
        try:
            # Check for minimum required fields
            if len(row) < 2:
                return False
                
            # Validate age if present
            if 'age' in row and row['age'] is not None:
                try:
                    age = int(row['age'])
                    if age < 0 or age > 120:
                        return False
                except (ValueError, TypeError):
                    return False
            
            # Validate gender if present
            if 'gender' in row and row['gender'] is not None:
                try:
                    gender = str(row['gender']).lower()
                    valid_genders = ['male', 'female', 'm', 'f', 'other', 'prefer not to say']
                    if gender not in valid_genders:
                        return False
                except (AttributeError, TypeError):
                    return False
            
            return True
            
        except Exception:
            return False
    
    def get_data_summary(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of the loaded data."""
        if not data:
            return {}
            
        summary = {
            'total_rows': len(data),
            'columns': list(data[0].keys()) if data else [],
            'missing_values': {},
            'unique_values': {}
        }
        
        # Analyze missing values and unique values
        for column in summary['columns']:
            values = [row.get(column) for row in data]
            missing_count = sum(1 for v in values if v is None or v == '')
            summary['missing_values'][column] = {
                'count': missing_count,
                'percentage': (missing_count / len(data)) * 100
            }
            
            unique_vals = set(v for v in values if v is not None and v != '')
            summary['unique_values'][column] = len(unique_vals)
        
        return summary
    
    def export_sample_data(self, file_path: str = "sample_survey.csv"):
        """Create a sample CSV file for testing."""
        sample_data = [
            {
                'age': '25',
                'gender': 'Female',
                'region': 'North',
                'education': 'Bachelor',
                'satisfaction': 'Very Satisfied',
                'feedback': 'Great experience with the product!',
                'recommend': 'Yes'
            },
            {
                'age': '32',
                'gender': 'Male',
                'region': 'South',
                'education': 'Master',
                'satisfaction': 'Satisfied',
                'feedback': 'Good but could be better.',
                'recommend': 'Yes'
            },
            {
                'age': '45',
                'gender': 'Female',
                'region': 'East',
                'education': 'High School',
                'satisfaction': 'Neutral',
                'feedback': 'It was okay, nothing special.',
                'recommend': 'Maybe'
            },
            {
                'age': '28',
                'gender': 'Male',
                'region': 'West',
                'education': 'Bachelor',
                'satisfaction': 'Dissatisfied',
                'feedback': 'Poor quality and bad service.',
                'recommend': 'No'
            },
            {
                'age': '35',
                'gender': 'Female',
                'region': 'North',
                'education': 'PhD',
                'satisfaction': 'Very Satisfied',
                'feedback': 'Excellent product and amazing support!',
                'recommend': 'Yes'
            }
        ]
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                if sample_data:
                    writer = csv.DictWriter(file, fieldnames=sample_data[0].keys())
                    writer.writeheader()
                    writer.writerows(sample_data)
                    
            print(f"SUCCESS: Sample data exported to {file_path}")
            return True
            
        except Exception as e:
            print(f"ERROR: Error exporting sample data: {str(e)}")
            return False 