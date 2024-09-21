from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "profile" ADD "bio" TEXT NOT NULL;
        ALTER TABLE "profile" DROP COLUMN "address";
        ALTER TABLE "profile" ALTER COLUMN "job_role" TYPE VARCHAR(125) USING "job_role"::VARCHAR(125);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "profile" ADD "address" VARCHAR(250) NOT NULL;
        ALTER TABLE "profile" DROP COLUMN "bio";
        ALTER TABLE "profile" ALTER COLUMN "job_role" TYPE VARCHAR(64) USING "job_role"::VARCHAR(64);"""
