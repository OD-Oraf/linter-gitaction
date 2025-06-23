# Development Setup

This guide helps you set up the same linting tools locally that are used in the GitHub Action.

## Quick Setup

### 1. Install Dependencies
```bash
npm install
```

### 2. Run Linters
```bash
# Lint all files
npm run lint:all

# Individual linters
npm run lint:markdown
npm run lint:openapi
npm run lint:json

# Fix markdown issues automatically
npm run fix:markdown
```

## IDE Integration

### VS Code
1. Install recommended extensions (prompted automatically)
2. Settings are pre-configured in `.vscode/settings.json`
3. Linting will work automatically with real-time feedback

### Other IDEs

#### IntelliJ/WebStorm
- Install plugins: Markdown, YAML/Ansible Support, JSON Schema
- Configure markdownlint to use `actions/documentation/.markdownlint.json`
- Set JSON schema mapping for `categories.json` → `actions/categories/categories-schema.json`

#### Vim/Neovim
- Use ALE or similar linting plugin
- Configure paths to the same config files

## Configuration Files

- **Markdown**: `actions/documentation/.markdownlint.json`
- **OpenAPI**: `actions/api-spec/.spectral.yaml`
- **JSON Schema**: `actions/categories/categories-schema.json`

## Pre-commit Hooks (Optional)

Install pre-commit to run linters automatically:

```bash
pip install pre-commit
pre-commit install
```

Now linters run automatically on every commit!
