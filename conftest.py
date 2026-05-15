from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / 'src'
EXAMPLES_DIR = ROOT / 'examples_bank'

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if EXAMPLES_DIR.exists() and str(EXAMPLES_DIR) not in sys.path:
    sys.path.insert(0, str(EXAMPLES_DIR))
