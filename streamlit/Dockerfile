FROM python:latest

WORKDIR /app

COPY streamlit/ /app/streamlit/

EXPOSE 8501

RUN pip install --no-cache-dir -r streamlit/requirements.txt

CMD ["streamlit", "run", "streamlit/main.py"]
