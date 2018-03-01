#!/bin/sh

# Change to the analyser directory to avoid any complications with relative paths
cd `dirname $0`

# Run unit tests
python3 -m unittest discover -s tests
if [ $? -ne 0 ]
then
    echo "Unit tests failed - aborting!"
    exit 3
fi

# Calculate coverage
coverage run --source=. -m unittest discover -s tests/
coverage report --fail-under=95 --omit=static_analyser.py,tests/** -m
if [ $? -ne 0 ]
then
    echo "Insufficient code coverage, must be above 95% - aborting!"
    exit 3
fi
