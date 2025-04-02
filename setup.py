from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="task-runner",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A powerful yet simple task runner with plugin support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/task-runner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
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
        "schedule==1.2.1",
        "PyYAML==6.0.1",
        "SQLAlchemy==2.0.27",
        "python-dateutil==2.8.2",
        "loguru==0.7.2",
        "pydantic==2.6.1",
        "pluggy==1.4.0",
        "rich==13.7.0",
    ],
    entry_points={
        "console_scripts": [
            "task-runner=task_runner.cli:main",
        ],
        "task_runner.plugins": [
            "mysql=task_runner.plugins.mysql:MySQLPlugin",
            "postgres=task_runner.plugins.postgres:PostgresPlugin",
            "redis=task_runner.plugins.redis:RedisPlugin",
            "http=task_runner.plugins.http:HTTPPlugin",
        ],
    },
)
