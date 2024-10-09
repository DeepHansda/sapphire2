from fastapi import APIRouter, Request, Response, Depends
from controllers.Text2ImgControllers import Text2ImgControllers
from common.Types import Text2Image_Type
from contextlib import asynccontextmanager
from common.Utils import templates

t2ImgControllers = Text2ImgControllers()
text2ImgRouter = APIRouter()

default_form_data = {
    "prompt": "",
    "negative_prompt": "",
    "scheduler": "eular",
    "seed": -1,
    "width": 512,
    "height": 512,
    "steps": 20,
    "use_kerras": False,
    "use_lora": False,
    "lora_scale": 0.75,
    "guidance_scale": 8.0,
    "batch_size": 1,
    "fixed_seed": False,
}


@text2ImgRouter.get("/text-to-img")
async def text_to_img(request: Request):
    return templates.TemplateResponse(
        "/pages/text2img.html", {"request": request, "data": default_form_data}
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
    return templates.TemplateResponse(
        "/partials/imageCard.html",
        {
            "request": request,
            "isGeneratedResImg": True,
            "response": res,
            "data": default_form_data,
        },
    )
