rm -rf dist/
rm -rf build/
rm -rf main.spec
pyinstaller -w -F main.py
cp -a templates dist/main/templates