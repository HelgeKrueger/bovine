from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "actor" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "account" VARCHAR(255) NOT NULL,
    "url" VARCHAR(255) NOT NULL,
    "actor_type" VARCHAR(255) NOT NULL,
    "private_key" TEXT NOT NULL,
    "public_key" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "follower" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "account" VARCHAR(255) NOT NULL,
    "followed_on" TIMESTAMP NOT NULL,
    "inbox" VARCHAR(255),
    "public_key" TEXT,
    "actor_id" INT NOT NULL REFERENCES "actor" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "following" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "account" VARCHAR(255) NOT NULL,
    "followed_on" TIMESTAMP NOT NULL,
    "actor_id" INT NOT NULL REFERENCES "actor" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "inboxentry" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created" TIMESTAMP NOT NULL,
    "content" JSON NOT NULL,
    "actor_id" INT NOT NULL REFERENCES "actor" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "outboxentry" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "local_path" VARCHAR(255) NOT NULL,
    "created" TIMESTAMP NOT NULL,
    "content" JSON NOT NULL,
    "actor_id" INT NOT NULL REFERENCES "actor" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
