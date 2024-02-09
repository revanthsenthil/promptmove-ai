from setuptools import setup, find_packages


def get_requirements(path: str):
    return [l.strip() for l in open(path)]


setup(
    name='promptmove-ai',
    packages=find_packages(),  # automatically find all packages
    version='0.1',
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=get_requirements("requirements.txt")
)