
clean:
	rm -rf dist/ build/ *.egg-info

build:
	python3 -m build

install:
	pip3 install dist/*.whl --force-reinstall

publish:
	twine upload dist/*
