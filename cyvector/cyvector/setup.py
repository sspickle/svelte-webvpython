from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np

setup(name='cyvector',
      version='0.1',
      ext_modules = cythonize(Extension("cyvector", ["cyvector.pyx"],
      include_dirs=[np.get_include()])))
