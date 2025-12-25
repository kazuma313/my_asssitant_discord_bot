from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import uvicorn
from threading import Thread

app = FastAPI()


@app.get("/")
def home():
    return PlainTextResponse("Bot is running!")


def run():
    uvicorn.run(app, host="0.0.0.0", port=8008)


def keep_alive():
    t = Thread(target=run)
    t.start()
