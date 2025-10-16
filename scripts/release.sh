#!/bin/bash

set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./scripts/release.sh VERSION"
    echo "Example: ./scripts/release.sh 0.1.0"
    exit 1
fi

echo "🚀 Releasing version ${VERSION}..."

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "⚠️  Warning: You are not on the main branch (current: $CURRENT_BRANCH)"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "❌ Error: You have uncommitted changes. Please commit or stash them first."
    git status -s
    exit 1
fi

echo "✓ Git status is clean"

# Update version in pyproject.toml
echo "📝 Updating version in pyproject.toml..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' "s/^version = .*/version = \"${VERSION}\"/" pyproject.toml
else
    # Linux
    sed -i "s/^version = .*/version = \"${VERSION}\"/" pyproject.toml
fi

# Update CHANGELOG.md with release date
CURRENT_DATE=$(date +%Y-%m-%d)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/## \[${VERSION}\] - .*/## [${VERSION}] - ${CURRENT_DATE}/" CHANGELOG.md 2>/dev/null || true
else
    sed -i "s/## \[${VERSION}\] - .*/## [${VERSION}] - ${CURRENT_DATE}/" CHANGELOG.md 2>/dev/null || true
fi

echo "✓ Version updated to ${VERSION}"

# Run tests
echo "🧪 Running tests..."
if command -v pytest &> /dev/null; then
    pytest || {
        echo "❌ Tests failed. Aborting release."
        exit 1
    }
    echo "✓ All tests passed"
else
    echo "⚠️  pytest not found, skipping tests"
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/
echo "✓ Build artifacts cleaned"

# Build package
echo "📦 Building package..."
python -m build || {
    echo "❌ Build failed. Make sure 'build' is installed: pip install build"
    exit 1
}
echo "✓ Package built successfully"

# List built artifacts
echo "📋 Built artifacts:"
ls -lh dist/

# Create git commit and tag
echo "🏷️  Creating git tag..."
git add pyproject.toml CHANGELOG.md
git commit -m "chore: bump version to ${VERSION}" || echo "No changes to commit"
git tag -a "v${VERSION}" -m "Release version ${VERSION}"
echo "✓ Git tag v${VERSION} created"

# Ask for confirmation before pushing
echo ""
echo "📤 Ready to push to remote repositories"
read -p "Push to git remote? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin main
    git push origin "v${VERSION}"
    echo "✓ Pushed to git remote"
else
    echo "⏭️  Skipped git push"
fi

# Ask for PyPI upload
echo ""
read -p "Upload to PyPI? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v twine &> /dev/null; then
        echo "📤 Uploading to PyPI..."
        python -m twine upload dist/*
        echo "✓ Uploaded to PyPI"
    else
        echo "❌ twine not found. Install it with: pip install twine"
        exit 1
    fi
else
    echo "⏭️  Skipped PyPI upload"
fi

# Ask for Docker build and push
echo ""
read -p "Build and push Docker image? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter Docker Hub username: " DOCKER_USERNAME
    if [ -z "$DOCKER_USERNAME" ]; then
        echo "❌ Docker username cannot be empty"
        exit 1
    fi

    echo "🐳 Building Docker image..."
    docker build -t ${DOCKER_USERNAME}/perplexity-mcp:${VERSION} \
                 -t ${DOCKER_USERNAME}/perplexity-mcp:latest .
    echo "✓ Docker image built"

    echo "📤 Pushing to Docker Hub..."
    docker push ${DOCKER_USERNAME}/perplexity-mcp:${VERSION}
    docker push ${DOCKER_USERNAME}/perplexity-mcp:latest
    echo "✓ Pushed to Docker Hub"
else
    echo "⏭️  Skipped Docker build"
fi

echo ""
echo "✅ Release ${VERSION} complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Create GitHub release at: https://github.com/YOUR_USERNAME/Perplexity-claude/releases/new"
echo "   2. Verify PyPI package: https://pypi.org/project/perplexity-mcp-server/"
echo "   3. Verify Docker image: https://hub.docker.com/r/${DOCKER_USERNAME}/perplexity-mcp"
echo "   4. Update documentation if needed"
echo ""
