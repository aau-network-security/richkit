#!/usr/bin/env sh

export MAXMIND_LICENSE_KEY="<licence_key_should_be_added_here>"

# change directory to /richkit

cd /richkit

echo "1. Checking flake8 linting ... "
 # test that number of violations does not increase
FLAKE8_ERROR_CNT=$(flake8 . -qq --count --exit-zero --max-complexity=10 --max-line-length=127 --exclude venv,__pycache__,docs/source/conf.py,old,build,dist)
FLAKE8_ERROR_LIMIT=25
if [ "$FLAKE8_ERROR_CNT" -gt "$FLAKE8_ERROR_LIMIT" ] ; then
  echo "Failed because the number of errors from flake8 increased (This: $FLAKE8_ERROR_CNT Previously: $FLAKE8_ERROR_LIMIT)" 1>&2
  false
  exit 1
fi
echo "Number of validation errors from flake8 is: $FLAKE8_ERROR_CNT (Limit is: $FLAKE8_ERROR_LIMIT)"


echo "2. Testing module .... "
coverage run --source=richkit -m pytest -Werror /richkit/richkit

