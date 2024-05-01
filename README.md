# Final Project

[![Run Pytest](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/unit-tests.yml)

[![Server Test](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/test-server.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/test-server.yml)

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## Link to App

[https://octopus-app-a6p6s.ondigitalocean.app/](https://octopus-app-a6p6s.ondigitalocean.app/)

## Instructions for Running

The [Docker image](./Dockerfile) is hosted on [Docker Hub](https://hub.docker.com/r/josckar/word-game-flask).

To run the server on port 5000:

```
docker build -t flask-app .

docker run -p 5000:5000 flask-app
```

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
