from fastapi import FastAPI
import hello
from ResumeExtractor import resume_result_wrapper
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    object = hello.sayHello()
    text = hello.method()
    return {"equivalent": object.add(10, 2), "text" : text}



@app.get('/api/v1/resume/{file_url}')
async def extract_resume(file_url):
    file_url = 'assets/test_resumes/T_001.pdf' #TODO:Parameter from Laravel Controller
    return resume_result_wrapper(file_url)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id, "item": "Item %s" % item_id}






# Run the server port 5000
if __name__ == '__main__':
    uvicorn.run(app, port=5000, host='0.0.0.0')
