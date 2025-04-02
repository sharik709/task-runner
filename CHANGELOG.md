# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-03-25

### Added
- Initial release
- Task scheduling with support for recurring and one-time tasks
- YAML-based task configuration
- Automatic retry mechanism for failed tasks
- Task dependencies
- Per-task logging with automatic rotation
- Command-line interface
- Python API for programmatic usage

### Security
- Secure command execution without shell injection vulnerabilities
- Safe file operations with appropriate permissions
- Input validation for all configuration files

### Dependencies
- pydantic>=2.0.0
- pyyaml>=6.0.0
- schedule>=1.2.0
- python-dateutil>=2.8.2
- typing-extensions>=4.5.0
