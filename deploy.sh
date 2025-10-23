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

# Validate version format (should be 1.number.number)
if ! [[ $VERSION =~ ^1\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version format must be 1.x.y where x and y are numbers"
    echo "Example: 1.3.20"
    exit 1
fi


echo "Starting deployment process for version: $VERSION"

# Delete folders if they exist
echo "Cleaning up old build files..."
[ -d ".venv" ] && rm -rf .venv && echo "Deleted .venv folder"
[ -d "dist" ] && rm -rf dist && echo "Deleted dist folder" 
[ -d "docs/build" ] && rm -rf docs/build && echo "Deleted docs/build folder"


# Update version in conf.py
echo "Updating version in conf.py..."
sed -i "s/^release = \".*\"/release = \"$VERSION\"/" docs/source/conf.py
if grep -q "release = \"$VERSION\"" docs/source/conf.py; then
    echo "Successfully updated version in conf.py"
else
    echo "Failed to update version in conf.py"
    exit 1
fi

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

# Build documentation
echo "Building documentation..."
cd docs
make html
cd ..

# Create tarball of html documentation
echo "Creating documentation tarball..."
tar -czf docs/build/html.tar.gz -C docs/build html

# Build the Python package
echo "Building Python package..."
python -m build

echo "Deployment process completed successfully!"
echo "Package version $VERSION is ready for distribution."

# Deactivate virtual environment
deactivate

# If everything went well, you can upload the package using twine by running :
# twine upload dist/* # you will be asked to enter the PIP API token.
