#!/usr/bin/env python
# coding: utf-8

r"""ydeos_weights's setup.py."""

from distutils.core import setup

import ydeos_weights


setup(name=ydeos_weights.__project_name__,
      version=ydeos_weights.__version__,
      description=ydeos_weights.__description__,
      long_description='Weights model',
      url=ydeos_weights.__url__,
      download_url=ydeos_weights.__download_url__,
      author=ydeos_weights.__author__,
      author_email=ydeos_weights.__author_email__,
      license=ydeos_weights.__license__,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.7'],
      keywords='weight weights',
      packages=['ydeos_weights'])
