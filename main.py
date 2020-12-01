
from fastapi import FastAPI
from database.mongodbmanager import connectToMongo, closeMongoConnection
from router.commonrouters import commonRouter
from router.shortvideorouters import shortVideoParseRouter

app = FastAPI()

# app启动时事件（连接数据库，也就是初始化数据库）
app.add_event_handler("startup", connectToMongo)
# app注销时事件（关闭数据库，防止数据库连接只增不减导致bug：系统崩溃）
app.add_event_handler("shutdown", closeMongoConnection)

# 包含根路由
app.include_router(
    commonRouter
)
# 包含短视频路由
app.include_router(
    shortVideoParseRouter
)
