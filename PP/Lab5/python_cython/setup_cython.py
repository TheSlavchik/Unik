from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    "vector_wrapper",
    sources=["vector_wrapper.pyx", "vector_dot.c"],
    include_dirs=["."]
)

setup(
    ext_modules=cythonize(ext, compiler_directives={'language_level': "3"})
)
