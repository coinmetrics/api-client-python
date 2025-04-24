#/bin/bash
VERSION=$1

sed -i.bak -e "s/__version__ = .*/__version__ = \"$VERSION\"/" coinmetrics/__init__.py
sed -i.bak -e "s/version = .*/version = \"$VERSION\"/" pyproject.toml
sed -i.bak -e "s/version = .*/version = \"$VERSION\";/" default.nix
sed -i.bak -e "s/## __version__/## $VERSION/" CHANGELOG.md

rm -f coinmetrics/__init__.py.bak pyproject.toml.bak default.nix.bak CHANGELOG.md.bak
