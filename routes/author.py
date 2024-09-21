from models.models import Author, AuthorIn_Pydantic, Author_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


author_router = APIRouter()


class Message(BaseModel):
    message: str
# Defining a simple Pydantic model for response messages (used in the delete operation), with a single field `message`.

@author_router.get('/api/author', response_model=List[Author_Pydantic])
async def get_all_authors():
    return await Author_Pydantic.from_queryset(Author.all())

@author_router.post('/api/author', response_model=Author_Pydantic)
async def create_an_author(author: AuthorIn_Pydantic):
    authorobj = await Post.create(**author.dict(exclude_unset=True))
    return await Author_Pydantic.from_tortoise_orm(authorobj)

@author_router.get('/api/author/{id}', response_model=Author_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_an_author(id: int):
    return await Author_Pydantic.from_queryset_single(Author.get(id=id))

@author_router.put("/api/author/{id}", response_model=Author_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_an_author(id: int, author: AuthorIn_Pydantic):
    await Author.filter(id=id).update(**author.dict(exclude_unset=True))
    return await Author_Pydantic.from_queryset_single(author.get(id=id))


@author_router.delete("/api/author/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_an_author(id: int):
    delete_obj = await Author.filter(id=id).delete()

    if not delete_obj:
        raise HTTPException(status_code=404, detail="This Author is not found.")
    return Message(message="Successfully Deleted")
