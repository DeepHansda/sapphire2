from typing import Annotated, Dict


from common.Utils import Utils
from controllers.ModelsControllers import ModelsController
from fastapi import APIRouter, Path, Response, status
from fastapi.responses import JSONResponse
from common.Types import Model_Request_Type


commonUtils = Utils()

modelsController = ModelsController()
extra_router = APIRouter()


@extra_router.post("/update-shared-values")
async def update_shared_values(shared_values: Dict[str, str]):
    res = await sharedValues.retrive_shared_values(shared_values)
    return Response(status_code=status.HTTP_200_OK, content=res)


@extra_router.get("/get-models/{model_type}")
async def get_models(model_type: Annotated[str, Path(title="to get the models")]):
    res = await modelsController.get_models(model_type)
    return res


@extra_router.get("/get-all-models")
async def get_all_models():
    res = await modelsController.get_all_models()
    return res


@extra_router.post("/change-models-by-type")
async def get_models_by_type(req:Model_Request_Type):
    res = await modelsController.change_model_by_type(req.model_name, req.model_type)
    return res


