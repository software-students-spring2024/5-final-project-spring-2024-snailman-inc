# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## Instructions

The [Docker image](./Dockerfile) is hosted on [Docker Hub](https://hub.docker.com/r/josckar/word-game-flask).

Install dependencies with `pythom -m pip install -r requirements.txt -r app/requirements.txt`

To run the development server, run `python app/app.py`

To run the production server, run `gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app`

### [Pytest](https://docs.pytest.org/en/stable/)

To run tests using pytest, run:

```bash
pytest
```
or for the Dockerized version
```bash
docker build -t test-image -f PytestDockerfile .
docker run test-image
```
from the project root

## Teammates

* [Corina Luca](https://github.com/CorinaLucaFocsan)
* [Jakob Hablitz](https://github.com/jsh9965)
* [Josckar Palomeque-Elias](https://github.com/josckar)
* [Stella Zhang](https://github.com/qq3173732005)
