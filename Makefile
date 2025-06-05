all:
	ruff check src
	mypy src
	pytest tests
	mutmut run

.PHONY: all
