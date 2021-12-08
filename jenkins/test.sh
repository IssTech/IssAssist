#!/usr/bin/env bash


# Install all our requirements
pip install -r requirements.txt

# Set all our Environment variables
export DEBUG=False

# Sync our database and test our Django App with Jenkins test
cd ./src
python manage.py makemigrations
python manage.py migrate
python manage.py jenkins
