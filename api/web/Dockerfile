FROM python:3-slim
WORKDIR /app/api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "web_server:app", "--host", "0.0.0.0", "--port", "9101"]
