# Deployment Guide for Cryptonets Python SDK

This document explains how to deploy new versions of the Cryptonets Python SDK.

## Prerequisites

Before deploying, ensure you have:

- Python 3.x installed
- `pip` installed
- Access to the repository with write permissions
- PyPI credentials (if publishing to PyPI)

## Automated Deployment

We provide a deployment script (`deploy.sh`) that automates most of the deployment process.

### Usage

```bash
./deploy.sh <version>
```

For example:

```bash
./deploy.sh 1.3.20
```

### What the Script Does

The deployment script performs the following steps:

1. **Cleanup**: Removes old build artifacts
   - Deletes `.venv` folder (virtual environment)
   - Deletes `dist` folder (distribution packages)
   - Deletes `docs/build` folder (documentation build)

2. **Version Update**:
   - Updates the release version in `docs/source/conf.py`
   - Updates the VERSION variable in `setup.py`

3. **Environment Setup**:
   - Creates a new Python virtual environment in `.venv`
   - Installs all required packages from `deployment_reqs.txt`

4. **Documentation Build**:
   - Builds the documentation using Sphinx
   - Creates a tarball of the HTML documentation

   > **IMPORTANT NOTE**: Always check the HTML generation output carefully. The conversion from reStructuredText (.rst) to HTML can sometimes generate errors or unexpected formatting. Review the generated documentation in a browser before proceeding.

5. **Package Build**:
   - Builds the Python package (both source distribution and wheel)

## Manual Deployment Steps

If you need to manually perform the deployment process:

1. Clean up old build artifacts:

   ```bash
   rm -rf .venv dist docs/build
   ```

2. Update version numbers:
   - In `docs/source/conf.py`: Change `release = "x.x.x"` to your new version
   - In `setup.py`: Change `VERSION = "x.x.x"` to your new version

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Install deployment requirements:

   ```bash
   pip install -r deployment_reqs.txt
   ```

5. Build documentation:

   ```bash
   cd docs
   make html
   cd ..
   ```

   After building the documentation, carefully review the terminal output for any warnings or errors. Open the generated HTML files in a browser to verify that the documentation renders correctly, as reStructuredText conversion can sometimes produce unexpected results.

6. Create documentation tarball:

   ```bash
   tar -czf docs/build/html.tar.gz -C docs/build html
   ```

   The content of the html generated documentation can be uploaded upstream later.

7. Build Python package:

   ```bash
   python -m build
   ```

## Publishing to PyPI

After running the deployment script, you can publish the package to PyPI:

```bash
# Activate the virtual environment if not already active
source .venv/bin/activate

# Upload to PyPI (you'll need to have PyPI credentials configured)
twine upload dist/*
```

## Checking the Build

After running the deployment script, you should verify:

1. The `dist` directory contains:
   - A `.tar.gz` file (source distribution)
   - A `.whl` file (wheel distribution)

2. The `docs/build/html` directory contains the built documentation

3. The `docs/build/html.tar.gz` file contains the compressed documentation

## Troubleshooting

If you encounter any issues during deployment:

1. Make sure you have the correct permissions
2. Ensure all dependencies are installed (`deployment_reqs.txt`)
3. Check for any error messages in the console output
4. Verify that the version numbers are correctly updated in all files

### Documentation Build Issues

The documentation uses reStructuredText (.rst) which can be tricky:

1. **Check Sphinx warnings**: Review all warnings in the terminal output during the `make html` step
2. **Validate RST syntax**: Use an RST linter to validate your .rst files before building
3. **Review in browser**: Always open the generated HTML in a browser to verify proper rendering
4. **Common problems**:
   - Indentation errors in code blocks
   - Incorrect heading hierarchy
   - Missing blank lines between sections
   - Improper table formatting
   
If the HTML output contains errors, fix the .rst source files and rebuild before proceeding with deployment.
