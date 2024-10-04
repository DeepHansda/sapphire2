from fastapi import FastAPI,APIRouter
from controllers.ImagesControllers import ImagesControllers
images_routes = APIRouter()

imagesControllers = ImagesControllers()
@images_routes.get("/get-images/{imgs_type}")
async def get_images(imgs_type:str):
    res = await imagesControllers.getImagesByType(imgs_type)
    return res
