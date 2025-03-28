FROM python:latest

WORKDIR /app

ARG GOOGLE_CREDENTIALS

#Vérifie que GOOGLE CREDIENTALS n'est pas nul et crée le fichier
RUN if [ -n "$GOOGLE_CREDENTIALS" ]; then \ 
        echo "$GOOGLE_CREDENTIALS" | base64 -d > /app/credentials.json; \
    fi

RUN chmod 777 /app/credentials.json
RUN cat /app/credentials.json

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

COPY deployment/ /app/deployment/
COPY models/ /app/models/

RUN pip install --no-cache-dir -r deployment/requirements.txt

EXPOSE 5100

ENTRYPOINT ["python", "-m", "deployment.main"]