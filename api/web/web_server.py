from datetime import datetime
from fastapi import FastAPI
from faker import Faker
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()
fake = Faker()

@app.get("/ping")
async def ping():
    return {
 	"pong": datetime.now()
    }

@app.get("/")
async def get():
    return "Hello, World!"

@app.get("/random")
async def person():
    return {
            "name": fake.name(),
            "address": fake.address(),
            "email": fake.email()
        }

@app.get("/profile")
async def profile():
    return fake.profile()

@app.get("/currentTime")
async def get_current_time():
    return datetime.now()


@app.get("/nav")
async def get_nav_sat_data(format: str, navSat: str):
    date = datetime.now().date().isoformat()
    path = f"/data/nav/{date}-{navSat}.{format}"
    if os.path.exists(path):
        with open(path) as f:
            return PlainTextResponse(f.read())

    return None