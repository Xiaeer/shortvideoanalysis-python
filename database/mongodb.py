from motor.motor_asyncio import AsyncIOMotorClient


class DataBase:
    # mongodb的client
    client: AsyncIOMotorClient = None
    # mongodb的database实例
    database = None
    # mongodb的collection实例
    shortVideoURLCollection = None


db = DataBase()
