import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyesprima",
    version = "0.1.2",
    author = "Jez Ng",
    author_email = "me@jezng.com",
    description = "Python port of Esprima, the Javascript parser.",
    license = "BSD",
    keywords = "javascript parser",
    url = "https://github.com/int3/pyesprima",
    packages=['pyesprima'],
    long_description=read('README'),
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
