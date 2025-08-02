# Survey Data Analyzer and Response Processor

**A comprehensive Command Line Interface (CLI) tool for analyzing survey responses from CSV files**

## Project Overview

The Survey Data Analyzer is a modular Python CLI application designed to perform structured statistical analysis, basic text sentiment analysis, identify response patterns, and generate readable reports from survey data stored in CSV format.

### Key Features

- **CSV Input Handling**: Load and validate structured survey data from CSV files
- **Survey Summary**: Calculate response counts, percentages, and demographic breakdowns
- **Statistical Analysis**: Perform cross-tabulation and Chi-Square tests
- **Sentiment Analysis**: Analyze text responses using keyword-based sentiment scoring
- **Pattern Recognition**: Identify correlations and trends between survey responses
- **Report Generation**: Create comprehensive analysis reports in text format

## Project Structure

```
SurveyAnalyzer/
├── main.py                    # CLI menu and application entry point
├── data_loader.py            # CSV loading and validation
├── survey_summary.py         # Response counts and demographics
├── stats_analyzer.py         # Cross-tabulation and chi-square tests
├── sentiment_analyzer.py     # Text sentiment analysis
├── pattern_detector.py       # Pattern correlation detection
├── report_generator.py       # Report generation and file output
├── utils.py                  # Utility functions and helpers
├── sample_survey.csv         # Example input file
├── requirements.txt          # Project dependencies (stdlib only)
├── README.md                 # This documentation
└── test/                     # Unit tests
    ├── test_data_loader.py
    ├── test_stats_analyzer.py
    └── test_sentiment_analyzer.py
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- No external dependencies required (uses only standard library)

### Installation

1. Clone or download the project files
2. Navigate to the SurveyAnalyzer directory
3. Run the application:

```bash
python main.py
```

### Usage Example

1. **Load Survey Data**: Choose option 1 and provide the path to your CSV file
2. **View Summary Statistics**: Choose option 2 to see demographic breakdowns
3. **Analyze Sentiment**: Choose option 3 for text sentiment analysis
4. **Cross-tabulate Results**: Choose option 4 for statistical analysis
5. **Detect Patterns**: Choose option 5 to find correlations
6. **Generate Report**: Choose option 6 to create a comprehensive report

## Sample Data

The project includes `sample_survey.csv` with example data containing:
- Age, gender, region, education demographics
- Satisfaction ratings
- Text feedback responses
- Recommendation preferences

## Technical Requirements

### Python Version
- **Minimum**: Python 3.8
- **Recommended**: Python 3.9+

### Standard Library Modules Used
- `csv`: CSV file handling
- `re`: Regular expressions for text processing
- `math`: Mathematical calculations
- `statistics`: Statistical functions
- `os`: Operating system interface
- `sys`: System-specific parameters
- `datetime`: Date and time handling
- `itertools`: Iterator building blocks
- `collections`: Specialized container datatypes
- `typing`: Type hints support

### Object-Oriented Design
- **Class Hierarchies**: Modular class structure for each component
- **Inheritance**: Base classes for common functionality
- **Polymorphism**: Flexible method implementations

## User Guide

### 1. Loading Survey Data

The application accepts CSV files with the following requirements:
- **File Format**: Comma-separated values (CSV)
- **Encoding**: UTF-8, Latin-1, or CP1252
- **Size Limit**: Maximum 50MB
- **Required Columns**: At least 2 columns with valid data

### 2. Survey Summary Analysis

View comprehensive statistics including:
- Total response count and response rate
- Demographic breakdowns (age, gender, region, education)
- Response distributions for each question
- Data quality metrics

### 3. Sentiment Analysis

Analyze text responses using:
- **Positive Keywords**: excellent, amazing, great, good, etc.
- **Negative Keywords**: terrible, awful, bad, poor, etc.
            - **Negation Handling**: "not good" - negative sentiment
            - **Intensifier Recognition**: "very good" - amplified positive

### 4. Statistical Analysis

Perform advanced statistical tests:
- **Cross-tabulation**: Compare responses across different questions
- **Chi-Square Tests**: Determine statistical significance
- **Correlation Analysis**: Find relationships between variables

### 5. Pattern Detection

Identify meaningful patterns:
- **Demographic Patterns**: Age, gender, regional differences
- **Response Correlations**: Related answers across questions
- **Combination Patterns**: Common response combinations
- **Outlier Detection**: Unusual or rare responses

### 6. Report Generation

Generate comprehensive reports including:
- Executive summary
- Demographic analysis
- Sentiment analysis results
- Pattern detection findings
- Statistical insights
- Key findings and recommendations

## Testing

### Running Tests

```bash
# Run all tests
python -m unittest discover test/

