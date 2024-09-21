
from models.models import Post, PostIn_Pydantic, Post_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


post_router = APIRouter()


class Message(BaseModel):
    message: str
# Defining a simple Pydantic model for response messages (used in the delete operation), with a single field `message`.

@post_router.get('/api/post', response_model=List[Post_Pydantic])
async def get_all_posts():
    return await Post_Pydantic.from_queryset(Post.all())

@post_router.post('/api/post', response_model=Post_Pydantic)
async def create_a_post(post: PostIn_Pydantic):
    postobj = await Post.create(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_tortoise_orm(postobj)

@post_router.get('/api/post/{id}', response_model=Post_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_a_post(id: int):
    return await Post_Pydantic.from_queryset_single(Post.get(id=id))

@post_router.put("/api/post/{id}", response_model=Post_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_a_post(id: int, post: PostIn_Pydantic):
    await Post.filter(id=id).update(**post.dict(exclude_unset=True))
    return await Post_Pydantic.from_queryset_single(post.get(id=id))


@post_router.delete("/api/post/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_a_post(id: int):
    delete_obj = await Post.filter(id=id).delete()

    if not delete_obj:
        raise HTTPException(status_code=404, detail="This Post is not found.")
    return Message(message="Successfully Deleted")





