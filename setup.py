import setuptools
from setuptools.extension import Extension
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='datathon_tools',  
    version='0.1',
    author="Demetrio Magatti",
    description="Package containing simple functions used for ESICM data exploration and analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)