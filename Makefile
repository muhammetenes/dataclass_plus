all: test

isort:
	isort -rc

tests:
	@pytest

cov:
	@PYTHONASYNCIODEBUG=1 pytest --cov=dataclass_plus
	@pytest --cov=dataclass_plus --cov-append --cov-report=html --cov-report=term
	@echo "open file://`pwd`/htmlcov/index.html"