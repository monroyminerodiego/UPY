"""
Ejecucion codigo: python setup.py build_ext --inplace
"""

from distutils.core import setup #type: ignore
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("code.pyx"),
    include_dirs=[numpy.get_include()]
)