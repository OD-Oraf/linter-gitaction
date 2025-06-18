# Documentation and API Validation Action

A GitHub Action that uses [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) to lint markdown files and [Spectral](https://github.com/stoplightio/spectral) to validate OpenAPI specifications in your repository.

## Features

- ✅ Lints markdown files using markdownlint-cli
- 🔍 Validates OpenAPI specifications using Spectral
- 📁 Configurable documentation directory
- 📄 Validates OpenAPI file existence and format
- 🔧 Sensible default configurations for both tools
- 📊 Detailed logging and summary output
- 📋 Generates validation reports in JSON and Markdown formats

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `documentation-directory` | Directory containing markdown files to lint | Yes | `./documentation` |
| `openapi-file` | Path to OpenAPI specification file | Yes | `./openapi.yaml` |

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
```

### Advanced Usage with Report Upload

```yaml
name: Documentation Quality Check

on:
  push:
    paths:
      - 'docs/**/*.md'
      - 'openapi.yaml'

jobs:
  validate-docs-and-api:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        
      - name: Validate documentation and API
        uses: ./actions
        with:
          documentation-directory: './docs'
          openapi-file: './openapi.yaml'
          
      - name: Upload validation reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: validation-reports
          path: |
            .markdownlint.json
            .spectral.yml
            spectral-report.json
            spectral-report.md
          retention-days: 30
```

## Tool Configurations

### Markdownlint Configuration

The action creates a `.markdownlint.json` configuration file with the following rules:

- **Line length**: Maximum 120 characters (excluding code blocks and tables)
- **HTML elements**: Allows `<br>`, `<sub>`, and `<sup>` tags
- **First line heading**: Disabled (MD041)
- **Default rules**: All other markdownlint rules are enabled

### Spectral Configuration

The action creates a `.spectral.yml` configuration file with enhanced OpenAPI validation rules:

- **Required fields**: Contact info, descriptions, and licenses
- **Operations**: Must have descriptions, unique operation IDs, and defined tags
- **Parameters**: Must have descriptions and proper validation
- **Security**: Security schemes must be properly defined
- **Naming**: Schema names should follow PascalCase convention
- **Servers**: API servers must be properly configured

## What Gets Validated

### Markdown Files
1. **Input Validation**: Verifies that the documentation directory exists
2. **Markdown Linting**: Runs markdownlint on all `.md` files in the specified directory
3. **Summary Report**: Provides a summary of linting results

### OpenAPI Specification
1. **File Validation**: Verifies the OpenAPI file exists and is not empty
2. **Format Validation**: Checks for valid YAML/JSON format
3. **Spectral Linting**: Validates against OpenAPI standards and best practices
4. **Structure Validation**: Performs additional structural checks
5. **Report Generation**: Creates detailed validation reports

## Generated Reports

The action generates several reports:

- **`.markdownlint.json`**: Markdownlint configuration used
- **`spectral-report.json`**: Machine-readable Spectral validation results
- **`spectral-report.md`**: Human-readable Spectral validation report with issue breakdown

## Error Handling

The action will fail if:
- The documentation directory doesn't exist
- The OpenAPI file doesn't exist or is empty
- Any markdown files fail linting rules
- The OpenAPI specification has structural errors (severity: error)
- Spectral validation finds critical issues

Warnings and informational messages will be reported but won't fail the action.

## Requirements

- Node.js 18+ (automatically installed by the action)
- Ubuntu runner (recommended)
- `jq` for JSON processing (available on GitHub runners)

## Spectral Rules Applied

The action applies comprehensive OpenAPI validation rules including:

- **info-contact**: API must have contact information
- **info-description**: API must have a description
- **operation-description**: All operations must have descriptions
- **operation-operationId-unique**: Operation IDs must be unique
- **path-keys-no-trailing-slash**: Paths should not have trailing slashes
- **oas3-api-servers**: OpenAPI 3.x must define servers
- **oas3-operation-security-defined**: Security requirements must be defined

## Contributing

Feel free to submit issues and enhancement requests!
