from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name="gt",
      author="Gabor Vecsei",
      version="0.1",
      packages=["prometh"],
      install_requires=requirements,
      entry_points={"console_scripts": ["prometh = prometh.prometh_cli:main"]})
