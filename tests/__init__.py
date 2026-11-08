import sys
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
parent_dir = os.path.abspath(os.path.join(base_dir, ".."))

for p in [base_dir, parent_dir]:
    if p not in sys.path:
        sys.path.insert(0, p)
