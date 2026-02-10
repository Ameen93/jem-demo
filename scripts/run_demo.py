#!/usr/bin/env python3
"""Run the Jem HR Demo CLI."""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

load_dotenv()

from src.cli.demo import main

if __name__ == "__main__":
    main()
