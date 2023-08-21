# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set environment variables (replace /path/to/your/module with the actual path)
ENV PYTHONPATH=/usr/src/app

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt
