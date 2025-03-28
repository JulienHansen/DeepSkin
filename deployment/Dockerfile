# Utiliser l'image officielle de Python comme base
FROM python:latest





# Définir le chemin du fichier credentials dans le conteneur
ARG CRED_FILE
ENV CRED_FILE_PATH=/app/credentials.json

# Définir la variable d'environnement pour les credentials Google Cloud
ENV CRED_FILE_PATH=/app/credentials.json
ENV GOOGLE_APPLICATION_CREDENTIALS=${CRED_FILE_PATH}

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier le fichier de credentials dans le conteneur
ARG CRED
RUN echo "$CRED" > ${CRED_FILE_PATH}

RUN echo "Contenu du fichier credentials.json :" && cat ${CRED_FILE_PATH}

# Afficher le contenu du fichier de credentials pour vérifier s'il est bien copié (Uniquement pour debug, à retirer en production)
#RUN echo "Contenu du fichier credentials.json :" && cat ${CRED_FILE_PATH}

# Copier les répertoires deployment et models dans le conteneur
COPY deployment/ /app/deployment/
COPY models/ /app/models/

# Exposer le port 5100 pour les connexions externes
EXPOSE 5100

# Installer les dépendances listées dans requirements.txt
RUN pip install --no-cache-dir -r deployment/requirements.txt

# Commande pour lancer l'application
ENTRYPOINT ["python", "-m", "deployment.main"]
