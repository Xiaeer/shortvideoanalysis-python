
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

# 常用路由，一般有根路由和favicon.ico（favicon.ico浏览器默认请求）
commonRouter = APIRouter()


@commonRouter.get("/favicon.ico")
async def favicon():
    return


@commonRouter.get("/", response_class=PlainTextResponse)
async def readRoot():
    return "Hello World"
