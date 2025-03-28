# Use the official Python image as the base image
FROM python:latest

#ARG CRED

ARG CRED_FILE
ENV CRED_FILE_PATH /app/credentials.json

#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json
# Set the working directory inside the container
WORKDIR /app

# Copy the credentials file into the container
COPY ${CRED_FILE} ${CRED_FILE_PATH}

# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS=${CRED_FILE_PATH}

#RUN cat ${CRED_FILE_PATH}

# Créer le fichier credentials.json à partir de la clé
#RUN echo "$CRED" > /app/credentials.json

# Définir la variable d'environnement pour les credentials Google Cloud
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json

# Set the environment variable for Google Cloud credentials
#ENV GOOGLE_APPLICATION_CREDENTIALS=${CRED}

# Créer un fichier credentials.json dans le conteneur et copier le fichier source
#COPY ${CRED} /app/credentials.json

# Afficher le contenu de la clé dans le fichier (attention à la sécurité)
RUN echo "Contenu de la clé : $(CRED)"

# Copy the contents of the 'deployment' and 'models' directories into the container
COPY deployment/ /app/deployment/
COPY models/ /app/models/

# Expose port 5100 to allow external access
EXPOSE 5100

# Install the dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r deployment/requirements.txt

# Command to run the application
ENTRYPOINT ["python", "-m", "deployment.main"]
