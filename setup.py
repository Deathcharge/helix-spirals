from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="helix-spirals",
    version="1.0.0",
    author="Helix Team",
    author_email="team@helix.dev",
    description="Open-source workflow automation engine for AI-driven integration orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Deathcharge/helix-spirals",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: Internet",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.0.0",
        "sqlalchemy>=2.0.0",
        "aiohttp>=3.9.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "cryptography>=41.0.0",
        "pyjwt>=2.8.0",
        "redis>=5.0.0",
        "celery>=5.3.0",
        "apscheduler>=3.10.0",
        "pydantic-settings>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "isort>=5.13.0",
        ],
        "integrations": [
            "slack-sdk>=3.23.0",
            "discord.py>=2.3.0",
            "stripe>=7.4.0",
            "boto3>=1.34.0",
            "google-cloud-storage>=2.14.0",
            "twilio>=8.10.0",
            "mailchimp-marketing>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "helix-spirals=helix_spirals.main:main",
        ],
    },
    keywords="workflow automation integration orchestration zapier alternative ai agents",
    project_urls={
        "Bug Reports": "https://github.com/Deathcharge/helix-spirals/issues",
        "Source": "https://github.com/Deathcharge/helix-spirals",
        "Documentation": "https://helix-spirals.dev",
    },
)
