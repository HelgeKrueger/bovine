from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "publickeypk" (
    "url" VARCHAR(255) NOT NULL  PRIMARY KEY,
    "public_key" TEXT NOT NULL
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "publickeypk";"""
