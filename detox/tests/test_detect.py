import sys

from detection_engine.diff import Differ

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        d = Differ(path)
        d.diff()
