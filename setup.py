from setuptools import setup, find_packages

setup(
    name='promptmove-ai',
    packages=find_packages(),  # automatically find all packages
    version='0.1',
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'pip',
        'numpy',
        'matplotlib',
        'pandas',
    ],  # list your dependencies here
)