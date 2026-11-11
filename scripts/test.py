# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML==6.0.3", "certifi>=2025.0.0"]
# ///
"""Run bundled-script tests with their declared runtime dependencies."""
from pathlib import Path
import unittest
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pattern", default="test*.py", help="Test filename pattern")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).resolve().parents[1] / "tests"), pattern=args.pattern)
    raise SystemExit(not unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful())
