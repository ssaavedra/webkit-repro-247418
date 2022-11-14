Minimal Reproduction for Bug #247418 on WebKit (Safari)
=======================================================

How to reproduce
----------------

This repo should be self-contained. It requires Python 3 and appropriate SQLite bindings for Python. I've been using Python under Linux, but should be working with standard macOS Python 3.

1. Open this repo in a Terminal, and run `python3 app.py`
2. Open Safari.
3. Optionally, open WebInspector if you want to see what's happening behind the scenes.
4. Click login
5. Click perform operation. Should work.
6. Click logout
7. Click perform operation. Will fail on buggy versions.


License
-------

Contains bottle.py from Bottle 0.12, and a modified version of bottle_sqlite from [bottle-sqlite](https://github.com/bottlepy/bottle-sqlite), both under the MIT License.

My code is under [CC0](https://creativecommons.org/publicdomain/zero/1.0/deed.en).
