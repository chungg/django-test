# How is My Team?
A simple Django application to allow daily checkins and monitoring of your teams happiness.

## Setup

in the directory you've pulled code into:
* install requirements: pip install -r requirements.txt
* set a SECRET_KEY value in testsite/settings.py

## Running

* initialise the database: python manage.py migrate
* create an admin user: python manage.py createsuperuser
* launch a test server: python manage.py runserver
* browse to localhost:8000/admin and add users
* use localhost:8000/polls to interact with happyiness app
* use localhost:8000/polls/results to see results without voting

## Testing

* install tox: pip install tox
* pep8: tox -epep8
* unit tests: tox -epy27

## Notes

* date is set to UTC. voting resets when date changes relative to UTC
* if a user is not part of a group, they can see everything.
