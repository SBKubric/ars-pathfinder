#!/bin/bash
if ! command -v python3 &> /dev/null
then
  echo "Python could not be found. Aborting..."
  exit 1
fi

poetry_export_installed=false

# Check if poetry is installed
if ! command -v poetry &> /dev/null
then
   echo "Poetry could not be found. Installing..."
   # Install pipx
   if ! command -v pipx &> /dev/null
   then
      python3 -m pip install pipx --user
   fi
   # Install poetry
   pipx install poetry
   pipx inject poetry poetry-plugin-export
   if [ $? -e 0 ]; then
      poetry_export_installed=true
      poetry config warnings.export false
   fi
fi

# Ensure that virtualenv is located at .venv
poetry config virtualenvs.in-project true --local


# Run poetry install for dev stand
bash ./compose/local/install.sh

poetry run pre-commit install --hook-type pre-push --hook-type pre-merge-commit --hook-type pre-commit

# Check that plugin was installed and print error message
RED='\033[0;31m'
NC='\033[0m' # No Color
if [ "$poetry_export_installed" = false ]; then
   printf "\n\n${RED}Failed to add poetry-plugin-export.\n\n"
   printf "Try to install it manually. Docs are located at:\n"
   printf "https://github.com/python-poetry/poetry-plugin-export${NC}\n"
fi
