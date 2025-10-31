# -*- coding: utf-8 -*-
"""
 PRIVATE IDENTITY LLC - PROPRIETARY AND CONFIDENTIAL (c) COPYRIGHT 2018 - 2025 PRIVATE IDENTITY LLC
 All Rights Reserved.
 NOTICE:  All information contained herein is, and remains the
 property of PRIVATE IDENTITY LLC and its suppliers, if any.  The intellectual and technical concepts contained
 herein are proprietary to PRIVATE IDENTITY LLC and its suppliers and may be covered by U.S. and Foreign Patents,
 patents in process, and are protected by trade secret or copyright law. Dissemination of this information or
 reproduction of this material is strictly forbidden unless prior written permission is obtained from PRIVATE
 IDENTITY LLC. Any software that is made available to download from Private Identity LLC ("Software") is the
 copyrighted work of Private Identity LLC and/or its suppliers. Use of the Software is governed by the terms of the
 end user license agreement, if any, which accompanies or is included with the Software ("License Agreement"). An
 end user must not install any Software that is accompanied by or includes a License Agreement, unless he or she
 first agrees to the License Agreement terms. RESTRICTED RIGHTS LEGEND. Any Software which is downloaded from
 PRIVATE IDENTITY LLC for or on behalf of the United States of America, its agencies and/or instrumentalities ("U.S.
 Government"), is provided with Restricted Rights. Use, duplication, or disclosure by the U.S. Government is subject
 to restrictions as set forth in subparagraph (c)(1)(ii) of the Rights in Technical Data and Computer Software
 clause at DFARS 252.227-7013 or subparagraphs (c)(1) and (2) of the Commercial Computer Software - Restricted
 Rights at 48 CFR 52.227-19, as applicable.
 Manufacturer is PRIVATE IDENTITY LLC , 13331 Signal Tree, Potomac, MD  20854  USA.
"""

import os
import sys
import platform
from setuptools import setup, find_packages, Extension
from setuptools.command.build_py import build_py
from setuptools.command.install import install
import subprocess

"""
Setup module for cryptonets python sdk.

Created on April 04th - 2025

@author: Private Identity
"""
NAME = "cryptonets_python_sdk"
DESCRIPTION = "Cryptonets SDK Library for Python"
AUTHOR = "Private Identity"
AUTHOR_EMAIL = "support@private.id"
URL = "https://private.id/"
VERSION = "2.0.0b1"
REQUIRES = [
    "numpy >= 1.21.0", 
    "pillow >= 9.1.0",
    "boto3 >= 1.24.0",
    "tqdm >= 4.64.0",
    "exifread >= 3.0.0",
    "cffi >= 1.15.0",
    # Note: importlib.metadata is part of stdlib in Python 3.8+
    # For older Python versions, add the backport
    "importlib-metadata >= 4.0.0; python_version < '3.8'",
    "betterproto >= 1.2.5",
    "pyyaml >= 6.0.2"
]

# Additional packages for development and testing
DEV_REQUIRES = [    
    "betterproto[compiler] >= 1.2.5"
]

LONG_DESCRIPTION = ""
if os.path.exists("./README.md"):
    with open("README.md", encoding="utf-8") as fp:
        LONG_DESCRIPTION = fp.read()

# Custom commands
class CustomBuildCommand(build_py):
    """Custom build command to handle API header generation and other preprocessing steps."""
    
    def run(self):
        # Generate the API header from the function declarations
        self.generate_api_header()
        
        # Generate Python code for API Resut
        # self.generate_proto_code()
        
        # Run the standard build_py command
        build_py.run(self)
 
    def generate_api_header(self):
            # This should call a script inside native subfolder
            # TODO add prividModule as git submodule
            pass

class CustomInstallCommand(install):
    """Custom install command to ensure proper binary installation."""
    
    def run(self):
        # Run the standard install
        install.run(self)
        
        # Additional post-install steps
        print("Running post-installation steps for Cryptonets SDK...")

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Proprietary",
    url=URL,
    keywords=["privateid", "cryptonets", "face identification", "biometrics", "privacy"],
    packages=find_packages(where="src", exclude=["tests*","idl*","protoc*","protoc"]),
    include_package_data=True,
    platforms="any",
    install_requires=REQUIRES,
    extras_require={
        "dev": DEV_REQUIRES,
    },
    python_requires=">=3.6",
    package_dir={"": "src"},
    cmdclass={
        'build_py': CustomBuildCommand,
        'install': CustomInstallCommand,
    },
    project_urls={
        "Bug Reports": "https://github.com/prividentity/cryptonets-python-sdk/issues",
        "Source": "https://github.com/prividentity/cryptonets-python-sdk",
        "Documentation": "https://docs.private.id/cryptonets-python-sdk/1.3.11/index.html",
        "Release Notes": "https://docs.private.id/cryptonets-python-sdk/1.3.11/changelog.html",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security :: Cryptography",
    ],
    # Entry points for CLI tools if any
    entry_points={
        "console_scripts": [
            # "cryptonets-cli=cryptonets_python_sdk.cli:main",
        ],
    },
    package_data={
        "cryptonets_python_sdk": [
            "api_h.h",           # Specifically include the CFFI header
            "*.py",              # Python modules
            "LICENSE",           # License file
            "README.md",         # README file
            "messages/**/*.py",
            "messages/**/*.pyi"
        ]
    },
)
