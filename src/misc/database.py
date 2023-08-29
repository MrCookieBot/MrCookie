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
    return(document)

# search for things from the database
async def do_find():
    cursor = db.cookieDict.find()
    document = await cursor.to_list(None)
    return document

