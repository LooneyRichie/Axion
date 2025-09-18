from setuptools import setup, find_packages

setup(
    name="axion",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'axion=axion.cli:main',
        ],
    },
    python_requires='>=3.10',
)
