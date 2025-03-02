"""
Ejecucion codigo: python setup.py build_ext --inplace
"""

from distutils.core import setup #type: ignore
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("code.pyx")
)