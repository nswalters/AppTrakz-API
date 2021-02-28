#!/bin/bash

rm -rf apptrakzapi/migrations
rm db.sqlite3
python manage.py makemigrations apptrakzapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata profiles
python manage.py loaddata social_media_types
python manage.py loaddata social_medias
python manage.py loaddata companies
python manage.py loaddata jobs
python manage.py loaddata applications
python manage.py loaddata statuses
python manage.py loaddata application_statuses
python manage.py loaddata job_notes
python manage.py loaddata company_notes
python manage.py loaddata contacts
python manage.py loaddata job_contacts
python manage.py loaddata contact_notes