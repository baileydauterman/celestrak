# Celestrak Scraper and API
Basic project to test scraping API endpoints and serving data via an API (web or tcp socket).
```
docker-compose -up -d --build
```

## Scrapers
All scrapers use the [celestrak.py](./scrapers/celestrak.py) file to pull data from the celestrak API and write it to a Docker volume.
I think there is a much better way to do this by allowing the celestrak.py to take parameter args and then it could be called from docker.

Current example of writing data to the Docker volume:
[tle_nav_sats.py](./scrapers/nav/tle_nav_sats.py)

## API
### Web
REST based API example to serve responses to basic input.

#### .env file
Required for the docker compose to define port and host to serve data on.

### TCP
Work in progress.
