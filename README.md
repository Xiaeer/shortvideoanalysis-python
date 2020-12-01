# shortvideoanalysis-python
短视频解析-python版

短视频解析demo（目前只有微视，后面有时间可能会分析其他）
基于Python的第三方web框架 FastAPI 搭建的一个web服务

## FastAPI框架的详细教程看官方文档
```bash
https://fastapi.tiangolo.com/zh/
```

## 本地启动mongodb
首先要安装mongodb环境，因为短视频解析后的地址数据保存到mongodb，避免每次解析都要请求短视频分享链接导致效率问题

打开终端运行mongod
```bash
mongod
```

### 安装python依赖（第三方库）
##### python环境需要3.6+
cd到此demo的根目录运行下面的pip安装命令
```bash
cd shortvideoanalysis
pip install -r ./requirements.txt
```

## 启动FastAPI服务
```bash
uvicorn main:app --reload
```

#### 短视频解析页面
```bash
http://127.0.0.1:8000/parseshortvideo
```

## Swagger Documentation
```bash
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```
