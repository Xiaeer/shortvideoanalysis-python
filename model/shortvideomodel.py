from pydantic import BaseModel


class WeseeBase(BaseModel):
    feed_id: str
    real_url: str
    real_url_lossless: str
