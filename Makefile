PYTHON ?= python

.PHONY: install test lint typecheck check run

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m flake8 .

typecheck:
	$(PYTHON) -m mypy .

check: test lint typecheck

run:
	$(PYTHON) main.py
