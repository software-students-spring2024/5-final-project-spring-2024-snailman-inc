# Use a base image with Python installed
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local code to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir -r app/requirements.txt

# Expose the port Flask app runs on
EXPOSE 5000

# Command to run the Flask app using Gunicorn
CMD ["python","-m", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
