# Northwind API

Simple REST API with data from Northwind database. Application in available on Heroku:

`https://northwind-api.herokuapp.com/`

## Technologies

* Python 3.8
* FastAPI
* PostgreSQL database
* SLQAlchemy ORM
* Pytest

## Setup

To run this project install dependencies using Pipenv for production environment:

`$ pipenv install --ignore-pipfile`

or development environment:

`$ pipenv install --dev`

Finally, run application with Uvicorn:

`$ uvicorn main:app`
