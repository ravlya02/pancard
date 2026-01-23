"""
Setup configuration for pancard package
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pancard",
    version="0.1.0",
    author="Rahul Ratnaparkhi",
    author_email="ravlya02@gmail.com",
    description="A Python package to validate and decode Indian PAN card numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravlya02/pancard",
    project_urls={
        "Bug Tracker": "https://github.com/ravlya02/pancard/issues",
        "Documentation": "https://github.com/ravlya02/pancard#readme",
        "Source Code": "https://github.com/ravlya02/pancard",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
            "twine>=3.0",
            "wheel>=0.36",
            "setuptools>=50.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pancard=pancard.cli:main",
        ],
    },
    keywords="pan pancard validation india tax identification",
    zip_safe=False,
    include_package_data=True,
)