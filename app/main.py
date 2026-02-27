from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok",
            "version": "1.0.0"}