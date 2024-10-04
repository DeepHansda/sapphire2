from fastapi import APIRouter, Response,Depends
from controllers.Text2ImgControllers import Text2ImgControllers
from common.Types import Text2Image_Type
from contextlib import asynccontextmanager
from common.Utils import templates

t2ImgControllers = Text2ImgControllers()
text2ImgRouter = APIRouter()



@text2ImgRouter.post("/text-to-img")
async def text_to_img(prompt:Text2Image_Type = Depends()):
        print(prompt)
        res = await t2ImgControllers.text2img(prompt)
        return res