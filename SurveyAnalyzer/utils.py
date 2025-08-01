#!/usr/bin/env python3
"""
Utilities Module
Description: Provides utility functions for the Survey Data Analyzer CLI,
including display formatting, input validation, and common operations.
"""

import os
import sys
from typing import List, Dict, Any, Optional


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"TARGET: {title}")
    print("=" * 60)


def print_menu(options: List[str]):
    """Print a numbered menu."""
    print("\nAvailable Options:")
    for i, option in enumerate(options, 1):
        print(f"   {i}. {option}")


def print_success(message: str):
    """Print a success message."""
    print(f"SUCCESS: {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"ERROR: {message}")


def print_warning(message: str):
    """Print a warning message."""
    print(f"WARNING: {message}")


def print_info(message: str):
    """Print an info message."""
    print(f"INFO: {message}")


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path exists and is accessible.
    
    Args:
        file_path: Path to the file to validate
        
    Returns:
        True if file is valid, False otherwise
    """
    if not file_path or not isinstance(file_path, str):
        return False
    
    file_path = file_path.strip()
    if not file_path:
        return False
    
    return os.path.exists(file_path) and os.path.isfile(file_path)


def validate_csv_file(file_path: str) -> bool:
    """
    Validate if a file is a valid CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        True if file is a valid CSV, False otherwise
    """
    if not validate_file_path(file_path):
        return False
    
    # Check file extension
    if not file_path.lower().endswith('.csv'):
        return False
    
    # Check file size (not empty and not too large)
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            return False
    except OSError:
        return False
    
    return True


def format_number(number: float, decimal_places: int = 2) -> str:
    """
    Format a number with specified decimal places.
    
    Args:
        number: Number to format
        decimal_places: Number of decimal places to show
        
    Returns:
        Formatted number string
    """
    return f"{number:.{decimal_places}f}"


def format_percentage(value: float, total: float) -> str:
    """
    Format a percentage value.
    
    Args:
        value: The value to calculate percentage for
        total: The total value
        
    Returns:
        Formatted percentage string
    """
    if total == 0:
        return "0.0%"
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"


def format_table(data: List[List[str]], headers: List[str] = None) -> str:
    """
    Format data as a table.
    
    Args:
        data: List of rows, each row is a list of values
        headers: Optional list of column headers
        
    Returns:
        Formatted table string
    """
    if not data:
        return "No data to display"
    
    # Determine column widths
    if headers:
        all_rows = [headers] + data
    else:
        all_rows = data
    
    col_widths = []
    for col in range(len(all_rows[0])):
        max_width = max(len(str(row[col])) for row in all_rows)
        col_widths.append(max_width)
    
    # Build table
    lines = []
    
    # Header
    if headers:
        header_line = " | ".join(f"{headers[i]:<{col_widths[i]}}" for i in range(len(headers)))
        lines.append(header_line)
        lines.append("-" * len(header_line))
    
    # Data rows
    for row in data:
        row_line = " | ".join(f"{row[i]:<{col_widths[i]}}" for i in range(len(row)))
        lines.append(row_line)
    
    return "\n".join(lines)


def get_user_input(prompt: str, default: str = None) -> str:
    """
    Get user input with optional default value.
    
    Args:
        prompt: Input prompt to display
        default: Optional default value
        
    Returns:
        User input string
    """
    if default:
        user_input = input(f"{prompt} (default: {default}): ").strip()
        return user_input if user_input else default
    else:
        return input(f"{prompt}: ").strip()


def confirm_action(prompt: str = "Are you sure?") -> bool:
    """
    Get user confirmation for an action.
    
    Args:
        prompt: Confirmation prompt
        
    Returns:
        True if user confirms, False otherwise
    """
    response = input(f"{prompt} (y/N): ").strip().lower()
    return response in ['y', 'yes']


def display_progress(current: int, total: int, description: str = "Processing"):
    """
    Display a progress bar.
    
    Args:
        current: Current progress value
        total: Total value
        description: Description of the operation
    """
    if total == 0:
        return
    
    percentage = (current / total) * 100
    bar_length = 30
    filled_length = int(bar_length * current // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f"\r{description}: |{bar}| {percentage:.1f}% ({current}/{total})", end='')
    
    if current == total:
        print()  # New line when complete


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator: The numerator
        denominator: The denominator
        default: Default value if division by zero
        
    Returns:
        Result of division or default value
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ValueError):
        return default


def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def validate_age(age_str: str) -> bool:
    """
    Validate if a string represents a valid age.
    
    Args:
        age_str: String to validate as age
        
    Returns:
        True if valid age, False otherwise
    """
    try:
        age = int(age_str)
        return 0 <= age <= 120
    except (ValueError, TypeError):
        return False


def validate_gender(gender_str: str) -> bool:
    """
    Validate if a string represents a valid gender.
    
    Args:
        gender_str: String to validate as gender
        
    Returns:
        True if valid gender, False otherwise
    """
    if not gender_str:
        return False
    
    valid_genders = [
        'male', 'female', 'm', 'f', 'other', 'prefer not to say',
        'Male', 'Female', 'M', 'F', 'Other', 'Prefer not to say'
    ]
    
    return gender_str.strip() in valid_genders


def normalize_text(text: str) -> str:
    """
    Normalize text by removing extra whitespace and converting to lowercase.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and convert to lowercase
    normalized = " ".join(text.strip().split()).lower()
    return normalized


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count words in
        
    Returns:
        Number of words
    """
    if not text:
        return 0
    
    return len(text.split())


def get_file_extension(file_path: str) -> str:
    """
    Get file extension from file path.
    
    Args:
        file_path: Path to file
        
    Returns:
        File extension (including dot)
    """
    return os.path.splitext(file_path)[1].lower()


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to directory
        
    Returns:
        True if directory exists or was created, False otherwise
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        return True
    except Exception:
        return False


def is_valid_filename(filename: str) -> bool:
    """
    Check if a filename is valid.
    
    Args:
        filename: Filename to validate
        
    Returns:
        True if valid filename, False otherwise
    """
    if not filename:
        return False
    
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?*'
    return not any(char in filename for char in invalid_chars)


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"


def print_separator(char: str = "-", length: int = 60):
    """Print a separator line."""
    print(char * length)


def print_bullet_list(items: List[str], indent: int = 2):
    """
    Print a bullet list.
    
    Args:
        items: List of items to print
        indent: Number of spaces to indent
    """
    indent_str = " " * indent
    for item in items:
        print(f"{indent_str}• {item}")


def print_key_value_pairs(data: Dict[str, Any], indent: int = 2):
    """
    Print key-value pairs in a formatted way.
    
    Args:
        data: Dictionary of key-value pairs
        indent: Number of spaces to indent
    """
    indent_str = " " * indent
    for key, value in data.items():
        print(f"{indent_str}{key}: {value}") 