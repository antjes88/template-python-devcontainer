#!/bin/bash

set -e

printf "\n \e[32mSetting up Python environment...\e[0m\n"
rm -rf venv
python3.10 -m venv ./venv
source ./venv/bin/activate
printf "\n \e[32mPython environment created.\e[0m\n"


printf "\n \e[32mInstalling Python packages...\e[0m\n"
pip install --upgrade pip
pip install -r requirements.txt
if [ "$ISDEVCONTAINER" == "true" ]; then
    pip install -r dev-requirements.txt
fi
FILE="cli-requirements.txt" # Do you need CLI capabilities?
if [ -f "$FILE" ]; then
    pip install -r "$FILE"
fi
FILE="webapp-requirements.txt" # Do you need a web app?
if [ -f "$FILE" ]; then
    pip install -r "$FILE"
fi
printf "\n \e[32mPython packages installed.\e[0m\n"