#!/bin/bash

if [ ! which pylint &> /dev/null ];then
  echo "no pylint installed"
  echo "run:"
  echo "source bin/activate"
  echo "pip install pylint"
  exit 0
fi

pylint -E report-api
# Simple script to run pylint test. This is the same tests travis use.

#find . -maxdepth 1 -type f  \( -iname "*.py" ! -iname "setup.py" \)  | xargs pylint -E
