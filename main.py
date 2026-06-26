from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, this is backend for florist -- Bloom Floral!"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"{name} Hello from Bloom Floral!"}
