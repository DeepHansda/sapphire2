from fastapi import FastAPI, APIRouter
from common.Utils import Utils
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import status
from controllers.ImagesControllers import ImagesControllers
from common.Utils import templates

import json

images_routes = APIRouter()

imagesControllers = ImagesControllers()


@images_routes.get("/generated-images/{imgs_type}")
async def get_images_container(request: Request, imgs_type: str):
    return templates.TemplateResponse("pages/generatedImages.html",{"request":request})


@images_routes.get("/get-images/{imgs_type}")
async def get_images(imgs_type: str):
    res = await Utils().getImagesByType(imgs_type)
    parse_data = json.load(res)
    if len(parse_data.img_list) == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=res)
    return JSONResponse(status_code=status.HTTP_200_OK, content=res)
