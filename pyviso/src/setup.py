from distutils.core import setup, Extension
from distutils.sysconfig import get_config_vars
import numpy
import os

(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
    flag for flag in opt.split() if flag != '-Wstrict-prototypes'
)

setup(name="pyviso2",
      version="0.1.0",
      py_modules=["viso2"],
      ext_modules=[Extension("_viso2",
                             sources=["filter.cpp", "matcher.cpp", "matrix.cpp", "reconstruction.cpp",
                                      "triangle.cpp", "viso.cpp", "viso_mono.cpp", "viso_stereo.cpp", "viso2.i"],
                             language="c++",
                             swig_opts=['-c++', '-threads'],
                             extra_compile_args=['-msse3'],
                             include_dirs=[numpy.get_include()])])
