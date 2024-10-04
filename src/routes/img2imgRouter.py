from controllers.Img2ImgControllers import Img2ImgControllers
from fastapi import APIRouter,Form,Depends
from common.Types import Image2Image_Type,Text2Image_Type

img2imgRouter = APIRouter()
img2imgControllers = Img2ImgControllers()

@img2imgRouter.post("/img-to-img")
async def img_to_img(body:Image2Image_Type = Depends()):
    res = await img2imgControllers.img2img(body)
    return res