# Use the official Python image as the base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the 'deployment' and 'models' directories into the container
COPY deployment/ /app/deployment/
COPY models/ /app/models/

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r deployment/requirements.txt

# Expose port 8080 to allow external access
EXPOSE 5100

# Command to run the application using Waitress
ENTRYPOINT ["python", "-m", "deployment.main"]

