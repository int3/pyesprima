# -*- coding: latin-1 -*-
from __future__ import print_function
import re, json, difflib
def typeof(t):
    if t is None: return 'undefined'
    elif isinstance(t, bool): return 'boolean'
    elif isinstance(t, str) or isinstance(t, unicode): return 'string'
    elif isinstance(t, int) or isinstance(t, float): return 'number'
    elif hasattr(t, '__call__'): return 'function'
    else: return 'object'

def list_indexOf(l, v):
    try:
        return l.index(v)
    except:
        return -1

parseFloat = float
parseInt = int

class jsdict(object):
    def __init__(self, d):
        self.__dict__.update(d)
    def __getitem__(self, name):
        if name in self.__dict__:
          return self.__dict__[name]
        else:
          return None
    def __setitem__(self, name, value):
        self.__dict__[name] = value
        return value
    def __getattr__(self, name):
        try:
            return getattr(self, name)
        except:
            return None
    def __setattr__(self, name, value):
        self[name] = value
        return value
    def __contains__(self, name):
        return name in self.__dict__
    def __delattr__(self, name):
        del self.__dict__[name]
    def __delitem__(self, name):
        del self.__dict__[name]
    def __repr__(self):
        return unicode(self.__dict__)

class RegExp(object):
    def __init__(self, pattern, flags=''):
        self.flags = flags
        pyflags = 0 | re.M if 'm' in flags else 0 | re.I if 'i' in flags else 0
        self.source = pattern
        self.pattern = re.compile(pattern, pyflags)
    def test(self, s):
        return self.pattern.search(s) is not None

console = jsdict({"log":print})
JSON = jsdict({"stringify": lambda a,b=None,c=None:json.dumps(a, default=b,
    indent=c, sort_keys=True)})

RegexObject = type(re.compile(''))
def adjustRegexLiteral(value):
    if hasattr(value, 'pattern') and isinstance(value.pattern, RegexObject):
        return "/%s/%s" % (value.source, value.flags)
    return value.__dict__

def cleanUpFloats(obj):
    if hasattr(obj, '__dict__') and obj.__dict__ is not None:
        for k,v in obj.__dict__.iteritems():
            if isinstance(v, float) and v % 1 == 0:
                obj[k] = int(v)
            else:
                cleanUpFloats(v)
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            if isinstance(v, float) and v % 1 == 0:
                obj[i] = int(v)
            else:
                cleanUpFloats(v)

class NotMatchingError(Exception):
    def __init__(self, expected, actual):
        super(NotMatchingError, self).__init__("Expected %s but got %s\nDiff:%s"
                % (expected, actual, "".join(difflib.unified_diff(
                    expected.splitlines(1), actual.splitlines(1)))))
        self.expected = expected
        self.actual = actual

def errorToObject(e):
    msg = unicode(e)
    if msg[0:(0 + 6)] != "Error:":
        if ('undefined' if not ('message' in e) else typeof(e.message)) == "string":
            msg = "Error: " + e.message
    return jsdict({
"index": e.index,
"lineNumber": e.lineNumber,
"column": e.column,
"message": msg,
})

def testParse(esprima=None, code=None, syntax=None):
    expected = None
    tree = None
    actual = None
    options = None
    StringObject = None
    i = None
    len__py__ = None
    err = None
    StringObject = unicode
    options = jsdict({
"comment": ('undefined' if not ('comments' in syntax) else typeof(syntax.comments)) != "undefined",
"range": True,
"loc": True,
"tokens": ('undefined' if not ('tokens' in syntax) else typeof(syntax.tokens)) != "undefined",
"raw": True,
"tolerant": ('undefined' if not ('errors' in syntax) else typeof(syntax.errors)) != "undefined",
"source": None,
})
    if ('undefined' if not ('tokens' in syntax) else typeof(syntax.tokens)) != "undefined":
        if len(syntax.tokens) > 0:
            options.range = ('undefined' if not ('range' in syntax.tokens[0]) else typeof(syntax.tokens[0].range)) != "undefined"
            options.loc = ('undefined' if not ('loc' in syntax.tokens[0]) else typeof(syntax.tokens[0].loc)) != "undefined"
    if ('undefined' if not ('comments' in syntax) else typeof(syntax.comments)) != "undefined":
        if len(syntax.comments) > 0:
            options.range = ('undefined' if not ('range' in syntax.comments[0]) else typeof(syntax.comments[0].range)) != "undefined"
            options.loc = ('undefined' if not ('loc' in syntax.comments[0]) else typeof(syntax.comments[0].loc)) != "undefined"
    if options.loc:
        options.source = syntax.loc.source
    expected = JSON.stringify(syntax, lambda o: o.__dict__, 4)
    try:
        tree = esprima.parse(code, tolerant=options.tolerant)
        tree = esprima.parse(code, tolerant=options.tolerant, range=True)
        tree = esprima.parse(code, tolerant=options.tolerant, loc=True)
        tree = esprima.parse(code, **options.__dict__)
        tree = (tree if (options.comment or options.tokens) or options.tolerant else tree.body[0])
        if options.tolerant:
            i = 0
            len__py__ = len(tree.errors)
            while 1:
                if not (i < len__py__):
                    break
                tree.errors[i] = errorToObject(tree.errors[i])
                i += 1
        cleanUpFloats(tree)
        actual = JSON.stringify(tree, adjustRegexLiteral, 4)
        esprima.parse(StringObject(code), **options.__dict__)
    except Exception as e:
        raise
    if expected != actual:
        raise NotMatchingError(expected, actual)
    def filter(key=None, value=None):
        if (key == "value") and isinstance(value, RegExp):
            value = unicode(value)
        return (None if (key == "loc") or (key == "range") else value)
    
    if options.tolerant:
        return 
    options.range = False
    options.loc = False
    expected = JSON.stringify(syntax, filter, 4)
    try:
        tree = esprima.parse(code, **options.__dict__)
        tree = (tree if options.comment or options.tokens else tree.body[0])
        if options.tolerant:
            i = 0
            len__py__ = len(tree.errors)
            while 1:
                if not (i < len__py__):
                    break
                tree.errors[i] = errorToObject(tree.errors[i])
                i += 1
        cleanUpFloats(tree)
        actual = JSON.stringify(tree, filter, 4)
    except Exception as e:
        raise NotMatchingError(expected, unicode(e))
    if expected != actual:
        raise NotMatchingError(expected, actual)

