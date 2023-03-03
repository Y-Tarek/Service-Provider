# Service-Provider
Api and Admin dashboard for service providers to host their services and manage orders from clients.

## API Documentation
https://documenter.getpostman.com/view/20343410/2s8YzZQzWg

## Prerequisite
>python (3.9 prefered)

>postgressql

## Installtion
   If you have docker installed you can run the docker image provided inside the application by just running:
             
             docker-compose up --build
             Then go to (http://127.0.0.1:8888/admin) for admin dashboard and (http://127.0.0.1:8888/api) for api interface provided by django rest framework.
             username and password for admin dashboard found in runserver.sh file.
   Or you can run it manually by:
   
         1- create database called (sorror) in postgres db or any name you desire just change it in project/settings.py SQL_DB environment variable.
         2- go inside the application and create virtual env to host the application requirements by running: (python -m venv venv).
         3- install the application required packages provided in requirements.txt file by running: (pip install -r requirememnts.txt).
         4- Run python manage.py makemigrations.
         5- Run python manage.py migrate.
         6- Run python manage.py createsuperuser (required for logining to admin dashboard).
              will ask for mobile phone , name and password
         7- Run python manage.py runserver.
         
