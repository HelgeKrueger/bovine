from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inboxentry" ADD "conversation" VARCHAR(255);
        ALTER TABLE "inboxentry" ADD "read" INT NOT NULL  DEFAULT 1;
        ALTER TABLE "outboxentry" DROP COLUMN "conversation";
        ALTER TABLE "outboxentry" DROP COLUMN "read";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "inboxentry" DROP COLUMN "conversation";
        ALTER TABLE "inboxentry" DROP COLUMN "read";
        ALTER TABLE "outboxentry" ADD "conversation" VARCHAR(255);
        ALTER TABLE "outboxentry" ADD "read" INT NOT NULL  DEFAULT 1;"""
