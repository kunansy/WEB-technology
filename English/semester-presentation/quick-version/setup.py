from distutils.core import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize('calc.pyx')
)

# pip install -U cython
# python setup.py build_ext --inplace
