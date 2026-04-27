from setuptools import setup, Extension

module = Extension(
    'vector_lib',
    sources=['vector_module.c', 'vector_dot.c']
)

setup(
    name='vector_lib',
    version='1.0',
    description='Python C API wrapper for vector dot product',
    ext_modules=[module]
)

#python3 setup_cpython.py build_ext --inplace