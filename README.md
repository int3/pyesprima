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
is a good way to get down to business. The API is almost exactly the same, so
you can easily swap in an interface to the external Node process later on.

Also, since the code is semi-automatically translated using [js2py][2], it's
easier to keep up-to-date, and thus bit-rot is less of a problem.

Finally, you'll be glad to know that all the relevant tests from the original
Esprima pass.

API
---

Aside from our handling of RegExps, we expose the same interface as Esprima /
SpiderMonkey:

    >>> import pyesprima

    >>> print pyesprima.tokenize("1 + 1")
    [{'type': 'Numeric', 'value': '1'},
     {'type': 'Punctuator', 'value': '+'},
     {'type': 'Numeric', 'value': '1'}]

    >>> pyesprima.parse("1 + 1", loc=True)
    {'body': [{'type': 'ExpressionStatement', 'expression': {'operator': '+',
    'loc': {'start': {'column': 0, 'line': 1}, 'end': ...

Esprima creates `RegExp` objects for regular expression literals in the JS
source. However, Python regular expressions do not have a `global` flag (it has
`re.findall` instead), so we cannot map JS RegExps perfectly; instead,
`pyesprima.RegExp` objects have a `flags` attribute that records what flags were
used in the JS source.

Note that the returned objects are instances of `pyesprima.jsdict`, which
simulates JavaScript dicts in having both `a.x` and `a['x']` mean the same
thing.

Installing
----------

    pip install pyesprima


[1]: http://esprima.org/
[2]: https://github.com/int3/js2py
