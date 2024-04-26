# Use an official Python runtime as a parent image
FROM python:3.11-slim
USER root
WORKDIR /root/src/app

# Copy the current directory contents into the container at /root/src/app
COPY requirements.txt /root/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt