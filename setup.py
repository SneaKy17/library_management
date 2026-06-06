# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="library_management",
	version="0.0.1",
	description="Library Management System for ERPNext",
	author="Nikhil Saklani",
	author_email="nikhilsaklani@example.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
