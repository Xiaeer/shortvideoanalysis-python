
from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db


async def connectToMongo():
    print("connecting to mongo...")
    db.client = AsyncIOMotorClient(str("localhost:27017"),
                                   maxPoolSize=20,
                                   minPoolSize=10)
    # get a database
    # Format db.<database_name>
    db.database = db.client.common
    print("connected to database: common")
    # get a collection
    # Format db.<database_name>.<collection_name>
    db.shortVideoURLCollection = db.client.common.short_video_url
    print("connected to collection: common/short_video_url")


async def closeMongoConnection():
    print("closing connection...")
    db.client.close()
    print("closed connection")