def testTokenize(esprima=None, code=None, tokens=None):
    options = None
    expected = None
    actual = None
    tree = None
    options = jsdict({
"comment": True,
"tolerant": True,
"loc": True,
"range": True,
})
    expected = JSON.stringify(tokens, adjustRegexLiteral, 4)
    try:
        tree = esprima.tokenize(code, **options.__dict__)
        cleanUpFloats(tree)
        actual = JSON.stringify(tree, adjustRegexLiteral, 4)
    except Exception as e:
        raise NotMatchingError(expected, unicode(e))
    if expected != actual:
        raise NotMatchingError(expected, actual)

def testError(esprima=None, code=None, exception=None):
    i = None
    options = None
    expected = None
    actual = None
    err = None
    handleInvalidRegexFlag = None
    tokenize = None
    options = [jsdict({
}), jsdict({
"comment": True,
}), jsdict({
"raw": True,
}), jsdict({
"raw": True,
"comment": True,
})]
    handleInvalidRegexFlag = False
    try:
        "test".match(RegExp("[a-z]", "x"))
    except Exception as e:
        handleInvalidRegexFlag = True
    exception.description = re.sub(r'Error: Line [0-9]+: ', "", exception.message)
    if exception.tokenize:
        tokenize = True
        del exception.tokenize
    expected = JSON.stringify(exception, adjustRegexLiteral, 4)
    i = 0
    while 1:
        if not (i < len(options)):
            break
        try:
            if tokenize:
                esprima.tokenize(code, **options[i].__dict__)
            else:
                esprima.parse(code, **options[i].__dict__)
        except Exception as e:
            err = errorToObject(e)
            err.description = e.description
            actual = JSON.stringify(err, adjustRegexLiteral, 4)
        if expected != actual:
            if exception.message.find("Invalid regular expression") > 0:
                if (('undefined' if not 'actual' in locals() else typeof(actual)) == "undefined") and (not handleInvalidRegexFlag):
                    return 
            raise NotMatchingError(expected, actual)
        i += 1

def testAPI(esprima=None, code=None, result=None):
    expected = None
    res = None
    actual = None
    expected = JSON.stringify(result.result, adjustRegexLiteral, 4)
    try:
        if ('undefined' if not ('property' in result) else typeof(result.property)) != "undefined":
            res = getattr(esprima, result.property)
        else:
            res = getattr(esprima, result.call)(*result.args)
        cleanUpFloats(res)
        actual = JSON.stringify(res, adjustRegexLiteral, 4)
    except Exception as e:
        raise NotMatchingError(expected, unicode(e))
    if expected != actual:
        raise NotMatchingError(expected, actual)

def runTest(esprima=None, code=None, result=None):
    if "lineNumber" in result:
        testError(esprima, code, result)
    elif "result" in result:
        testAPI(esprima, code, result)
    elif isinstance(result, list):
        testTokenize(esprima, code, result)
    else:
        testParse(esprima, code, result)

def make_jsdict(d):
    if isinstance(d, list):
        for i, item in enumerate(d):
            d[i] = make_jsdict(item)
        return d
    elif isinstance(d, dict):
        jsd = jsdict({})
        for k, v in d.iteritems():
            jsd[k] = make_jsdict(v)
        return jsd
    else:
        return d

def main():
    import sys
    from os import path
    import pyesprima
    with open(path.join(path.dirname(__file__), 'test.json')) as f:
        fixtures = json.load(f)
    failures = 0
    passes = 0
    # API tests that check for JavaScript's 'undefined' value have no good
    # equivalent in Python, so we skip them.
    # Also, JSON.stringify and json.dumps seem to treat floats slightly
    # differently, so we xfail that one numeric test.
    xfail = set(['Numeric Literals: 6.02214179e+23',
                 'API: tokenize(undefined)',
                 'API: parse()',
                 'API: parse(undefined)',
                 'API: tokenize()'])
    for category, fixture in fixtures.iteritems():
        for source, expected  in fixture.iteritems():
            if ("%s: %s" % (category, source)) in xfail:
                continue
            try:
                runTest(pyesprima, source, make_jsdict(expected))
                passes += 1
            except:
                failures += 1
                print("%s: %s" % (category, source))
    print("Passed: %d Failed: %d XFail: %d" % (passes, failures, len(xfail)))
    if failures > 0: sys.exit(1)

if __name__ == '__main__': main()
