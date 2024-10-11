from fastapi import APIRouter, Request, Response, Depends
from controllers.Text2ImgControllers import Text2ImgControllers
from common.Types import Text2Image_Type
from contextlib import asynccontextmanager
from common.Utils import templates
from common.const import DEFAULT_FORM_DATA
import json

t2ImgControllers = Text2ImgControllers()
text2ImgRouter = APIRouter()


@text2ImgRouter.get("/text-to-img")
async def text_to_img(request: Request):
    return templates.TemplateResponse(
        "/pages/text2img.html", {"request": request, "data": DEFAULT_FORM_DATA}
    )


@text2ImgRouter.post("/text-to-img/generate")
async def generate_text_to_img(request: Request, prompt: Text2Image_Type = Depends()):
    res = await t2ImgControllers.text2img(prompt)
    return res


@text2ImgRouter.post("/text-to-img/jinja/generate")
async def generate_jinja_text_to_img(
    request: Request, prompt: Text2Image_Type = Depends()
):
    res = await t2ImgControllers.text2img(prompt)
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
            "data": default_form_data,
        },
    )
