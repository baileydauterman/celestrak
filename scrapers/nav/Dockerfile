FROM python:3-slim
WORKDIR /app/tle
COPY --from=scrapers requirements.txt .
COPY --from=scrapers celestrak.py .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "tle_nav_sats.py"]
