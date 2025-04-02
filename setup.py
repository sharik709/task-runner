from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="task-runner",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A powerful yet simple task runner for scheduling and automating tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sharik709/task-runner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "pyyaml>=6.0.0",
        "schedule>=1.2.0",
        "python-dateutil>=2.8.2",
        "typing-extensions>=4.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
            "flake8>=6.0.0",
            "build>=1.0.0",
            "twine>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "task-runner=task_runner.__main__:main",
        ],
    },
)
