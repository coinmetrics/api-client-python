from os.path import dirname, join

from setuptools import find_packages, setup

readme = join(dirname(__file__), 'README.md')
requirements = join(dirname(__file__), 'requirements.txt')

with open(readme) as file:
    readme_content = file.read()

with open(requirements) as file:
    requirements_content = file.read() + '\n'

__version__ = '2020.01.01.00.00.00'

packages = find_packages()
print(packages)

setup(
    name='coinmetrics-api-client',
    packages=packages,
    version=__version__,
    description='Beta Python Client for Coin Metrics API',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    author='Oleksandr Buchkovsky',
    author_email='oleksandr@coinmetrics.io',
    # url='',
    keywords=['coin-metrics', 'coin', 'metrics', 'for-humans', 'fast', 'bigdata', 'api', 'handy'],
    install_requires=[line.strip() for line in requirements_content.splitlines() if line.strip()],
)
