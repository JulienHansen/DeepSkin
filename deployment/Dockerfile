FROM python:latest

WORKDIR /app

ARG GOOGLE_CREDENTIALS

COPY deployment/format.py /app/format.py

# Copier et vérifier le fichier credentials
COPY credentials.json /app/credentials.json

# Formater le fichier JSON
RUN python /app/format.py /app/credentials.json

# Vérifier le formatage
RUN python -m json.tool /app/credentials.json

# Set the environment variable for Google Cloud credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

COPY deployment/ /app/deployment/
COPY models/ /app/models/

RUN pip install --no-cache-dir -r deployment/requirements.txt

EXPOSE 5100

ENTRYPOINT ["python", "-m", "deployment.main"]
