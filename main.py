from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks

app = FastAPI()

with open("languages.txt") as f:
    languages = f.read().split(", ")

class Translation(BaseModel):
    text: str
    base_lang: str
    final_lang: str

    @validator('base_lang', 'final_lang')
    def valid_lang(cls, v):
        if v not in languages:
            raise ValueError('Language not supported')
        return v

## Route 1: /
## Test if everything is working
##{ "message": "Hello World!"}
@app.get("/")
def get_root():
    return {"message": "Hello World!"}

## Route 2: /translate
## Take a translation request and store it in the database
## Return the translation id
@app.post("/translate")
def post_translation(t: Translation, background_tasks: BackgroundTasks):
    #Store the translation in the database
    t_id = tasks.store_translation(t)
    #run translation in the background
    background_tasks.add_task(tasks.run_translation, t.id)
    return {"task_id": t_id}
    

## Route 3: /result
## Take a translation id
## return the result if it is ready
@app.get("/result")
def get_result(t_id: int):
    return {"translation": tasks.find_translation(t_id)}
