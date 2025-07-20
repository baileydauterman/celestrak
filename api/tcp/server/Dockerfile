FROM python:3-slim
WORKDIR /app/tcp_server
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "tcp_server.py", HOST, PORT]
