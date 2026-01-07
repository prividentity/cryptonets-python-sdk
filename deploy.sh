#!/bin/bash

# Automated Python package deployment script
# Usage: ./deploy.sh <version>

set -e  # Exit immediately if a command exits with a non-zero status

# Check if version parameter is provided
if [ -z "$1" ]; then
    echo "Error: Version parameter is required"
    echo "Usage: ./deploy.sh <version>"
    exit 1
fi

VERSION=$1

# Validate version format (should be 2.number.number)
if ! [[ $VERSION =~ ^2\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version format must be 2.x.y where x and y are numbers"
    echo "Example: 2.3.20"
    exit 1
fi

# Function to check if manifest.yaml exists in S3
check_manifest_exists() {
    local version=$1
    local manifest_url="https://cryptonets-python-sdk.s3.us-east-1.amazonaws.com/${version}/manifest.yaml"

    echo "Checking if manifest.yaml exists for version ${version}..."

    # Use curl to check if the file exists (HTTP HEAD request)
    if curl --head --silent --fail "$manifest_url" > /dev/null 2>&1; then
        echo "✓ Manifest file found at: $manifest_url"
        return 0
    else
        echo "✗ Error: Manifest file not found at: $manifest_url"
        echo "Please ensure the manifest.yaml file exists in S3 before deploying this version."
        exit 1
    fi
}

# Check if manifest.yaml exists for this version
check_manifest_exists "$VERSION"

echo "Starting deployment process for version: $VERSION"

# Delete folders if they exist
echo "Cleaning up old build files..."
[ -d ".venv" ] && rm -rf .venv && echo "Deleted .venv folder in sdk directory"
[ -d "build" ] && rm -rf build && echo "Deleted build folder in sdk directory"
[ -d "dist" ] && rm -rf dist && echo "Deleted dist folder in sdk directory"

# Update version in setup.py
echo "Updating version in setup.py..."
sed -i "s/^VERSION = \".*\"/VERSION = \"$VERSION\"/" setup.py
if grep -q "VERSION = \"$VERSION\"" setup.py; then
    echo "Successfully updated version in setup.py"
else
    echo "Failed to update version in setup.py"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install deployment requirements
echo "Installing deployment requirements..."
pip install -r deployment_reqs.txt

# Build the Python package
echo "Building Python package..."
python -m build

echo "Deployment process completed successfully!"
echo "Package version $VERSION is ready for distribution."

# Deactivate virtual environment
deactivate

# If everything went well, you can upload the package using twine by running :
# twine upload dist/* # you will be asked to enter the PIP API token.

# Test the deployed package
echo "Testing deployed package..."
cd examples
[ -d ".venv" ] && rm -rf .venv && echo "Deleted .venv folder in examples directory"
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib pytest dotenv
pip install ../dist/*.whl

# Run tests and capture exit code
set +e  # Temporarily disable exit on error to capture exit code
python samples.py --all
TEST_EXIT_CODE=$?
set -e  # Re-enable exit on error

deactivate

# Check if tests passed
if [ $TEST_EXIT_CODE -ne 0 ]; then
    echo "✗ Package tests failed with exit code: $TEST_EXIT_CODE"
    exit $TEST_EXIT_CODE
fi

echo "✓ Package tests passed successfully!"
