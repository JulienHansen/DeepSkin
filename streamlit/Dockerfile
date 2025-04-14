FROM python:latest

WORKDIR /app

# Copy the full streamlit directory including any subfolders like .github
COPY streamlit/ /app/streamlit/

# Explicitly copy the .github folder if it’s outside of the streamlit folder
COPY .github/ /app/.github/

EXPOSE 8501

RUN pip install --no-cache-dir -r streamlit/requirements.txt

CMD ["streamlit", "run", "streamlit/main.py"]
