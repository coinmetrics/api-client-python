# Contributing guidelines


## Setting up env
```
conda create -n api-client-python python=3.8

activate api-client-python

pip install poetry
poetry install
```

Commands you should run before merging your changes into master
```
python -m mypy -p coinmetrics
python -m black coinmetrics test
python -m flake8 coinmetrics
python -m pytest test

poetry export --without-hashes --format=requirements.txt > requirements.txt
```


## Publishing package to pypi

```
poetry build && poetry publish
```


## GENERATING DOCUMENTATION

```
pydoc-markdown -m coinmetrics.api_client > docs\docs\api_client.md

cp -f README.md docs\docs\index.md
cd docs && mkdocs build && cd ..
```
