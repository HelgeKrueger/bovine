from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE UNIQUE INDEX "uid_publickey_url_43f8a9" ON "publickey" ("url");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "publickey" DROP INDEX "idx_publickey_url_43f8a9";"""
