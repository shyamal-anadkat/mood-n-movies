install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black scripts/*.py main.py

lint:
	pylint --disable=R,C scripts/*.py main.py

clean: format lint
all: install format lint
ci: test format lint