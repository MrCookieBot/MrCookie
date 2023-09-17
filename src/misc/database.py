# env stuff
import os
from dotenv import load_dotenv
load_dotenv()

# database stuff
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = motor.motor_asyncio.AsyncIOMotorClient()

uri_p = os.getenv("uri_p")
mongo: AsyncIOMotorClient = AsyncIOMotorClient(uri_p)

db = mongo["mrcookie"]


# update things into the database
async def do_update(dict, set):
    await db.cookieDict.update_one(dict, set)


async def do_insert(dict):
    await db.cookieDict.insert_one(dict)


# search for things from the database
async def do_find_one(dict):
    document = await db.cookieDict.find_one(dict)
    return document

# search for things from the database
async def do_find():
    cursor = db.cookieDict.find()
    document = await cursor.to_list(None)
    return document




# search for users from the blacklist database
async def do_find_blacklist_user(dict):
    document = await db.blacklist_users.find_one(dict)
    return document

# search for all users in blacklisted db
async def do_find_blacklist():
    full_list = []

    cursor = db.blacklist_users.find()
    docs = await cursor.to_list(None)
    for dict in docs:
        full_list.append(dict["_id"])


    return full_list

# add user into the blacklist database
async def do_insert_blacklist_user(dict):
    await db.blacklist_users.insert_one(dict)

# unblacklist a user
async def do_delete_blacklist_user(dict):
    await db.blacklist_users.delete_one(dict)
