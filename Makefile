.PHONY: install tests flake run

run:
	python3 manager.py

tests:
	coverage run -m pytest ./tests; make clean

coverage:
	make tests
	coverage report | grep -v "100%"

flake:
	python3 -m flake8 .

clean:
	rm -rf .pytest_cache
	rm -rf tests/*/.pytest_cache
