#Python
from operator import gt
from pathlib import Path
from typing import Optional
from unittest import result

#Pydantic
from pydantic import BaseModel, Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query,Path

app = FastAPI()

# Models

class Hair_color(BaseModel):
    red = 'red'
    blue = 'blue'
    green = 'green'

class Person(BaseModel): 
    first_name: str = Field(...,
                            max_length=30,
                            min_length=1
                            )
    last_name: str = Field(...,
                            max_length=30,
                            min_length=1
                            )
    age: int = Field(...,
                     gt=18,
                     le=100
                     )
    hair_color: Optional[Hair_color] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    
class Location(BaseModel):
    country: str
    city: str
    street: str
    address: int 
    

@app.get("/")
def home(): 
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(
    ...
    )): 
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title='Name',
        description='Name description'
        ),
    age: int = Query( #No es buena practica poner como 
        ...           #campo obligatorio en un query,deberia hacerse en el path
        )
): 
    return {name: age}

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0
        )
):
    return{person_id:'its exist'}

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        gt=0
    ),
    person: Person = Body(
        ...
        ),
    Location: Location = Body(
        ...
    )
    
):
    result = person.dict()
    result.update(Location.dict())
    print(result)
    return result