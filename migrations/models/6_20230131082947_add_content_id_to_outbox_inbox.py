from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inboxentry" ADD "content_id" VARCHAR(255);
        ALTER TABLE "outboxentry" ADD "content_id" VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inboxentry" DROP COLUMN "content_id";
        ALTER TABLE "outboxentry" DROP COLUMN "content_id";"""
