import os
import sys

import pytest

# Добавьте путь к директории src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

pytest_plugins = ["pytest_asyncio"]
