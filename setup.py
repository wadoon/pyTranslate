#!/usr/bin/env python

import sys
from distutils.core import setup

setup(name='pyTranslate',
      version='1.0',
      description='translate input from one to another language',
      long_description="""\
      Uses Google Language Api for translating
      ...
      """,
      author='Alexander Weigl',
      author_email='alexweigl@gmail.com',
      url='http://areku.kilu.de',
      scripts=['translate.py'],
      py_modules=['translate'],
      provides=['translate (1.0)'],
	)
