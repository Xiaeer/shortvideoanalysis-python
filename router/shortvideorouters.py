
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from database.mongodb import db
from model.shortvideomodel import WeseeBase
import re
import aiohttp


# 短视频解析路由
shortVideoParseRouter = APIRouter()
# 挂载模板文件夹（最好统一挂载，防止其他路由也要挂载模板，不方便）
templates = Jinja2Templates(directory="templates")

# 微视链接正则，判断是否合法，还要通过这个正则提取feedID
patternWesee = re.compile(r'^https://h5\.weishi\.qq\.com/weishi/feed/[\d\w]+')
# 微视提取真实地址正则
patternWeseeRealURL = re.compile(
    r"http://v\.weishi\.qq\.com/v\.weishi\.qq\.com/.+?mp4")
# 微视链接前缀
weseePrefix = "https://h5.weishi.qq.com/weishi/feed/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0"
}


@shortVideoParseRouter.get("/parseshortvideo", response_class=HTMLResponse)
async def parseShortVideo(request: Request):
    return templates.TemplateResponse(
        "parseshortvideo.html", {"request": request})


@shortVideoParseRouter.post("/parseshortvideobyurl")
async def parseShortVideoByURL(request: Request, parse_url: str = Form(...)):
    if "h5.weishi.qq.com" in parse_url:
        return {"real_url_lossless": await handleURLWesee(parse_url)}
    return {"real_url_lossless": "解析失败！未分析过该短视频网站"}


# 处理微视短视频链接
async def handleURLWesee(parseURL: str):
    matchObj = patternWesee.match(parseURL)
    if not matchObj:
        return "微视短视频解析失败！"
    # 微视的feed id号
    feedID = matchObj.group().replace(weseePrefix, "")
    # ***************************  查询mongodb并返回  **************************** #
    # 到mongodb查询看有没有此id的视频真实地址，没有则解析网页获取真实地址，并存入mongodb中，有则直接取出返回
    '''
    微视的原版无损1080p的视频地址具有时效性，一般半天就失效了，如果想要原版视频，推荐每次请求解析（每次都用正则匹配出地址，不存到数据库中，效率可能没有存到数据库中高），
    如果存到mongodb中，过半天真实地址失效，下次从mongodb查询的url就无意义了
    或者解析微视网页时候，获取视频压缩后的真实地址，这个地址没有时效性，任何时间都能访问，而且这个压缩近乎无损，可以存到mongodb中，提高下次查询的效率（避免解析网页）
    '''
    findOneRes = await db.shortVideoURLCollection.find_one({"feed_id": feedID})
    # 不为None，则查询到，直接返回real_url_lossless字段  
    if findOneRes:
        return findOneRes["real_url_lossless"]

    # ********************  解析网页获取真实地址并插入数据库  ********************* #
    return await analysisWeseeURL(feedID)


# 定义异步get请求，请求短视频链接(fastapi是异步web框架，所以requests同步请求的框架用不了)
async def analysisWeseeURL(feedID: str):
    shortVideoURL = weseePrefix + feedID + "/?from=pc"
    # 获取 session 对象
    async with aiohttp.ClientSession() as session:
        # get方式请求短视频链接
        async with session.get(shortVideoURL, headers=headers) as response:
            weseeRealURLObj = patternWeseeRealURL.search(await response.text())
            if not weseeRealURLObj:
                return "该视频不存在！"
            # 原版无损地址，直接访问没有权限
            realURL = weseeRealURLObj.group()
            # 替换成f30的无损压缩地址
            realURLLossless = realURL.replace(".f0.", ".f30.")
            # 解析成功后，插入mongodb中并返回真实地址
            # weseeBase = {
            #     "feed_id": feedID,
            #     "real_url": realURL,
            #     "real_url_lossless": realURLLossless
            # }
            # 推荐使用BaseModel处理数据，这样model和controller分离
            weseeBase = WeseeBase(feed_id=feedID, real_url=realURL, real_url_lossless=realURLLossless)
            insertOneRes = await db.shortVideoURLCollection.insert_one(weseeBase.dict())
            return weseeBase.real_url_lossless


# 修复collections中的id，因为mongodb中id都是ObjectId，转换成str方便python里操作（可忽略此步）
def fixShortVideoURLId(shortVideoURL):
    if shortVideoURL.get("_id", False):
        # change ObjectID to string
        shortVideoURL["_id"] = str(shortVideoURL["_id"])
        return shortVideoURL
    else:
        raise ValueError(
            f"No `_id` found! Unable to fix pet ID for pet: {shortVideoURL}"
        )
