#!/bin/sh

coverage erase
python -m pytest --cov --cov-report term-missing || exit
#coverage report --fail-under="$COVERAGE_THRESHOLD" || exit
#coverage xml
