from os.path import dirname, join

from setuptools import find_packages, setup

readme = join(dirname(__file__), 'README.md')
requirements = join(dirname(__file__), 'requirements.txt')

with open(readme) as file:
    readme_content = file.read()

requirements_exclude_list = {'flake8', 'mypy'}

with open(requirements) as file:
    requirements_content = file.read() + '\n'
    requirements = [line.strip() for line in requirements_content.splitlines() if line.strip()]
    requirements = [package for package in requirements
                    if not package.split('=')[0].split('>')[0].split('<')[0] in requirements_exclude_list]


__version__ = '2020.01.01.00.00.00-alpha'

packages = find_packages()
print(packages)

setup(
    name='coinmetrics-api-client',
    packages=packages,
    version=__version__,
    description='Alpha Release for official Python Client for Coin Metrics API',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    author='Oleksandr Buchkovsky',
    author_email='oleksandr@coinmetrics.io',
    url='https://github.com/coinmetrics-io/api-client-python',
    keywords=['coin-metrics', 'coin', 'metrics', 'crypto', 'bitcoin', 'network-data', 'market-data',
              'for-humans', 'fast', 'bigdata', 'api', 'handy'],
    install_requires=requirements,
)
