# Final Project

[![Run Pytest](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/unit-tests.yml)

[![Server Test](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/test-server.yml/badge.svg)](https://github.com/software-students-spring2024/5-final-project-spring-2024-snailman-inc/actions/workflows/test-server.yml)

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## About the Game

**wrdl**: A deceptively difficult word game. 16 letters are given, from which the player must recreate 4 words of length 4. Add friends and compare the number of boards you've won.

Play now at [https://octopus-app-a6p6s.ondigitalocean.app/](https://octopus-app-a6p6s.ondigitalocean.app/).

## Instructions for Running

The [Docker image](./Dockerfile) is hosted on [Docker Hub](https://hub.docker.com/r/josckar/flask-word-game).

### Configuring Environment Variables

MONGO_DB=\[*Name of your MongoDB database*\]

MONGO_URI=\[*URI of your MongoDB database*\]

SECRET_KEY=\[*Your secret key*\]

### Running the Server

To run the server on port 5000:

```
docker build -t flask-app .

docker run -p 5000:5000 flask-app
```

### [Pytest](https://docs.pytest.org/en/stable/)

In the project root: to run tests using pytest, build the dockerfile with:
```bash
docker build -t test-image -f PytestDockerfile .
```
`MONGO_URI` and `MONGO_DB` environment variables must be specified. If using a `.env` file created in the root directory, you can run the following command to test the server:
```bash
docker run --env-file .env test-image
```
## Teammates

* [Corina Luca](https://github.com/CorinaLucaFocsan)
* [Jakob Hablitz](https://github.com/jsh9965)
* [Josckar Palomeque-Elias](https://github.com/josckar)
* [Stella Zhang](https://github.com/qq3173732005)
