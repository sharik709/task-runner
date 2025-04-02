"""
Configure the test environment
"""
import os
import sys
from pathlib import Path

# Add the project root to the Python path to ensure taskops can be imported
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
