# Linter GitHub Action

A comprehensive GitHub Action for validating documentation, API specifications, and data structures. This action provides professional-grade validation with detailed reporting and error analysis to maintain high-quality project standards.

## Overview

This repository contains a composite GitHub Action that integrates multiple industry-standard validation tools:

- Markdown Linting - Ensures consistent documentation formatting
- OpenAPI Validation - Validates API specifications against best practices  
- JSON Schema Validation - Validates data structures with detailed error reporting
- Enhanced Reporting - Provides comprehensive GitHub Step Summaries

## Key Features

### Multi-Tool Integration
- [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) for markdown consistency
- [Spectral](https://github.com/stoplightio/spectral) for OpenAPI validation
- [AJV CLI](https://github.com/ajv-validator/ajv-cli) for JSON schema validation

### Advanced Reporting
- Structured Error Tables with field-level details
- GitHub Step Summaries with validation status
- Multiple Output Formats (JSON, Markdown, Text)
- Actionable Feedback showing exactly what to fix

### Professional Error Handling
- Graceful Failures - continues validation even when components fail
- Detailed Logging - captures specific error details
- File Existence Checks - handles missing files gracefully
- Comprehensive Coverage - validates entire project structure

## Quick Start

### Basic Usage

```yaml
name: Documentation and API Validation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Validation
      - uses: ./actions
        with:
          documentation-directory: './documentation'
          openapi-file: './openapi.yaml'
          categories-file: './categories.json'
```

### Advanced Usage with Artifacts

```yaml
name: Quality Assurance

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Comprehensive Validation
        uses: ./actions
        with:
          documentation-directory: './docs'
          openapi-file: './api/openapi.yaml'
          categories-file: './config/categories.json'
      
      - name: Upload Validation Reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-reports
          path: |
            spectral-report.json
            spectral-report.md
            ajv-errors.json
            validation-errors.md
          retention-days: 30
```

## Validation Components

### 1. Markdown Linting
- Validates all `.md` files in specified directory
- Configurable rules via `.markdownlint.json`
- Reports formatting issues, style problems, and syntax errors
- Provides file-by-file error breakdown

### 2. OpenAPI Validation  
- Validates OpenAPI 3.x specifications
- Uses Spectral with comprehensive ruleset
- Checks API design best practices
- Reports issues by severity (error, warning, info, hint)
- Generates detailed validation reports

### 3. JSON Schema Validation
- Validates JSON files against custom schemas
- Supports complex conditional validation rules
- Provides structured error tables with:
  - Field Path - exact location of error
  - Issue Description - what went wrong
  - Expected Values - what was expected
  - Actual Values - what was found

## Sample Output

### GitHub Step Summary
```
Validation Summary
┌─────────────────────┬────────┬─────────┬──────────┐
│ Component           │ Status │ Files   │ Issues   │
├─────────────────────┼────────┼─────────┼──────────┤
│ Markdown Linting    │ Pass   │ 5 files │ 0 errors │
│ OpenAPI Validation  │ Pass   │ 1 file  │ 0 errors │
│ JSON Schema         │ Fail   │ 1 file  │ 2 errors │
└─────────────────────┴────────┴─────────┴──────────┘

JSON Schema Validation Errors
┌──────────┬─────────────────────────────────┬─────────────────┬─────────┐
│ Field    │ Issue                           │ Expected        │ Actual  │
├──────────┼─────────────────────────────────┼─────────────────┼─────────┤
│ /1/value │ must be equal to allowed values │ DCL1,DCL2,DCL3  │ ""      │
│ /2/tagKey│ must be equal to allowed values │ Environment,App │ "Invalid"│
└──────────┴─────────────────────────────────┴─────────────────┴─────────┘
```

## Configuration

### Input Parameters

| Parameter | Description | Default | Required |
|-----------|-------------|---------|----------|
| `documentation-directory` | Directory containing markdown files | `./documentation` | No |
| `openapi-file` | Path to OpenAPI specification | `./openapi.yaml` | No |
| `categories-file` | Path to categories JSON file | `./categories.json` | No |

### Configuration Files

The action supports standard configuration files:

- `.markdownlint.json` - Markdown linting rules
- `.spectral.yaml` - OpenAPI validation rules  
- `categories-schema.json` - JSON schema for categories validation

## Generated Reports

### Artifacts Created
- `spectral-report.json` - Machine-readable OpenAPI results
- `spectral-report.md` - Human-readable OpenAPI report
- `ajv-errors.json` - Structured JSON schema errors
- `validation-errors.md` - Consolidated error log

### GitHub Step Summary Sections
- Validation Summary Table - Overall status at-a-glance
- Markdown Linting Results - File counts and error details
- OpenAPI Validation Results - Issue breakdown by severity
- JSON Schema Validation Results - Structured error tables
- Error Details - Consolidated failure information
- Generated Artifacts - Available report files
- Next Steps - Component-specific guidance

## Development

### Project Structure
```
├── actions/
│   ├── action.yaml          # Main composite action
│   └── README.md           # Action documentation
├── documentation/          # Sample markdown files
├── categories.json         # Sample categories data
├── categories-schema.json  # JSON schema for validation
├── openapi.yaml           # Sample OpenAPI specification
└── README.md              # This file
```

### Tool Versions
- Node.js: 18.x
- markdownlint-cli: Latest
- @stoplight/spectral-cli: Latest
- ajv-cli: Latest

## Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

### Areas for Enhancement
- Additional validation tools integration
- Custom rule configurations
- Performance optimizations
- Extended reporting formats
- Integration with other CI/CD platforms

## License