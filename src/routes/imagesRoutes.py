from fastapi import FastAPI,APIRouter
from common.Utils import Utils
from fastapi.responses import JSONResponse
from fastapi import status

import json

images_routes = APIRouter()

imagesControllers = ImagesControllers()
@images_routes.get("/get-images/{imgs_type}")
async def get_images(imgs_type:str):
    res = await Utils.getImagesByType(imgs_type)
    parse_data = json.load(res)
    if(len(parse_data.img_list) == 0):
         return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=res
            )
    return JSONResponse(status_code=status.HTTP_200_OK, content=res)
    
