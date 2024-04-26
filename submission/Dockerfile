# Use an official Python runtime as a parent image
FROM autogluon.base:latest

# Identify as root user
USER root

# Set the working directory in the container
WORKDIR /root/src/app

# Copy the modified file into the Docker image
COPY app.py /root/src/app

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run script.py when the container launches
ENTRYPOINT ["python", "./app.py"]