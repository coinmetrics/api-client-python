#!/usr/bin/env python3
"""
Build hook for Poetry to run schema generation before building.
"""

import subprocess
import sys
from pathlib import Path


def build_schema_constants():
    """Run the schema build script."""
    script_path = Path(__file__).parent / "coinmetrics" / "build.py"
    result = subprocess.run([sys.executable, str(script_path)], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Schema build failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print(result.stdout)


if __name__ == "__main__":
    build_schema_constants()