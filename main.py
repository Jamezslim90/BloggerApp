from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routes.author import  author_router
from routes.category import category_router
from routes.comment import comment_router
from routes.post import post_router

# from fastapi.staticfiles import StaticFiles


# Initialise our fastapi app
app = FastAPI(title="Blogger App", description="A Simple Blog App with multiple models and database connections")


# Mount static files
# app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/home")
def read_root():
    return {"Hello": "World"}


# Include routers
app.include_router(author_router)
app.include_router(category_router)
app.include_router(comment_router)
app.include_router(post_router)






# Register Tortoise ORM
register_tortoise(
    app,
    # db_url="sqlite://db.sqlite3",
    db_url= "asyncpg://jamezslim90:zmgHh7aNwQk9@ep-cold-leaf-25567838.us-west-2.aws.neon.tech/bloggerapp-db",
    modules={"models": ["models.models","aerich.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)


