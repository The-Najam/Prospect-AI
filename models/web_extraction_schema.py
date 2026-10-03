from pydantic import BaseModel, HttpUrl




class Page(BaseModel):
    url : HttpUrl
    page_type : str
    content : str


class WebExtraction(BaseModel):
    pages : list[Page]
