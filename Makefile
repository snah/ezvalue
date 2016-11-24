
default: test

clean:
	find . -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .coverage htmlcov

test:
	nose2

unittest:
	nose2 test.unit

coverage:
	nose2 -C  --coverage ezvalue/__init__.py --coverage-report html
