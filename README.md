PyEsprima
=========

A Python port of [Esprima][1], the JavaScript parser.

Why shouldn't I use it?
-----------------------

It's pretty slow -- about two orders of magnitude slower to parse a 116k JS
file. The code was semi-automatically translated from JavaScript, and it does a
lot of string appending, which is fast in JS but slow in Python.

Why should I use it?
--------------------

Shelling out to a NodeJS process is likely to be a better way to use Esprima
from Python. However, writing the interprocess data-marshaling code is a bit
annoying, so if you want to do a quick hack on small amounts of data, PyEsprima
is a good way to get down to business. The API is exactly the same, so you can
easily swap in an interface to the external Node process later on.

Also, since the code is semi-automatically translated using [js2py][2], it's
pretty easy to keep up-to-date. You could even do it yourself. Don't fear the
bit rot!

API
---

Pretty much the same as Esprima's / SpiderMonkey's API:

    >>> import pyesprima

    >>> print pyesprima.tokenize("1 + 1")
    [{'type': 'Numeric', 'value': '1'},
     {'type': 'Punctuator', 'value': '+'},
     {'type': 'Numeric', 'value': '1'}]

    >>> pyesprima.parse("1 + 1", loc=True)
    {'body': [{'type': 'ExpressionStatement', 'expression': {'operator': '+',
    'loc': {'start': {'column': 0, 'line': 1}, 'end': ...

Installing
----------

    pip install pyesprima

[1]: http://esprima.org/
[2]: https://github.com/int3/js2py
