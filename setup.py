#!/usr/bin/env python

from setuptools import *
setup(
	name='unfluff',
	version='0.1',
	author_email='tim3d.junk+unfluff@gmail.com',
	author='Tim Cuthbertson',
	url='http://github.com/gfxmonk/unfluff',
	description="HTML content extraction - remove the fluff",
	packages = find_packages(exclude=['test', 'test.*']),
	entry_points = {
		'console_scripts':   ['unfluff = unfluff:main'],
	},
	keywords='html content extraction',
	license='BSD',
	zip_safe=True,
	install_requires=[
		'setuptools',
		'scipy',
		'lxml',
	],
)
