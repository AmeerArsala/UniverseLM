import uvicorn


# uvicorn app.main:app --port 8080 --reload
def start():
    uvicorn.run("app.main:app", reload=True, port=8080)


if __name__ == "__main__":
    start()
