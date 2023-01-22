from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "peer" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "domain" VARCHAR(255) NOT NULL,
    "peer_type" VARCHAR(7) NOT NULL  DEFAULT 'NEW' /* TRUSTED: TRUSTED\nBLOCKED: BLOCKED\nNEW: NEW */,
    "software" VARCHAR(255),
    "version" VARCHAR(255),
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMP
);;
        CREATE TABLE IF NOT EXISTS "publickey" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "public_key" TEXT NOT NULL
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "peer";
        DROP TABLE IF EXISTS "publickey";"""
