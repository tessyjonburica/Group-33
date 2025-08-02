#!/usr/bin/env python3
"""
Unit Tests for Data Loader Module
Author: Student Developer
Description: Comprehensive unit tests for CSV data loading and validation functionality.
"""

import unittest
import tempfile
import os
import csv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_loader import DataLoader


class TestDataLoader(unittest.TestCase):
    """Test cases for the DataLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.data_loader = DataLoader()
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_validate_file_existing(self):
        """Test file validation with existing file."""
        # Create a temporary file
        temp_file = os.path.join(self.temp_dir, "test.csv")
        with open(temp_file, 'w') as f:
            f.write("test data")
        
        result = self.data_loader._validate_file(temp_file)
        self.assertTrue(result)
    
    def test_validate_file_nonexistent(self):
        """Test file validation with non-existent file."""
        result = self.data_loader._validate_file("nonexistent_file.csv")
        self.assertFalse(result)
    
    def test_validate_file_empty(self):
        """Test file validation with empty file."""
        temp_file = os.path.join(self.temp_dir, "empty.csv")
        with open(temp_file, 'w') as f:
            pass  # Create empty file
        
        result = self.data_loader._validate_file(temp_file)
        self.assertFalse(result)
    
    def test_validate_file_too_large(self):
        """Test file validation with file too large."""
        temp_file = os.path.join(self.temp_dir, "large.csv")
        # Create a file larger than 50MB
        with open(temp_file, 'w') as f:
            f.write("x" * (51 * 1024 * 1024))  # 51MB
        
        result = self.data_loader._validate_file(temp_file)
        self.assertFalse(result)
    
    def test_read_csv_with_encoding_utf8(self):
        """Test CSV reading with UTF-8 encoding."""
        temp_file = os.path.join(self.temp_dir, "test_utf8.csv")
        
        # Create test CSV data
        test_data = [
            {'name': 'John', 'age': '25', 'city': 'New York'},
            {'name': 'Jane', 'age': '30', 'city': 'Los Angeles'},
            {'name': 'Bob', 'age': '35', 'city': 'Chicago'}
        ]
        
        with open(temp_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'age', 'city'])
            writer.writeheader()
            writer.writerows(test_data)
        
        result = self.data_loader._read_csv_with_encoding(temp_file, 'utf-8')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['name'], 'John')
    
    def test_read_csv_with_encoding_latin1(self):
        """Test CSV reading with Latin-1 encoding."""
        temp_file = os.path.join(self.temp_dir, "test_latin1.csv")
        
        # Create test CSV data
        test_data = [
            {'name': 'José', 'age': '25', 'city': 'Madrid'},
            {'name': 'François', 'age': '30', 'city': 'Paris'}
        ]
        
        with open(temp_file, 'w', newline='', encoding='latin-1') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'age', 'city'])
            writer.writeheader()
            writer.writerows(test_data)
        
        result = self.data_loader._read_csv_with_encoding(temp_file, 'latin-1')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 2)
    
    def test_clean_and_validate_data_valid(self):
        """Test data cleaning and validation with valid data."""
        test_data = [
            {'age': '25', 'gender': 'Male', 'region': 'North'},
            {'age': '30', 'gender': 'Female', 'region': 'South'},
            {'age': '35', 'gender': 'Male', 'region': 'East'}
        ]
        
        result = self.data_loader._clean_and_validate_data(test_data)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
    
    def test_clean_and_validate_data_invalid_age(self):
        """Test data cleaning with invalid age data."""
        test_data = [
            {'age': '25', 'gender': 'Male', 'region': 'North'},
            {'age': '150', 'gender': 'Female', 'region': 'South'},  # Invalid age
            {'age': '35', 'gender': 'Male', 'region': 'East'}
        ]
        
        result = self.data_loader._clean_and_validate_data(test_data)
        self.assertIsNotNone(result)
        # Should filter out invalid age
        self.assertEqual(len(result), 2)
    
    def test_clean_and_validate_data_invalid_gender(self):
        """Test data cleaning with invalid gender data."""
        test_data = [
            {'age': '25', 'gender': 'Male', 'region': 'North'},
            {'age': '30', 'gender': 'Invalid', 'region': 'South'},  # Invalid gender
            {'age': '35', 'gender': 'Female', 'region': 'East'}
        ]
        
        result = self.data_loader._clean_and_validate_data(test_data)
        self.assertIsNotNone(result)
        # Should filter out invalid gender
        self.assertEqual(len(result), 2)
    
    def test_clean_and_validate_data_empty(self):
        """Test data cleaning with empty data."""
        result = self.data_loader._clean_and_validate_data([])
        self.assertIsNone(result)
    
    def test_validate_row_valid(self):
        """Test row validation with valid data."""
        valid_row = {'age': '25', 'gender': 'Male', 'region': 'North'}
        result = self.data_loader._validate_row(valid_row, 1)
        self.assertTrue(result)
    
    def test_validate_row_invalid_age(self):
        """Test row validation with invalid age."""
        invalid_row = {'age': '150', 'gender': 'Male', 'region': 'North'}
        result = self.data_loader._validate_row(invalid_row, 1)
        self.assertFalse(result)
    
    def test_validate_row_invalid_gender(self):
        """Test row validation with invalid gender."""
        invalid_row = {'age': '25', 'gender': 'Invalid', 'region': 'North'}
        result = self.data_loader._validate_row(invalid_row, 1)
        self.assertFalse(result)
    
    def test_validate_row_insufficient_fields(self):
        """Test row validation with insufficient fields."""
        invalid_row = {'age': '25'}  # Only one field
        result = self.data_loader._validate_row(invalid_row, 1)
        self.assertFalse(result)
    
    def test_get_data_summary(self):
        """Test data summary generation."""
        test_data = [
            {'age': '25', 'gender': 'Male', 'region': 'North'},
            {'age': '30', 'gender': 'Female', 'region': 'South'},
            {'age': '35', 'gender': 'Male', 'region': 'East'}
        ]
        
        summary = self.data_loader.get_data_summary(test_data)
        
        self.assertIn('total_rows', summary)
        self.assertIn('columns', summary)
        self.assertIn('missing_values', summary)
        self.assertIn('unique_values', summary)
        
        self.assertEqual(summary['total_rows'], 3)
        self.assertEqual(len(summary['columns']), 3)
    
    def test_export_sample_data(self):
        """Test sample data export functionality."""
        temp_file = os.path.join(self.temp_dir, "sample_export.csv")
        
        result = self.data_loader.export_sample_data(temp_file)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(temp_file))
        
        # Verify the exported file has content
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('age', content)
            self.assertIn('gender', content)
            self.assertIn('region', content)
    
    def test_load_csv_integration(self):
        """Test complete CSV loading integration."""
        temp_file = os.path.join(self.temp_dir, "integration_test.csv")
        
        # Create test CSV data
        test_data = [
            {'age': '25', 'gender': 'Male', 'region': 'North', 'satisfaction': 'High'},
            {'age': '30', 'gender': 'Female', 'region': 'South', 'satisfaction': 'Medium'},
            {'age': '35', 'gender': 'Male', 'region': 'East', 'satisfaction': 'Low'}
        ]
        
        with open(temp_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['age', 'gender', 'region', 'satisfaction'])
            writer.writeheader()
            writer.writerows(test_data)
        
        result = self.data_loader.load_csv(temp_file)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['age'], '25')
        self.assertEqual(result[0]['gender'], 'Male')


if __name__ == '__main__':
    unittest.main() 