# Use the official Python image as the base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the current directory (deployment) into the container's working directory
# Copy the 'deployment' directory contents
COPY deployment/ /app/deployment/

# Copy the 'models' directory contents
COPY models/ /app/models/

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r deployment/requirements.txt


# Command to run the application using Gunicorn
ENTRYPOINT [ "python" ]
CMD ["-m", "deployment.main"]

