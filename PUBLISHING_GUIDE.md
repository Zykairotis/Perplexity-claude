# Publishing Guide for Perplexity MCP Server

This guide covers all the steps needed to publish this project to various platforms.

## Table of Contents

1. [Pre-Publishing Checklist](#pre-publishing-checklist)
2. [Publishing to GitHub](#publishing-to-github)
3. [Publishing to PyPI](#publishing-to-pypi)
4. [Publishing to Docker Hub](#publishing-to-docker-hub)
5. [Creating Releases](#creating-releases)
6. [Distribution Best Practices](#distribution-best-practices)

---

## Pre-Publishing Checklist

Before publishing, ensure you complete these tasks:

### 1. Clean Sensitive Data

```bash
# Remove sensitive files
rm -f cookies.json
rm -f .env
rm -f nohup.out
rm -rf __pycache__
rm -rf .venv
rm -rf logs/*
```

### 2. Update .gitignore

Ensure your `.gitignore` includes:

```gitignore
# Sensitive files
cookies.json
.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log
nohup.out

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/

# Temporary files
temp-test/
*.tmp
```

### 3. Add Required Files

- `README.md` ✅ (Already created)
- `LICENSE` (Choose appropriate license)
- `pyproject.toml` ✅ (Already created)
- `CHANGELOG.md` (Track version changes)

### 4. Update Project Metadata

Edit `pyproject.toml` and replace placeholders:
- Author name and email
- Repository URLs
- Project description
- Version number

---

## Publishing to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `Perplexity-claude` (or your preferred name)
3. Do NOT initialize with README (you already have one)

### Step 2: Initialize Git (if not already done)

```bash
cd /home/mewtwo/Zykairotis/Perplexity-claude

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Perplexity MCP Server"
```

### Step 3: Add Remote and Push

```bash
# Add GitHub as remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/Perplexity-claude.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Configure Repository Settings

On GitHub, go to repository settings:

1. **Description**: Add a short description
2. **Topics**: Add tags like `mcp`, `perplexity`, `ai`, `llm`, `python`
3. **About**: Add homepage URL (if applicable)
4. **Security**: Review security settings

### Step 5: Create LICENSE File

Create a `LICENSE` file. For MIT License:

```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

git add LICENSE
git commit -m "Add MIT License"
git push
```

---

## Publishing to PyPI

### Step 1: Prepare Package Structure

Ensure your `pyproject.toml` is properly configured (already done).

### Step 2: Install Build Tools

```bash
pip install --upgrade pip
pip install build twine
```

### Step 3: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build package
python -m build
```

This creates:
- `dist/perplexity-mcp-server-0.1.0.tar.gz` (source distribution)
- `dist/perplexity_mcp_server-0.1.0-py3-none-any.whl` (wheel)

### Step 4: Test on TestPyPI First

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*
```

You'll need to:
1. Create account at https://test.pypi.org
2. Create API token
3. Enter credentials when prompted

### Step 5: Test Installation from TestPyPI

```bash
# Create test environment
python -m venv test_env
source test_env/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    perplexity-mcp-server

# Test it works
perplexity-mcp --help
```

### Step 6: Publish to Real PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

You'll need:
1. Account at https://pypi.org
2. API token from https://pypi.org/manage/account/token/

### Step 7: Configure PyPI Token (Optional)

Store token in `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

---

## Publishing to Docker Hub

### Step 1: Create Docker Hub Account

Sign up at https://hub.docker.com if you don't have an account.

### Step 2: Login to Docker Hub

```bash
docker login
# Enter username and password
```

### Step 3: Build Docker Image with Tags

```bash
# Replace USERNAME with your Docker Hub username
export DOCKER_USERNAME=yourusername
export VERSION=0.1.0

# Build with multiple tags
docker build -t ${DOCKER_USERNAME}/perplexity-mcp:${VERSION} \
             -t ${DOCKER_USERNAME}/perplexity-mcp:latest .
```

### Step 4: Test Image Locally

```bash
# Run container
docker run -d \
  -p 8000:8000 \
  --name perplexity-test \
  ${DOCKER_USERNAME}/perplexity-mcp:latest

# Check logs
docker logs perplexity-test

# Stop and remove
docker stop perplexity-test
docker rm perplexity-test
```

### Step 5: Push to Docker Hub

```bash
# Push specific version
docker push ${DOCKER_USERNAME}/perplexity-mcp:${VERSION}

# Push latest
docker push ${DOCKER_USERNAME}/perplexity-mcp:latest
```

### Step 6: Update Docker Hub Repository

On Docker Hub:
1. Add repository description
2. Add README (from your GitHub)
3. Link to GitHub repository
4. Add tags for categorization

---

## Creating Releases

### Step 1: Create CHANGELOG.md

```bash
cat > CHANGELOG.md << 'EOF'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- Initial release
- MCP server implementation
- Perplexity AI integration
- Profile management system
- CLI chat interface
- Docker support
- FastAPI REST API
- LiteLLM proxy support

### Security
- Cookie-based authentication
- Environment variable configuration

EOF

git add CHANGELOG.md
git commit -m "Add CHANGELOG"
git push
```

### Step 2: Create Git Tag

```bash
# Create annotated tag
git tag -a v0.1.0 -m "Release version 0.1.0"

# Push tag to GitHub
git push origin v0.1.0
```

### Step 3: Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Select tag `v0.1.0`
4. Title: "v0.1.0 - Initial Release"
5. Description: Copy from CHANGELOG.md
6. Attach build artifacts (optional)
7. Click "Publish release"

### Step 4: Automate Releases with GitHub Actions (Optional)

Create `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Distribution Best Practices

### Version Numbering (Semantic Versioning)

- **MAJOR** (1.0.0): Incompatible API changes
- **MINOR** (0.1.0): Backward-compatible functionality
- **PATCH** (0.0.1): Backward-compatible bug fixes

### Release Workflow

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit changes
4. Create git tag
5. Build and test package
6. Push to PyPI
7. Push Docker image
8. Create GitHub release

### Documentation

- Keep README.md up to date
- Document breaking changes
- Provide migration guides
- Include code examples
- Add API documentation

### Security

- Never commit secrets
- Use `.env` for local configuration
- Provide `.example.env` template
- Document security considerations
- Rotate credentials regularly

### Testing

- Run tests before releasing
- Test installation from PyPI
- Test Docker image
- Verify documentation links
- Check all examples work

---

## Quick Release Command

Create a script `scripts/release.sh`:

```bash
#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./scripts/release.sh VERSION"
    echo "Example: ./scripts/release.sh 0.1.0"
    exit 1
fi

echo "Releasing version ${VERSION}..."

# Update version in pyproject.toml
sed -i "s/^version = .*/version = \"${VERSION}\"/" pyproject.toml

# Run tests
pytest

# Build package
rm -rf dist/ build/ *.egg-info/
python -m build

# Create git tag
git add pyproject.toml
git commit -m "Bump version to ${VERSION}"
git tag -a "v${VERSION}" -m "Release version ${VERSION}"
git push origin main
git push origin "v${VERSION}"

# Upload to PyPI
python -m twine upload dist/*

# Build and push Docker
docker build -t yourusername/perplexity-mcp:${VERSION} \
             -t yourusername/perplexity-mcp:latest .
docker push yourusername/perplexity-mcp:${VERSION}
docker push yourusername/perplexity-mcp:latest

echo "Release ${VERSION} complete!"
```

Make it executable:

```bash
chmod +x scripts/release.sh
```

---

## Verification Checklist

After publishing, verify:

- [ ] GitHub repository is public and accessible
- [ ] README displays correctly on GitHub
- [ ] Package installs from PyPI: `pip install perplexity-mcp-server`
- [ ] Docker image pulls: `docker pull username/perplexity-mcp`
- [ ] Documentation links work
- [ ] Examples in README run successfully
- [ ] GitHub release is created with correct version
- [ ] CHANGELOG is updated
- [ ] License file is present

---

## Troubleshooting

### PyPI Upload Fails

**Error: "File already exists"**
- You cannot re-upload the same version
- Increment version number in `pyproject.toml`

**Error: "Invalid credentials"**
- Check API token is correct
- Ensure token has upload permissions

### Docker Push Fails

**Error: "denied: requested access to the resource is denied"**
- Run `docker login` again
- Check repository name matches your username

### Git Push Fails

**Error: "remote: Permission denied"**
- Check SSH key is added to GitHub
- Or use HTTPS with personal access token

---

## Additional Resources

- [PyPI Packaging Guide](https://packaging.python.org/)
- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [GitHub Releases Guide](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

---

**Last Updated**: 2024