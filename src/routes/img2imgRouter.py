from controllers.Img2ImgControllers import Img2ImgControllers
from fastapi import APIRouter, Form, Depends
from fastapi.requests import Request
from common.Types import Image2Image_Type, Text2Image_Type
from common.Utils import templates
from common.const import DEFAULT_FORM_DATA, TABS_LINKS
import json

img2imgRouter = APIRouter()
img2imgControllers = Img2ImgControllers()


@img2imgRouter.get("/img-to-img")
async def img_to_img(request: Request):
    print(request.url.path)
    return templates.TemplateResponse(
        "/pages/img2img.html",
        {"request": request, "data": DEFAULT_FORM_DATA, "tabs_links": TABS_LINKS},
    )


@img2imgRouter.post("/img-to-img/generate")
async def img_to_img_generate(body: Image2Image_Type = Depends()):
    res = await img2imgControllers.img2img(body)
    return res


@img2imgRouter.post("/img-to-img/generate")
async def img_to_img_generate(body: Image2Image_Type = Depends()):
    res = await img2imgControllers.img2img(body)
    return res


@img2imgRouter.post("/img-to-img/jinja/generate")
async def generate_jinja_img_to_img(
    request: Request, body: Image2Image_Type = Depends()
):
    res = await img2imgControllers.img2img(body)
    parsedData = json.loads(res.body.decode("utf-8"))

    content = {
        "enc_img": parsedData["enc_img_data"],
        "additional_data": json.loads(parsedData["additional_data"]),
        "date": parsedData["date"],
    }
    return templates.TemplateResponse(
        "/partials/imageCard.html",
        {
            "request": request,
            "isGeneratedResImg": True,
            "resData": content,
            "data": DEFAULT_FORM_DATA,
        },
    )
