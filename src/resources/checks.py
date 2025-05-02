import discord

from resources.mrcookie import instance as bot
from resources.constants import ADMIN_USERS

from datetime import datetime, timedelta

async def is_admin(userID):
    for value in ADMIN_USERS:
        if userID == value:
            return True
        else:
            return False
        

async def is_blacklisted(userID):
    if await bot.db.find_blacklist({"_id": str(userID)}) != None:
        return True
    else:
        return False
        

async def validate_userid(userID):
    temp_id = userID.strip("<@!>")
    if temp_id.isdigit():
        new_id = int(temp_id)
        if len(str(new_id)) > 17:
            return new_id
        else:
            return None
    else:
        return None
    

async def lookup_database(userID, guildID):
    data = await bot.db.find_user({"_id": str(guildID), f"users.{userID}": {"$exists": True}})
    if data != None:
        return data
    else:
        return False


async def new_database(userID, guildID):
    newUser = {"Cookies": 0, "Streaks": 0, "DailyExpire": datetime.now() - timedelta(hours = 24), "RobExpire": datetime.now() - timedelta(hours = 24), "DailyMultiplier": 0, "RobChances": 7, "DailyMultExpire": datetime.now(), "RobExpire": datetime.now(), "Inventory": "Empty", "RobProtection": 0}
    await bot.db.update_user({"_id": str(guildID)}, {'$set': {"users." + str(userID) : {**newUser}}})


async def update_database(userID, guildID, updated_dict):
    await bot.db.update_user({"_id": str(guildID)}, {'$set': {"users." + str(userID) : {**updated_dict}}})


async def update_value(userID, guildID, item, new_value):
    await bot.db.update_user({"_id": str(guildID)}, {'$set': {"users." + str(userID) + "." + item: new_value}})
