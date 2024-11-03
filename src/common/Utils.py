import asyncio
import io
import os, json
import base64
import subprocess
from datetime import date
from random import randint
from typing import Any, Callable, List

import common.shared as sharedValues
import torch
from common.const import OUTPUT
from common.Folder_Paths import cwd, models_dir
from common.Types import Text_Emmbed_Type
from diffusers.utils import make_image_grid
from fastapi import HTTPException, status
from PIL import Image
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


templates = Jinja2Templates(directory="./templates")


class Utils:
    def __init__(self):

        pass

    def get_text_embds(self, args: Text_Emmbed_Type):
        pipe = args.pipeline
        prompt = args.prompt
        negative_prompt = args.negative_prompt
        max_length = pipe.tokenizer.model_max_length
        input_ids = pipe.tokenizer(prompt, return_tensors="pt").input_ids
        input_ids = input_ids.to("cuda")

        negative_ids = pipe.tokenizer(
            negative_prompt,
            truncation=False,
            padding="max_length",
            max_length=input_ids.shape[-1],
            return_tensors="pt",
        ).input_ids
        negative_ids = negative_ids.to("cuda")
        concat_embeds = []
        neg_embeds = []
        for i in range(0, input_ids.shape[-1], max_length):
            concat_embeds.append(pipe.text_encoder(input_ids[:, i : i + max_length])[0])
            neg_embeds.append(pipe.text_encoder(negative_ids[:, i : i + max_length])[0])

        prompt_embeds = torch.cat(concat_embeds, dim=1)
        negative_prompt_embeds = torch.cat(neg_embeds, dim=1)

        return prompt_embeds, negative_prompt_embeds

    def get_byte_img(self, image: Image.Image) -> bytes:
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        byte_img = buf.getvalue()
        print(type(byte_img))
        return byte_img

    def seed_handler(self, seed: int) -> (int, Any):
        shared = sharedValues.load_shared_values()
        device = shared.get("init_device")
        if seed == -1:
            n = 10
            range_start = 10 ** (n - 1)
            range_end = (10**n) - 1
            rand_seed = randint(range_start, range_end)
            seed = rand_seed

        generator = torch.Generator(device=device).manual_seed(seed)
        return seed, generator

    def try_catch_wrapper(self, func):
        async def wrapper(request: Request, *args, **kwargs):
            try:
                return await func(request, *args, **kwargs)
            except HTTPException as http_exc:
                # Handle HTTPException differently if needed
                error_message = str(
                    http_exc.detail
                )  # Get the HTTPException detail message
                print(f"HTTP Error: {error_message}")

                # Check if it's an HTMX request
                if request.headers.get("HX-Request"):
                    # Return a partial HTML response for HTMX to inject
                    return templates.TemplateResponse(
                        "htmx_error.html",
                        {"request": request, "error": error_message},
                        status_code=http_exc.status_code,
                    )
                else:
                    # Re-raise the HTTPException to be handled by FastAPI's default exception handler
                    raise http_exc

            except Exception as e:
                # Handle all other exceptions (non-HTTPException)
                error_message = str(e)
                print(f"Error: {error_message}")

                # Check if it's an HTMX request
                if request.headers.get("HX-Request"):
                    # Return a partial HTML response for HTMX to inject
                    return templates.TemplateResponse(
                        "htmx_error.html",
                        {"request": request, "error": error_message},
                        status_code=500,
                    )
                else:
                    # Raise a general HTTP 500 error for non-HTMX requests
                    raise HTTPException(status_code=500, detail=error_message)

        return wrapper

    def get_all_models(self) -> dict:
        all_models_dic = {}
        for root, directories, files in os.walk(models_dir):
            for d in directories:
                models_dic = {}
                dir_path = os.path.join(root, d)

                for f in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, f)
                    models_dic[f] = file_path

                all_models_dic[d] = models_dic
        return all_models_dic

    async def download_with_wget(self, url: str, output_path: str):
        try:
            # Command to execute wget with the provided URL and output path

            command = [
                "wget",
                "-c",
                url,
                "-O",
                output_path,
                "--progress=bar",
                "--show-progress",
            ]

            # Start the subprocess and redirect stderr to stdout
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            # print(process.stdout.read())

            # Read the output stream line by line
            for line in process.stdout:
                print(
                    line.strip()
                )  # Print the line without trailing newline characters

            # Wait for the subprocess to finish
            return_code = process.wait()

            # Check the return code for errors
            if return_code != 0:
                print(
                    f"An error occurred during the download (return code: {return_code})"
                )
        except Exception as e:
            print(f"An error occurred: {e}")

    def generate_grid_size(self, total_number: int) -> (int, int):

        import math

        grid_size = math.sqrt(total_number)

        rows = math.ceil(grid_size)
        cols = math.ceil(total_number / rows)

        return rows, cols

    def byte_img_to_base64(self, byte_img: bytes, img_path) -> str:
        if img_path:
            with open(img_path, "rb") as img:
                byte_img_base64 = base64.b64encode(img.read()).decode("utf-8")
        else:
            byte_img_base64 = base64.b64encode(byte_img).decode("utf-8")
        return byte_img_base64

    def handle_generated_images(
        self,
        images: List[Image.Image],
        metaData: {str: any},
        base64_for_img: bool,
        tag: str,
    ) -> Any:
        today = date.today()
        if tag:
            as_path = f"{OUTPUT}/{tag}/{today}"
        else:
            as_path = f"{OUTPUT}/{today}"
        output_path = os.path.join(cwd, as_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        file_count_in_output = len(os.listdir(output_path))
        print(images)
        for index, image in enumerate(images):
            index = int(file_count_in_output / 2) + index
            file_name = f"{OUTPUT}_{index}_{today}"
            if metaData is not None:
                with open(f"{output_path}/{file_name}.json", "wb") as metaJson:
                    metaJson.write(json.dumps(metaData).encode("utf-8"))
            with open(f"{output_path}/{file_name}.png", "wb") as img:
                image.save(img, format="PNG")

        images_length = len(images)

        result_images = ""
        if images_length > 1:
            byte_imgs_list = []
            rows, cols = self.generate_grid_size(images_length)

            for index, img in enumerate(images):
                byte_img = self.get_byte_img(img)
                byte_imgs_list.append(byte_img)
            result_images = make_image_grid(images, rows=rows, cols=cols)
            byte_img = self.get_byte_img(result_images)

            if base64_for_img is True:
                byte_imgs_list_base64 = []
                byte_img_base64 = self.byte_img_to_base64(
                    byte_img=byte_img, img_path=None
                )

                for b_i in byte_imgs_list:
                    b_i_base64 = self.byte_img_to_base64(byte_img=b_i, img_path=None)
                    byte_imgs_list_base64.append(b_i_base64)

                return json.dumps(
                    {"imgs_list": byte_imgs_list_base64, "img": byte_img_base64}
                )

            return byte_imgs_list, byte_img
        else:
            result_images = images[0]
            byte_img = self.get_byte_img(result_images)
            if base64_for_img is True:
                byte_img_base64 = self.byte_img_to_base64(
                    byte_img=byte_img, img_path=None
                )
                return byte_img_base64
            return byte_img
