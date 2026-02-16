install:
	pip install poetry
	poetry install

run:
	python3 a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ mypy_cache__ .mypy_cache

setup:
	python setup.py sdist bdist_wheel

lint:
	flake8 .
	mypy . --warn-return-any \
	--warn-unused-ignores \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict