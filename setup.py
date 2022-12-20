from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='python-screen',
    version='1.0.3',
    packages=['pyscreen'],
    url='https://gitlab.com/jvadair/pyscreen',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache 2.0',
    author='jvadair',
    author_email='dev@jvadair.com',
    description='A simple python wrapper for GNU Screen'
)
