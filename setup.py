from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(name='hdf5storage',
      version='0.1',
      description='Utilities to read/write Python types to HDF5 files.',
      long_description=long_description,
      author='Freja Nordsiek',
      author_email='fnordsie at gmail dt com',
      url='https://github.com/frejanordsiek/hdf5storage',
      packages=['hdf5storage'],
      requires=['numpy', 'h5py (>= 2.0)'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "Development Status :: 3 - Alpha",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering",
          "Topic :: Database",
          "Topic :: Software Development :: Libraries :: Python Modules"
          ]
      )