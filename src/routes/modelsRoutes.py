from typing import Annotated, Dict
from common.Utils import Utils
from controllers.ModelsControllers import ModelsController
from fastapi import APIRouter, Path, Response, status,Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from common.Types import Model_Request_Type
from common.Utils import templates
import json


commonUtils = Utils()

modelsController = ModelsController()
models_router = APIRouter()


@models_router.post("/update-shared-values")
async def update_shared_values(shared_values: Dict[str, str]):
    res = await sharedValues.retrive_shared_values(shared_values)
    return Response(status_code=status.HTTP_200_OK, content=res)


@models_router.get("/get-models/{model_type}")
async def get_models(model_type: Annotated[str, Path(title="to get the models")]):
    res = await modelsController.get_models(model_type)
    return res


@models_router.get("/get-all-models")
async def get_all_models():
    res = await modelsController.get_all_models()
    return res


@models_router.get("/get-all-models/jinja")
async def get_all_models_jinja(request: Request):
    res = await modelsController.get_all_models()
    parsedData = json.loads(res.body.decode("utf-8"))

    return templates.TemplateResponse(
        "partials/models_list.html", {"request": request, "all_models_list": parsedData}
    )


@models_router.post("/change-models-by-type")
async def get_models_by_type(req: Model_Request_Type):
    res = await modelsController.change_model_by_type(req.model_name, req.model_type)
    return res
    
@models_router.post("/change-models-by-type/jinja")
async def get_models_by_type_jinja(request: Request):
    data:Dict = (await request.form())
    for key, value in data.items():
        model_type = key  # Assign the key to model_type
        model_name = value 
    res = await modelsController.change_model_by_type(model_name, model_type)
    return res