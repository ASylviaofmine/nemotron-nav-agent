"""The project's tools: evaluation, self-test, video rendering.

This directory is a package rather than a loose folder of scripts, so
that every module can be imported with an absolute import
(``from tools.selftest import ...``) instead of a path hack. PyCharm
resolves those without complaint, and so does every other tool.

Run them either way:

    python tools/selftest.py          # directly
    python -m tools.selftest          # as a module
"""
