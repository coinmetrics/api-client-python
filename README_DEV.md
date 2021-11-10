# Contributing guidelines


## Setting up env
Run these commands to set up your conda environment. We use `poetry` to manage dependencies as we make changes.
```
conda create -n api-client-python python=3.8

activate api-client-python

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install
```
_Install is taken from poetry documentation. For more information on poetry, see [their docs](https://python-poetry.org/docs/#updating-poetry)_

Alternatively, you may install poetry via `pip` and lock in dependencies from there:

```
pip install poetry
poetry install
```

But this is not recommended as you may run into dependency issues from doing so.

Commands you should run before merging your changes into master
```
python -m mypy -p coinmetrics
python -m black coinmetrics test
python -m flake8 coinmetrics
python -m pytest test

poetry export --without-hashes --format=requirements.txt > requirements.txt
```


## Publishing package to pypi
**NOTE: Run this only when you merge your changes into master and actually want to release the updates**
```
poetry build
poetry publish
```


## GENERATING DOCUMENTATION
#### Windows
```
pydoc-markdown -m coinmetrics.api_client > docs\docs\api_client.md

cp -f README.md docs\docs\index.md
cd docs 
mkdocs build 
cd ..
```

#### Mac
```
pydoc-markdown -m coinmetrics.api_client > docs/docs/api_client.md

cp -f README.md docs/docs/index.md
cd docs && mkdocs build && cd ..
```