# Run specific test file
python -m unittest test.test_data_loader

# Run with verbose output
python -m unittest discover test/ -v
```

### Test Coverage

- **Data Loading**: File validation, encoding detection, data cleaning
- **Statistical Analysis**: Cross-tabulation, chi-square calculations
- **Sentiment Analysis**: Keyword matching, negation handling
- **Pattern Detection**: Correlation analysis, demographic patterns
- **Report Generation**: File output, formatting

## Technical Documentation

### Core Classes

#### DataLoader
- **Purpose**: Handle CSV file loading and validation
- **Key Methods**: `load_csv()`, `_validate_file()`, `_clean_and_validate_data()`
- **Features**: Multi-encoding support, delimiter detection, data cleaning

#### SurveySummary
- **Purpose**: Generate summary statistics and demographic breakdowns
- **Key Methods**: `generate_summary()`, `_analyze_demographics()`, `get_age_distribution()`
- **Features**: Response counting, percentage calculations, trend analysis

#### StatsAnalyzer
- **Purpose**: Perform statistical analysis and hypothesis testing
- **Key Methods**: `cross_tabulate()`, `chi_square_test()`, `correlation_analysis()`
- **Features**: Cross-tabulation matrices, chi-square tests, correlation coefficients

#### SentimentAnalyzer
- **Purpose**: Analyze text sentiment using keyword-based approach
- **Key Methods**: `analyze_text()`, `analyze_column()`, `_clean_text()`
- **Features**: Keyword dictionaries, negation handling, intensifier recognition

#### PatternDetector
- **Purpose**: Identify patterns and correlations in survey responses
- **Key Methods**: `find_patterns()`, `_analyze_age_patterns()`, `_find_correlation_patterns()`
- **Features**: Demographic analysis, correlation detection, outlier identification

#### ReportGenerator
- **Purpose**: Generate comprehensive analysis reports
- **Key Methods**: `generate_report()`, `_build_report_content()`, `_write_report_to_file()`
- **Features**: Structured reports, multiple sections, file output

### Error Handling

The application implements robust error handling:
- **File Validation**: Check file existence, size, and format
- **Data Validation**: Validate age ranges, gender values, required fields
- **Graceful Degradation**: Continue processing even with partial data
- **User-Friendly Messages**: Clear error messages with suggestions

### Performance Considerations

- **Memory Efficient**: Process data in chunks for large files
- **Fast Processing**: Optimized algorithms for statistical calculations
- **Responsive UI**: Non-blocking operations with progress indicators

## Educational Features

### Learning Objectives

This project demonstrates:
- **Modular Design**: Clean separation of concerns
- **Object-Oriented Programming**: Classes, inheritance, polymorphism
- **Error Handling**: Robust exception management
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Unit tests for all major components
- **CLI Design**: User-friendly command-line interface

### Code Quality

- **Readability**: Clear variable names and function purposes
- **Maintainability**: Modular structure for easy updates
- **Extensibility**: Easy to add new analysis features
- **Documentation**: Inline comments and comprehensive docstrings

## Contributing

### Development Guidelines

1. **Code Style**: Follow PEP 8 conventions
2. **Documentation**: Add docstrings for all functions and classes
3. **Testing**: Write unit tests for new features
4. **Error Handling**: Implement proper exception handling
5. **User Experience**: Ensure intuitive CLI interface

### Adding New Features

1. Create new module in appropriate directory
2. Implement class with clear interface
3. Add comprehensive unit tests
4. Update main.py to integrate new feature
5. Update documentation

## License

This project is designed for educational purposes. Feel free to use, modify, and distribute for learning and teaching.

## Author

**Student Developer** - Survey Data Analyzer Project

---

**Note**: This application uses only Python standard library modules, making it easy to run without external dependencies. Perfect for educational environments and learning Python programming concepts. 