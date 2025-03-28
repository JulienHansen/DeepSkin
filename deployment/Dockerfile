# Use the official Python image as the base image
FROM python:latest

ARG CRED

# Set the working directory inside the container
WORKDIR /app

# Copy the service account JSON file into the container (adjust the file name/path as needed)
#COPY credentials.json /app/credentials.json

# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=${CRED}

# Copy the contents of the 'deployment' and 'models' directories into the container
COPY deployment/ /app/deployment/
COPY models/ /app/models/

# Expose port 5100 to allow external access
EXPOSE 5100

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r deployment/requirements.txt

# Command to run the application
ENTRYPOINT ["python", "-m", "deployment.main"]
