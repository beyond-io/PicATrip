#!/bin/bash -ex
# The -e option would make our script exit with an error if any command
# fails while the -x option makes it verbosely output what it does

# Install Pipenv, the -n option makes sudo fail instead of asking for a
# password if we don’t have sufficient privileges to run it
sudo -n dnf install -y pipenv

cd /vagrant
# Install dependencies with Pipenv
pipenv sync --dev

#installing package for google fast signing
pipenv install django-allauth

# Run database migrations
pipenv run python manage.py migrate

# run our app. Nohup and "&" are used to let the setup script finish
# while our app stays up. The app logs will be collected in nohup.out
nohup pipenv run python manage.py runserver 0.0.0.0:8000 &
