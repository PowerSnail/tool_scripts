"""Remove duplicated value in environment variable

This script preserves the ordering of the environment variable.

Only Compatible with python3.7 or later, as this script uses
the order-preserving feature added in python3.7.

Input is taken from standard input as a single line of 
":"-delimited string.

Output is printed to standard output, as a single line of
":"-delimited string.

Usage:
    python rm_duplicate_env_val.py
    python rm_duplicate_env_val.py -h|--help
    python rm_duplicate_env_val.py -v|--version

Other options will be ignored.
"""
import sys

__version__ = "0.1.0"


if len(sys.argv) > 1:
    option = sys.argv[1]
    if option in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    elif option in ("-v", "--version"):
        print(__version__)
        sys.exit(0)

values = input().split(":")
values_uniq = { v : None for v in values }
print(":".join(values_uniq.keys()))
