# Documentation and API Validation Action

A comprehensive GitHub Action that validates documentation, API specifications, and data structures using industry-standard tools. Provides detailed reporting and error analysis for maintaining high-quality project documentation and APIs.

## Features

- **Markdown Linting**: Uses [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) to ensure consistent markdown formatting
- **OpenAPI Validation**: Uses [Spectral](https://github.com/stoplightio/spectral) to validate OpenAPI specifications
- **JSON Schema Validation**: Uses Python-based validator with [jsonschema](https://python-jsonschema.readthedocs.io/) for robust validation
- **Enhanced Reporting**: Generates comprehensive GitHub Step Summaries with detailed error analysis
- **Structured Error Output**: Provides actionable feedback with tagKey context and allowed values
- **Configurable Paths**: Flexible input parameters for different project structures
- **Sensible Defaults**: Works out-of-the-box with minimal configuration
- **Multiple Output Formats**: Generates JSON, Markdown, and text reports
- **Python Integration**: Automated Python environment setup with virtual environments

## Validation Components

### 1. Markdown Linting
- Validates markdown files for consistent formatting
- Configurable rules via `.markdownlint.json`
- Reports syntax errors, style issues, and formatting problems
- Generates detailed error reports with line numbers and rule violations

### 2. OpenAPI Validation
- Validates OpenAPI 3.x specifications
- Uses Spectral ruleset (`.spectral.yaml`)
- Checks for API design best practices
- Reports errors, warnings, info, and hints by severity
- Provides structured JSON output for programmatic processing

### 3. JSON Schema Validation
- **Python-based validator** with enhanced error reporting
- Validates JSON files against custom schemas with `$defs` and `$ref` support
- **TagKey-aware validation** for structured data with clear context
- **Consolidated error reporting** - one error per tagKey to avoid duplicates
- Shows **invalid values** and **all allowed values** for easy correction
- Supports both **text and JSON output formats**
- **Virtual environment isolation** for reliable dependency management

## Technical Architecture

### Environment Setup
- **Node.js 18**: For markdown and OpenAPI validation tools
- **Python 3.9**: For JSON schema validation with virtual environment
- **Automated dependency management**: Installs required packages automatically
- **Tool verification**: Confirms all tools are properly installed

### Validation Pipeline
1. **Environment Setup**: Installs Node.js and Python tools
2. **Markdown Validation**: Lints documentation files
3. **Categories Validation**: Python-based JSON schema validation
4. **OpenAPI Validation**: Spectral-based API specification validation
5. **Report Generation**: Creates comprehensive GitHub Step Summary
6. **Final Check**: Aggregates all errors and determines build status

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
            categories-errors.json
            validation-errors.md
          retention-days: 30
```

## Output Reports

The action generates several types of reports:

### GitHub Step Summary
- **Validation Summary Table**: At-a-glance status of all components
- **Markdown Details**: File counts, tool info, and results
- **OpenAPI Details**: Issue breakdown by severity with descriptions
- **Categories Details**: Schema validation with structured error tables
- **Error Details**: Consolidated error information when validation fails
- **Generated Artifacts**: List of available report files
- **Next Steps**: Component-specific guidance for fixing issues

### Validation Reports
- `spectral-report.json` - Machine-readable OpenAPI validation results
- `spectral-report.md` - Human-readable OpenAPI validation report
- `categories-errors.json` - Structured JSON schema validation errors from Python validator
- `validation-errors.md` - Consolidated error log with detailed information

### Error Table Format (Categories Validation)
When categories validation fails, you'll see a structured table with tagKey context:

| TagKey | Invalid Value | Allowed Values |
|--------|---------------|----------------|
| **Owning Business Group** | `"customer experience"` | Global, Service, Customer Experience, Engineering, Product, Marketing, Sales, Operations, Finance, Human Resources |
| **Data Classification** | `"DCL5"` | DCL1, DCL2, DCL3, DCL4 |

**Example JSON Output:**
```json
{
  "valid": false,
  "errors": [
    {
      "tagKey": "Owning Business Group",
      "invalidValues": ["customer experience"],
      "allowedValues": ["Global", "Service", "Customer Experience", "Engineering", "Product", "Marketing", "Sales", "Operations", "Finance", "Human Resources"]
    }
  ],
  "summary": "Found 1 validation error(s)"
}
```

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
The schema now uses `$defs` and `$ref` for maintainable enum definitions:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Categories",
  "type": "array",
  "$defs": {
    "owningBusinessGroupValues": {
      "enum": ["Global", "Service", "Customer Experience", "Engineering", "Product", "Marketing", "Sales", "Operations", "Finance", "Human Resources"]
    },
    "dataClassificationValues": {
      "enum": ["DCL1", "DCL2", "DCL3", "DCL4"]
    },
    "stringOrArrayValue": {
      "oneOf": [
        {"type": "string"},
        {"type": "array", "items": {"type": "string"}}
      ]
    }
  },
  "items": {
    "type": "object",
    "properties": {
      "tagKey": {
        "type": "string",
        "enum": ["Owning Business Group", "Data Classification"]
      },
      "value": {
        "$ref": "#/$defs/stringOrArrayValue"
      }
    },
    "required": ["tagKey", "value"],
    "additionalProperties": false
  }
}
```

## Project Structure

```
├── actions/
│   ├── action.yaml                    # Main composite GitHub Action
│   ├── README.md                      # Action-specific documentation
│   ├── categories-config/
│   │   └── categories-schema.json     # JSON schema for categories validation
│   ├── api-spec-config/
│   │   └── .spectral.yaml            # Spectral rules for OpenAPI validation
│   ├── documentation-config/
│   │   └── .markdownlint.json        # Markdownlint configuration
│   └── local-development/
│       ├── validate_categories.py     # Python validator script
│       ├── requirements.txt           # Python dependencies
│       ├── package.json              # Development scripts
│       └── DEVELOPMENT.md            # Development guide
├── categories.json                    # Sample categories data
├── openapi.yaml                      # Sample OpenAPI specification
├── documentation/                     # Sample markdown files
│   └── *.md
└── README.md                         # This file
```

## Troubleshooting

### Common Issues

**Python Environment Issues**
```bash
# If virtual environment creation fails
python3 -m pip install --upgrade pip
python3 -m venv .venv --clear

# If jsonschema installation fails
pip install --upgrade setuptools wheel
pip install jsonschema==4.21.1
```

**Categories Validation Errors**
- Check that tagKey values match exactly (case-sensitive)
- Ensure enum values are spelled correctly
- Verify JSON syntax is valid
- Use `--json` flag for detailed error information

**OpenAPI Validation Issues**
- Ensure OpenAPI file is valid YAML/JSON
- Check that all referenced components are defined
- Verify API version is OpenAPI 3.x

**Markdown Linting Problems**
- Check `.markdownlint.json` configuration
- Ensure markdown files use consistent formatting
- Review line length and heading structure

### Debug Mode

For detailed debugging information:

```bash
# Run with verbose output
cd actions/local-development
source .venv/bin/activate
python3 validate_categories.py ../../categories.json ../categories-config/categories-schema.json --json | jq '.'
```

## Contributing

We welcome contributions! Here's how you can help:

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Include sample files that reproduce the issue
- Provide error messages and expected behavior

### Development Guidelines
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation for any changes
- Test locally before submitting PRs

### Areas for Enhancement
- Additional validation rules for categories schema
- Support for more file formats
- Performance optimizations
- Enhanced error reporting
- Integration with other CI/CD platforms

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) for markdown validation
- [Spectral](https://github.com/stoplightio/spectral) for OpenAPI validation
- [jsonschema](https://python-jsonschema.readthedocs.io/) for JSON schema validation
- GitHub Actions team for the composite action framework