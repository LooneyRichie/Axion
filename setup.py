from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="axion-lang",
    version="0.1.0",
    author="Axion Language Contributors",
    author_email="", 
    description="A lightweight experimental programming language built in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gershom-Benni/Axion",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'axion': ['stdlib/*.ax'],
    },
    entry_points={
        'console_scripts': [
            'axion=axion.cli:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Interpreters",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.8',
    keywords="programming-language interpreter axion",
    project_urls={
        "Bug Reports": "https://github.com/Gershom-Benni/Axion/issues",
        "Source": "https://github.com/Gershom-Benni/Axion",
    },
)
