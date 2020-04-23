.PHONY: all prep-dev venv clean lint test docker-test

# virtual environment for development
VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3
# help messages for make, it runs in `make` or `make all`
all:
	@echo "\033[92m make prep-dev \033[0m"
	@echo "---> Prepares dev environment, use only once"
	@echo "\033[92m make test \033[0m"
	@echo "---> Runs test cases in virtual environment"
	@echo "\033[92m make lint \033[0m"
	@echo "---> Linting project with autopep8"
	@echo "\033[92m make clean \033[0m"
	@echo "---> Cleans project cache and other stuffs"
	@echo "\033[92m make docker-test \033[0m"
	@echo "---> Runs test cases in docker environment"


prep-dev:
	python3 -m pip install virtualenv  ## virtual environment for development purposes
	make venv

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements.txt
		test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
		${PYTHON} -m pip install -U pip setuptools
		${PYTHON} -m pip install -U autopep8  coverage  isort
		${PYTHON} -m pip install -U -r requirements.txt
		touch $(VENV_NAME)/bin/activate

clean:
	rm -rf $(VENV_NAME) *.eggs *.egg-info dist build docs/_build .cache .coverage
	rm -rf .pytest*  # cache file for Intellij PyCharm

sort: venv
	isort -rc . --skip_glob docs/*


lint: venv
	autopep8 --in-place --recursive --max-line-length=100 --exclude docs/source/conf.py,venv,__pycache__,old,build,dist .

test: venv
	coverage run --source=richkit -m pytest -Werror --ignore src/python-whois

docker-test: clean
	docker build -t richkit-docker-test -f Dockerfile.test .
	docker run -e MAXMIND_LICENSE_KEY=$MAXMIND_LICENSE_KEY richkit-docker-test