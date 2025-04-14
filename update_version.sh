#/bin/bash
VERSION=$1
new_line_py="__version__ = \"$VERSION\""
new_line_toml="version = \"$VERSION\""
new_line_nix="version = \"$VERSION\";"
new_line_cl="## $VERSION"
init=coinmetrics/__init__.py
pyproject=pyproject.toml
nix_default=default.nix
changelog=CHANGELOG.md

cat $init | while read line; do

  if [[ $line =~ "__version__ = " ]]; then sed -i '' -e "s/$line/$new_line_py/" $init
  fi

done < $init

cat $pyproject | while read line; do
  if [[ $line =~ "version = " ]]; then sed -i '' -e "s/$line/$new_line_toml/" $pyproject
  fi

done < $pyproject

cat $nix_default | while read line; do
  if [[ $line =~ "version = " ]]; then sed -i '' -e "s/$line/$new_line_nix/" $nix_default
  fi

done < $nix_default

cat $changelog | while read line; do

  if [[ $line =~ "## __version__" ]]; then sed -i '' -e "s/$line/$new_line_cl/" $changelog
  fi

done < $changelog
