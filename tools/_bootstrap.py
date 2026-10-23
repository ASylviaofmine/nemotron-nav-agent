"""Make the project importable no matter where the script is run from.

A script in ``tools/`` is run in two ways, and both have to work:

    python tools/selftest.py      # sys.path[0] is tools/
    python -m tools.selftest      # sys.path[0] is the project root

In the first case the project root is not on the path, so ``import src``
would fail. Putting the fix in a module of its own keeps it in one
place, and keeps it out of the import block -- which is what stops
editors from flagging every import in the file as "not at the top".

Import it like this, before anything else:

    from tools._bootstrap import ROOT
"""

import os
import sys

# The project root -- the directory that contains ``src/`` and ``tools/``.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
