from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
# from tortoise.query_utils import Prefetch
# from models.author import Author
# from models.category import Category



class Author(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    posts: fields.ReverseRelation["Post"]

    def __str__(self):
        return self.name

    class Meta:
        table = "author"
        table_description = "This table contains a list of all the authors"




Author_Pydantic = pydantic_model_creator(Author, name="Author")
AuthorIn_Pydantic = pydantic_model_creator(Author, name="AuthorIn", exclude_readonly=True)


class Profile(Model):
    job_role = fields.CharField(max_length=125)
    bio = fields.TextField()

    author: fields.OneToOneRelation[Author] = fields.OneToOneField(
        "models.Author", on_delete=fields.OnDelete.CASCADE, related_name="profile", primary_key=True
    )

    def __str__(self):
        return f"Address({self.city}, {self.street})"




Profile_Pydantic = pydantic_model_creator(Profile, name="Profile")
ProfileIn_Pydantic = pydantic_model_creator(Profile, name="ProfileIn", exclude_readonly=True)

class Post(Model):

    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=125)
    author: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField("models.Author", related_name="posts")
    body = fields.TextField()
    categories: fields.ManyToManyRelation["Category"] = fields.ManyToManyField(
        "models.Category", related_name="posts", through="post_category")
    created_at = fields.DatetimeField(auto_now_add=True)  # Automatically set to current time on creation
    updated_at = fields.DatetimeField(auto_now=True)  # Automatically updates when the record is modified
    is_published = fields.BooleanField(default=True)  # Optional field to mark post as published or not

    def __str__(self):
        return self.title

    class Meta:
        table = "post"
        table_description = "This table contains a list of all blog posts"



Post_Pydantic = pydantic_model_creator(Post, name="Post")
PostIn_Pydantic = pydantic_model_creator(Post, name="PostIn", exclude_readonly=True)


class Category(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()

    posts: fields.ManyToManyRelation[Post]

    def __str__(self):
        return self.name

    class Meta:
        table = "category"
        table_description = "This table contains a list of all the categories"



Category_Pydantic = pydantic_model_creator(Category, name="Category")
CategoryIn_Pydantic = pydantic_model_creator(Category, name="CategoryIn", exclude_readonly=True)


class Comment(Model):
    id = fields.IntField(primary_key=True)
    name = fields.TextField()
    post: fields.ForeignKeyRelation[Post] = fields.ForeignKeyField("models.Post", related_name="comments")
    owner: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField("models.Author", related_name="comments")
    created_at = fields.DatetimeField(auto_now_add=True)  # Automatically set to current time on creation
    updated_at = fields.DatetimeField(auto_now=True)  # Automatically updates when the record is modified

    def __str__(self):
        return self.name

    class Meta:
        table = "comment"
        table_description = "This table contains a list of all post comments"



Comment_Pydantic = pydantic_model_creator(Comment, name="Comment")
CommentIn_Pydantic = pydantic_model_creator(Comment, name="CommentIn", exclude_readonly=True)





TORTOISE_ORM = {
    "connections": {
        "default": "asyncpg://jamezslim90:zmgHh7aNwQk9@ep-cold-leaf-25567838.us-west-2.aws.neon.tech/bloggerapp-db"
    },
    "apps": {
        "models": {
            "models": ["models.models", "aerich.models"],  # Include Aerich models
            "default_connection": "default",
        },
    },
}