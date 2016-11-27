
PYTHON_FILES = ezvalue/__init__.py

NOSE_OPTIONS = --plugin nose2.plugins.doctests --with-doctest

default: coverage lint

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

lint: fix-whitespace
	@pylama test --ignore W0612 || true
	@pylama ezvalue || true

%.fixed_whitespace: %
	@if grep '^\s\+$$' --quiet $<; then sed -i 's/^\s\+$$//' $<; fi

fix-whitespace: $(addsuffix .fixed_whitespace, $(PYTHON_FILES))

FORCE:
