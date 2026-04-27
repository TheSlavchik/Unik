from setuptools import setup, Extension
from pathlib import Path
import os

current_dir = Path(__file__).resolve().parent
# Путь на уровень выше
parent_dir = current_dir.parent

core_dir = parent_dir / 'c_core'

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# core_dir = os.path.join(curr_dir, 'c_core')

module = Extension(
    'vector_lib',
    sources=[
        'vector_module.c',
        os.path.join(core_dir, 'vector_dot.c')
    ],

    include_dirs=[core_dir] 
)

setup(
    name='vector_lib',
    version='1.0',
    description='Python C API wrapper for vector dot product',
    ext_modules=[module]
)

#python3 setup_cpython.py build_ext --inplace