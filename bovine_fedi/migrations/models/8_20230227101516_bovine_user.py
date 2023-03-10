from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "actorobjects" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "object_id" VARCHAR(255) NOT NULL,
    "actor_id" INT NOT NULL REFERENCES "actor" ("id") ON DELETE CASCADE
);;
        CREATE TABLE IF NOT EXISTS "actorproperties" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "value" JSON NOT NULL,
    "actor_id" INT NOT NULL REFERENCES "actor" ("id") ON DELETE CASCADE
);;
        CREATE TABLE IF NOT EXISTS "bovineuser" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "hello_sub" VARCHAR(255) NOT NULL,
    "handle_name" VARCHAR(255) NOT NULL UNIQUE,
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "last_sign_in" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);;
        CREATE TABLE IF NOT EXISTS "bovineuserendpoint" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "endpoint_type" VARCHAR(12) NOT NULL  /* ACTOR: ACTOR\nINBOX: INBOX\nOUTBOX: OUTBOX\nFOLLOWERS: FOLLOWERS\nFOLLOWING: FOLLOWING\nPROXY_URL: PROXY_URL\nEVENT_SOURCE: EVENT_SOURCE\nCOLLECTION: COLLECTION */,
    "stream_name" VARCHAR(255) NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "bovine_user_id" INT NOT NULL REFERENCES "bovineuser" ("id") ON DELETE CASCADE
);;
        CREATE TABLE IF NOT EXISTS "bovineuserkeypair" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "private_key" TEXT NOT NULL,
    "public_key" TEXT NOT NULL,
    "bovine_user_id" INT NOT NULL REFERENCES "bovineuser" ("id") ON DELETE CASCADE
);;
        CREATE TABLE IF NOT EXISTS "bovineuserproperty" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "value" JSON NOT NULL,
    "bovine_user_id" INT NOT NULL REFERENCES "bovineuser" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "actorobjects";
        DROP TABLE IF EXISTS "actorproperties";
        DROP TABLE IF EXISTS "bovineuser";
        DROP TABLE IF EXISTS "bovineuserendpoint";
        DROP TABLE IF EXISTS "bovineuserkeypair";
        DROP TABLE IF EXISTS "bovineuserproperty";"""
