#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import pyqart

packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

setup(
    name='pyqart',
    keywords=['qrcode', 'qart'],
    version=pyqart.__version__,
    description='QArt Python implementation, '
                'see http://research.swtch.com/qart for details.',
    author='7sDream',
    author_email='7seconddream@gmail.com',
    license='MIT',
    url='https://github.com/7sDream/pyqart',

    install_requires=['pillow'],
    packages=packages,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    entry_points={
        'console_scripts': [
            'pyqr = pyqart.qr_entry:main',
            'pyqart = pyqart.qart_entry:main',
        ]
    }
)
