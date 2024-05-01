# Use a base image with Python installed
FROM python:3.10-slim

# Install Poetry
RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$PATH:/root/.local/bin/"

# Set the working directory in the container
WORKDIR /app

# Copy only the poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install project dependencies
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the local code to the container
COPY . .

# Expose the port Flask app runs on
EXPOSE 5000

# Command to run the Flask app using Gunicorn
CMD ["poetry", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
