import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# Thanks https://realpython.com/pypi-publish-python-package/
setup(
	name="adderlib",
	version="1.0.3",
	python_requires=">=3.7",
	description="Python wrapper for the Adder API, for use with Adderlink KVM systems",
	long_description=README,
	long_description_content_type="text/markdown",
	url="https://adderlib.readthedocs.io/",
	download_url="https://github.com/mjiggidy/adderlib/",
	author="Michael Jordan",
	author_email="michael@glowingpixel.com",
	license="GNU General Public License v3 or later (GPLv3+)",
	classifiers=[
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: System Administrators",
		"Topic :: Multimedia",
		"Topic :: Internet",
		"Topic :: Utilities",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.9",
		"Natural Language :: English"
	],
	packages=["adderlib"],
	include_package_data=True,
	install_requires=["requests", "xmltodict==0.12.0"]
)