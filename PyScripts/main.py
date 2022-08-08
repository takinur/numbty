from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World, i am from Python FastAPI"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "item": "Item %s" % item_id}


# Run the server port 5000
if __name__ == '__main__':
    uvicorn.run(app, port=5000, host='0.0.0.0')
