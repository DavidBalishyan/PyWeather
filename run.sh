#!/bin/bash

# Create python virtual enviroment
python3 -m venv venv
# activate virtual enviroment
source venv/bin/activate    
# install requirements.txt
pip3 install -r requirements.txt
# Run the project
python3 main.py