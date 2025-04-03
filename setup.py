from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="taskops",
    version="0.1.7",
    author="Sharik Shaikh",
    author_email="shaikhsharik709@gmail.com",
    description="A powerful yet simple task processor for scheduling and automating tasks",
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
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=2.0.0",
        "schedule>=1.2.0",
        "loguru>=0.7.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=5.0.0",
            "black>=24.0.0",
            "isort>=5.13.0",
            "mypy>=1.9.0",
            "flake8>=7.0.0",
            "build>=1.0.0",
            "twine>=5.0.0",
        ],
        "mysql": ["mysql-connector-python>=8.0.0"],
    },
    entry_points={
        "console_scripts": [
            "taskops=task_processor.__main__:main",
        ],
    },
)
