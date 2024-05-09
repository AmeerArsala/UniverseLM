# Use an official Python runtime as a parent image
FROM python:3.9.7-slim

# Set the working directory in the container to /project
WORKDIR /project

# Copy the current directory contents into the container at the working directory
COPY . .

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.2

# Install project dependencies
RUN poetry install

# Expose the port on which the application will run
EXPOSE 8080

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
