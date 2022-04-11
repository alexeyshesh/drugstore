.PHONY: install tests flake run install winstall wrun

install:
	pip3 install -r requirements.txt

winstall:
	pip install -r requirements.txt

run:
	python3 manager.py

wrun:
	python manager.py

tests:
	python3 -m pytest ./tests

coverage:
	make tests
	coverage report | grep -v "100%"

flake:
	python3 -m flake8 .

clean:
	rm -rf .pytest_cache
	rm -rf tests/*/.pytest_cache
