import json
import os
import uvicorn
import torch, gc, threading

from common.Folder_Paths import models_dir, Folder_paths
from common.Utils import Utils
from common.shared import save_shared_values, load_shared_values
from common.PipelineComponents import PipelineComponents
from fastapi import HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from common.const import CHECKPOINT, CHECKPOINTS, LORAS, LORA
from controllers.Img2ImgControllers import Img2ImgControllers
from controllers.Text2ImgControllers import Text2ImgControllers
import common.shared as sharedValues
from importlib import reload


commonUtils = Utils()
folder_paths = Folder_paths()


class ModelsController:
    def __init__(self):
        pass

    async def get_models(self, model_type: str):
        try:
            folder_path = None
            if model_type in (
                "checkpoints",
                "sd_models",
                "stable_diffusion_models",
                "stable_diffusion",
            ):
                folder_path = os.path.join(models_dir, "checkpoints")
            elif model_type in ("loras", "lora"):
                folder_path = os.path.join(models_dir, "loras")
            else:
                folder_path = os.path.join(models_dir, model_type)

            if not os.path.isdir(folder_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="models directory does not exist",
                )

            models_dic = {}

            for root, _, files in os.walk(folder_path):
                for f in files:
                    models_dic[f] = os.path.join(root, f)

            return JSONResponse(status_code=status.HTTP_200_OK, content=models_dic)
        except Exception as e:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    async def get_all_models(self):
        try:
            selected_models = await sharedValues.retrive_shared_values(
                shared_values=None
            )

            all_models_dic = commonUtils.get_all_models()
            final_models_data = {}
            final_models_data["all_models"] = all_models_dic
            final_models_data["selected_models"] = selected_models

            return JSONResponse(
                status_code=status.HTTP_200_OK, content=final_models_data
            )
        except Exception as e:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    # @commonUtils.exception_handler
    async def change_model_by_type(self, model_name: str, model_type: str):

        pipelineComponents = PipelineComponents()
        file_name, path = folder_paths.search_file_in_path(model_type, model_name)
        model = {}
        if model_type == CHECKPOINTS:
            model_type = CHECKPOINT
        if model_type == LORAS:
            model_type = LORA
        model[model_type] = path

        device = pipelineComponents.device
        gc.collect()
        if device == "cuda":
            torch.cuda.empty_cache()

        def init_save():
            save_shared_values(model, save=True)

        tasks = BackgroundTasks()
        tasks.add_task(init_save)

        updated_values = save_shared_values(model)
        all_models_dic = commonUtils.get_all_models()
        final_models_data = {}
        final_models_data["all_models"] = all_models_dic
        final_models_data["selected_models"] = updated_values

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=final_models_data, background=tasks
        )
