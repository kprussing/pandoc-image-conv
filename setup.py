#!/usr/bin/env python3
import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst"), "r") as fid:
    long_description = fid.read()

setup(
    name = "pandoc-image-conv",
    version = "0.2",

    description = "Convert Images in Pandoc AST to a Reasonable Format",
    long_description = long_description,
    keywords = "pandoc, filter, image, scons",

    author = "Keith F Prussing",
    author_email = "kprussing74@gmail.com",
    maintainer = "Keith F Prussing",
    maintainer_email = "kprussing74@gmail.com",

    url = "https://github.com/kprussing/pandoc-image-conv",
    dowload_url = "https://github.com/kprussing/pandoc-image-conv/releases",
    license = "MIT",

    install_requires = ["panflute >= 1.11.0"],

    py_modules = ["pandoc_image_conv"],
    entry_points = {
        "console_scripts" : {
            "pandoc-image-conv = pandoc_image_conv:main",
        },
    },

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Filters',
    ],
)

