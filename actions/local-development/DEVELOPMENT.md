# Development Setup

This guide helps you set up the same linting tools locally that are used in the GitHub Action.

## Installation Options

### Option A: Using npm (Recommended)
```bash
npm install
```

### Option B: Global Installation
```bash
npm install -g markdownlint-cli @stoplight/spectral-cli ajv-cli
```

## Running Linters

### With npm scripts (if using Option A):
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

### With global tools (if using Option B):

#### Using Local Configurations:
```bash
# Lint markdown
markdownlint documentation/**/*.md --config actions/documentation/.markdownlint.json

# Lint OpenAPI (if actions/api-spec/.spectral.yaml exists)
spectral lint --ruleset actions/api-spec/.spectral.yaml

# Validate JSON schema
ajv validate --spec=draft7 --errors=json -s actions/categories/categories-schema.json -d categories.json

# Fix markdown automatically
markdownlint documentation/**/*.md --config actions/documentation/.markdownlint.json --fix
```

#### Using Remote Configurations:
```bash
# Lint markdown with remote config
markdownlint documentation/**/*.md --config https://raw.githubusercontent.com/your-org/shared-configs/main/markdownlint/.markdownlint.json

# Lint OpenAPI with remote ruleset
spectral lint openapi.yaml --ruleset https://raw.githubusercontent.com/your-org/shared-configs/main/spectral/.spectral.yaml

# Validate JSON schema with remote schema
ajv validate --spec=draft7 --errors=json -s https://raw.githubusercontent.com/your-org/shared-configs/main/schemas/categories-schema.json -d categories.json

# Fix markdown with remote config
markdownlint documentation/**/*.md --config https://raw.githubusercontent.com/your-org/shared-configs/main/markdownlint/.markdownlint.json --fix
```

#### Using Cached Remote Configurations:
```bash
# Download and cache remote configs (run once)
mkdir -p .cache/remote-configs
curl -o .cache/remote-configs/.markdownlint.json https://raw.githubusercontent.com/your-org/shared-configs/main/markdownlint/.markdownlint.json
curl -o .cache/remote-configs/.spectral.yaml https://raw.githubusercontent.com/your-org/shared-configs/main/spectral/.spectral.yaml
curl -o .cache/remote-configs/categories-schema.json https://raw.githubusercontent.com/your-org/shared-configs/main/schemas/categories-schema.json

# Use cached configs (faster, works offline)
markdownlint documentation/**/*.md --config .cache/remote-configs/.markdownlint.json
spectral lint openapi.yaml --ruleset .cache/remote-configs/.spectral.yaml
ajv validate --spec=draft7 -s .cache/remote-configs/categories-schema.json -d categories.json
```

## IDE Integration

### VS Code
1. Install recommended extensions (prompted automatically)
2. Settings are pre-configured in `.vscode/settings.json`
3. Linting will work automatically with real-time feedback

**For remote configs in VS Code:**
```json
{
  "markdownlint.config": "https://raw.githubusercontent.com/your-org/shared-configs/main/markdownlint/.markdownlint.json",
  "spectral.rulesetFile": "https://raw.githubusercontent.com/your-org/shared-configs/main/spectral/.spectral.yaml",
  "json.schemas": [
    {
      "fileMatch": ["categories.json"],
      "url": "https://raw.githubusercontent.com/your-org/shared-configs/main/schemas/categories-schema.json"
    }
  ]
}
```

### Other IDEs

#### IntelliJ/WebStorm
- Install plugins: Markdown, YAML/Ansible Support, JSON Schema
- Configure markdownlint to use remote URL: `https://raw.githubusercontent.com/your-org/shared-configs/main/markdownlint/.markdownlint.json`
- Set JSON schema mapping for `categories.json` → `https://raw.githubusercontent.com/your-org/shared-configs/main/schemas/categories-schema.json`

#### Vim/Neovim
- Use ALE or similar linting plugin
- Configure remote config URLs in your plugin settings

## Configuration Files

### Local Configurations:
- **Markdown**: `actions/documentation/.markdownlint.json`
- **OpenAPI**: `actions/api-spec/.spectral.yaml`
- **JSON Schema**: `actions/categories/categories-schema.json`

### Remote Configurations (Example URLs):
- **Markdown**: `https://raw.githubusercontent.com/your-org/shared-configs/main/markdownlint/.markdownlint.json`
- **OpenAPI**: `https://raw.githubusercontent.com/your-org/shared-configs/main/spectral/.spectral.yaml`
- **JSON Schema**: `https://raw.githubusercontent.com/your-org/shared-configs/main/schemas/categories-schema.json`

## Setting Up Remote Configuration Repository

Create a shared configuration repository with this structure:

```
your-org/shared-configs/
├── markdownlint/
│   ├── .markdownlint.json          # Standard rules
│   ├── .markdownlint-strict.json   # Strict rules
│   └── .markdownlint-docs.json     # Documentation-specific
├── spectral/
│   ├── .spectral.yaml              # Standard OpenAPI rules
│   ├── .spectral-strict.yaml       # Strict API rules
│   └── .spectral-internal.yaml     # Internal API rules
├── schemas/
│   ├── categories-schema.json
│   ├── config-schema.json
│   └── api-metadata-schema.json
└── README.md
```

## Pre-commit Hooks (Optional)

Install pre-commit to run linters automatically:

```bash
pip install pre-commit
pre-commit install
```

**Using remote configs in pre-commit:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.37.0
    hooks:
      - id: markdownlint
        args: ['--config', 'https://raw.githubusercontent.com/your-org/shared-configs/main/markdownlint/.markdownlint.json']
```

Now linters run automatically on every commit with centralized rules!
