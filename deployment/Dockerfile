# Python image
FROM python:latest

# Working Directory
WORKDIR /app


COPY . . 


# Dependencies
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8080

# Run command
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app.main:app"]
