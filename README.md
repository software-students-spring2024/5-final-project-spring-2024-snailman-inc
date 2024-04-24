# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## Instructions

Install dependencies with `python -m pip install -r requirements.txt -r app/requirements.txt`

To run the development server, run `python app/app.py`

To run the production server, run `gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app`

## Teammates

* [Corina Luca](https://github.com/CorinaLucaFocsan)
* [Jakob Hablitz](https://github.com/jsh9965)
* [Josckar Palomeque-Elias](https://github.com/josckar)
* [Stella Zhang](https://github.com/qq3173732005)
