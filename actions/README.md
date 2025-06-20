# Documentation and API Validation Action

A comprehensive GitHub Action that validates documentation, API specifications, and data structures using industry-standard tools. Provides detailed reporting and error analysis for maintaining high-quality project documentation and APIs.

## Features

- 📝 **Markdown Linting**: Uses [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) to ensure consistent markdown formatting
- 🔍 **OpenAPI Validation**: Uses [Spectral](https://github.com/stoplightio/spectral) to validate OpenAPI specifications
- 📋 **JSON Schema Validation**: Uses [AJV CLI](https://github.com/ajv-validator/ajv-cli) to validate JSON files against schemas
- 📊 **Enhanced Reporting**: Generates comprehensive GitHub Step Summaries with detailed error analysis
- 🎯 **Structured Error Output**: Provides actionable feedback with field-level error details
- 📁 **Configurable Paths**: Flexible input parameters for different project structures
- 🔧 **Sensible Defaults**: Works out-of-the-box with minimal configuration
- 📄 **Multiple Output Formats**: Generates JSON, Markdown, and text reports

## Validation Components

### 1. Markdown Linting
- Validates markdown files for consistent formatting
- Configurable rules via `.markdownlint.json`
- Reports syntax errors, style issues, and formatting problems

### 2. OpenAPI Validation
- Validates OpenAPI 3.x specifications
- Uses Spectral ruleset (`.spectral.yaml`)
- Checks for API design best practices
- Reports errors, warnings, info, and hints by severity

### 3. JSON Schema Validation
- Validates JSON files against custom schemas
- Supports complex validation rules with conditional logic
- Provides detailed field-level error reporting
- Shows expected vs actual values for easy debugging

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `documentation-directory` | Directory containing markdown files to lint | No | `./documentation` |
| `openapi-file` | Path to OpenAPI specification file | No | `./openapi.yaml` |
| `categories-file` | Path to categories JSON file for schema validation | No | `./categories.json` |

## Usage

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
      - uses: ./actions
        with:
          documentation-directory: './docs'
          openapi-file: './api/openapi.yaml'
          categories-file: './config/categories.json'
```

### Advanced Usage with Report Upload

```yaml
name: Documentation Quality Check

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
      
      - name: Validate Documentation and APIs
        uses: ./actions
        with:
          documentation-directory: './documentation'
          openapi-file: './openapi.yaml'
          categories-file: './categories.json'
      
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

## Output Reports

The action generates several types of reports:

### GitHub Step Summary
- **📊 Validation Summary Table**: At-a-glance status of all components
- **📝 Markdown Details**: File counts, tool info, and results
- **🔍 OpenAPI Details**: Issue breakdown by severity with descriptions
- **📋 Categories Details**: Schema validation with structured error tables
- **🚨 Error Details**: Consolidated error information when validation fails
- **📄 Generated Artifacts**: List of available report files
- **🔧 Next Steps**: Component-specific guidance for fixing issues

### Validation Reports
- `spectral-report.json` - Machine-readable OpenAPI validation results
- `spectral-report.md` - Human-readable OpenAPI validation report
- `ajv-errors.json` - Structured JSON schema validation errors
- `validation-errors.md` - Consolidated error log with detailed information

### Error Table Format (JSON Schema)
When JSON schema validation fails, you'll see a structured table:

| Field | Issue | Expected | Actual |
|-------|-------|----------|--------|
| `/1/value` | must be equal to one of allowed values | DCL1, DCL2, DCL3, DCL4 | `""` |
| `/2/tagKey` | must be equal to one of allowed values | Environment, Application, Owner | `"InvalidKey"` |

## Configuration Files

### Markdownlint Configuration (`.markdownlint.json`)
```json
{
  "MD013": false,
  "MD033": false,
  "MD041": false
}
```

### Spectral Configuration (`.spectral.yaml`)
```yaml
extends: ["spectral:oas"]
rules:
  info-contact: error
  info-description: error
  operation-description: error
  operation-operationId-unique: error
  operation-parameters: error
  operation-tag-defined: error
```

### Categories Schema (`categories-schema.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Categories",
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "tagKey": {
        "type": "string",
        "enum": ["Environment", "Application", "Owner"]
      },
      "value": {
        "type": "string",
        "minLength": 1
      }
    },
    "required": ["tagKey", "value"],
    "additionalProperties": false
  }
}
```

## Default Spectral Rules

The action uses Spectral's OpenAPI ruleset with additional custom rules:

### Error Level Rules
- **info-contact**: API must have contact information
- **info-description**: API must have description
- **operation-description**: All operations must have descriptions
- **operation-operationId-unique**: Operation IDs must be unique
- **operation-parameters**: Parameters must be properly defined
- **operation-tag-defined**: All tags must be defined in the global tags list
- **oas3-operation-security-defined**: Security requirements must be defined

### Warning Level Rules
- **operation-tags**: Operations should have tags
- **openapi-tags**: Should define global tags
- **info-license**: Should include license information

## Error Handling

The action provides comprehensive error handling:

- **Graceful Failures**: Continues validation even when individual components fail
- **Detailed Logging**: Captures and reports specific error details
- **Structured Output**: Provides machine-readable and human-readable error formats
- **Actionable Feedback**: Shows exactly what needs to be fixed and where
- **File Existence Checks**: Handles missing files gracefully with clear messaging

## Tool Versions

- **Node.js**: 18.x
- **markdownlint-cli**: Latest
- **@stoplight/spectral-cli**: Latest  
- **ajv-cli**: Latest

## Contributing

Feel free to submit issues and enhancement requests!
