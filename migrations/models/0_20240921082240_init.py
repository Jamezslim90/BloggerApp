from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "author" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);
COMMENT ON TABLE "author" IS 'This table contains a list of all the authors';
CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);
COMMENT ON TABLE "category" IS 'This table contains a list of all the categories';
CREATE TABLE IF NOT EXISTS "post" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(125) NOT NULL,
    "body" TEXT NOT NULL,
    "author_id" INT NOT NULL REFERENCES "author" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "post" IS 'This table contains a list of all blog posts';
CREATE TABLE IF NOT EXISTS "comment" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "owner_id" INT NOT NULL REFERENCES "author" ("id") ON DELETE CASCADE,
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "comment" IS 'This table contains a list of all post comments';
CREATE TABLE IF NOT EXISTS "profile" (
    "job_role" VARCHAR(64) NOT NULL,
    "address" VARCHAR(250) NOT NULL,
    "author_id" INT NOT NULL  PRIMARY KEY REFERENCES "author" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "post_category" (
    "post_id" INT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "category_id" INT NOT NULL REFERENCES "category" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_post_catego_post_id_0d8446" ON "post_category" ("post_id", "category_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
