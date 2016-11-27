
NOSE_OPTIONS = --plugin nose2.plugins.doctests --with-doctest

default: test

clean:
	find . -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .coverage htmlcov

test: FORCE
	nose2 $(NOSE_OPTIONS)

unittest: FORCE
	nose2 $(NOSE_OPTIONS) test.unit

coverage: FORCE
	nose2 $(NOSE_OPTIONS) test.unit -C  --coverage ezvalue/__init__.py --coverage-report html
	@sed -n 's/.*<span class="pc_cov">\(100%\)<\/span>.*/\nCoverage: \1\n/ p' htmlcov/index.html

FORCE:
