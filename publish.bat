rd /s /q "dist"
python replace_version_in_setup_py.py
python setup.py sdist
twine upload --repository pypi dist/*