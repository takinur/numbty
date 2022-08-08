from fastapi import FastAPI, Request
import hello
from ResumeExtractor import resume_result_wrapper
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    object = hello.sayHello()
    text = hello.method()
    return {"message": object.add(10, 2), "text": text}


@app.post('/api/v1/resume-extract/')
async def getInformation(info: Request):
    req_info = await info.json()
    resume = req_info['resume']

    return resume_result_wrapper(resume)


@app.get('/api/v1/resume/{file_url}')
async def extract_resume(file_url):
    # TODO:Parameter from Laravel Controller
    file_url = 'assets/test_resumes/T_001.pdf'
    return resume_result_wrapper(file_url)


fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]





# Run the server port 5000
if __name__ == '__main__':
    uvicorn.run(app, port=5000, host='0.0.0.0')
