from setuptools import setup
from Cython.Build import cythonize
import numpy as np

setup(
    name='vector_dot_cython',
    ext_modules=cythonize("vector_dot_cython.pyx"),
    include_dirs=[np.get_include(), '.']
)

# python setup_cython.py build_ext --inplace