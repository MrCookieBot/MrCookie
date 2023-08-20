from config import uri_p

# database stuff
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

client = motor.motor_asyncio.AsyncIOMotorClient()

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

