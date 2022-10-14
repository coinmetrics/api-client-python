#/bin/bash
VERSION=`python get_utc_update_time.py`
new_line_py="__version__ = \"$VERSION\""
new_line_toml="version = \"$VERSION\""
init=coinmetrics/__init__.py
pyproject=pyproject.toml
cat $init | while read line; do

  if [[ $line =~ "__version__ = " ]]; then sed -i '' -e "s/$line/$new_line_py/" $init
  fi

done < $init
cat $pyproject | while read line; do
  if [[ $line =~ "version = " ]]; then sed -i '' -e "s/$line/$new_line_toml/" $pyproject
  fi

done < $pyproject
