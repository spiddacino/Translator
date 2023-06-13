from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks

app = FastAPI()

## Route 1: /
## Test if everything is working
##{ "message": "Hello World!"}
@app.get("/")
def get_root():
    return {"message": "Hello World!"}

## Route 2: /translate
## Take a translation request and store it in the database
## Return the translation id

## Route 3: /result
## Take a translation id
## return the result if it is ready