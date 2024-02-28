from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from clues import getInfo
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# CORS stuff
origins = [
    "http://localhost:5173/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class Item(BaseModel):
    board: list[list[str]]
    horizontal: dict[int, str]
    vertical: dict[int, str]

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/{difficulty}", response_model=Item)
def getGame(difficulty: int) -> Item:
    hashmap = getInfo(difficulty)


    #Verify return values in case of malformed board
    if not all(key in hashmap for key in ['board', 'horizontal', 'vertical']):
        raise HTTPException(status_code=404, detail="Data not found for the given difficulty")
    
    item = Item(
        board=hashmap['board'],
        horizontal=hashmap['horizontal'],
        vertical=hashmap['vertical']
    )

    return item
    