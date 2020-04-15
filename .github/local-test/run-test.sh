#!/usr/bin/env sh

NC='\033[0m'
RED='\033[0;31m'
ORANGE='\033[0;33m'
GREEN='\033[0;32m'

if [ "$MAXMIND_LICENSE_KEY" = "" ] ; then
   echo "${ORANGE} Warning: Environment variable for MAXMINDDB could not be found, proceeding without it, check README file "
fi
# change directory to /richkit

cd /richkit

echo "${GREEN}1. Checking flake8 linting ... "
 # test that number of violations does not increase
FLAKE8_ERROR_CNT=$(flake8 . -qq --count --exit-zero --max-complexity=10 --max-line-length=127 --exclude venv,__pycache__,docs/source/conf.py,old,build,dist)
FLAKE8_ERROR_LIMIT=25
if [ "$FLAKE8_ERROR_CNT" -gt "$FLAKE8_ERROR_LIMIT" ] ; then
  echo "${RED}Failed because the number of errors from flake8 increased (This: $FLAKE8_ERROR_CNT Previously: $FLAKE8_ERROR_LIMIT)" 1>&2
  false
  exit 1
fi
echo "${ORANGE}Number of validation errors from flake8 is: $FLAKE8_ERROR_CNT (Limit is: $FLAKE8_ERROR_LIMIT)"


echo "${GREEN}2. Testing module .... "
echo "${NC}"
coverage run --source=richkit -m pytest -Werror /richkit/richkit

