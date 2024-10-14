import asyncio
from contextlib import asynccontextmanager
import uvicorn
import common.Folder_Paths as Folder_Paths
import logging, os, time
from common.startup import startUp
from fastapi.middleware.cors import CORSMiddleware
from watchfiles import run_process,arun_process,awatch
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from common.PipelineComponents import PipelineComponents
from fastapi.staticfiles import StaticFiles

from fastapi.responses import JSONResponse

from routes.modelsRoutes import models_router
from routes.text2imgRouter import text2ImgRouter
from routes.img2imgRouter import img2imgRouter
from routes.imagesRoutes import images_routes
from fastapi.middleware.gzip import GZipMiddleware
from common.Utils import templates




main_shared_file_path = os.path.join(Folder_Paths.cwd, "shared_values.json")


async def callback(changes):
    print("changes in :", changes)


def changesMade():
    print("changes made")


async def changeHandler():
    async for changes in awatch(main_shared_file_path):
        print(changes)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     run_process(main_shared_file_path,target=changesMade())
#     yield
#     asyncio.get_event_loop().stop()
#     print("main shutdown")


app = FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
app.add_middleware(GZipMiddleware)

# main_app_lifespan = app.router.lifespan_context

# @asynccontextmanager
# async def lifespan_wrapper(app):
#     await arun_process(main_shared_file_path,target=changesMade())
#     async with main_app_lifespan(app) as maybe_state:
#         yield maybe_state
#     print("sub shutdown")

# app.router.lifespan_context = lifespan_wrapper

origins = ["*", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(models_router)
app.include_router(text2ImgRouter)
app.include_router(img2imgRouter)
app.include_router(images_routes)


@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse("base.html",{"request":request})
