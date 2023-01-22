from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "outboxentry" ADD "conversation" VARCHAR(255);
        ALTER TABLE "outboxentry" ADD "read" INT NOT NULL  DEFAULT 1;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "outboxentry" DROP COLUMN "conversation";
        ALTER TABLE "outboxentry" DROP COLUMN "read";"""
