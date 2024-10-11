from fastapi import FastAPI

app = FastAPI(
    title="Microservice for messages",
    docs_url="/api/docs",
    description="A simple microservice written with DDD pattern for messaging with users",
    debug=True,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
