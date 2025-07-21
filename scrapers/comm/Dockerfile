FROM python:3-slim
WORKDIR /app/misc
COPY --from=scrapers requirements.txt .
COPY --from=scrapers celestrak.py .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "celestrak.py", "comm"]
