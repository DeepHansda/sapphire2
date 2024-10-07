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


templates=Jinja2Templates(directory="./templates")


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

    def exception_handler(self, func: Callable[..., Any]) -> Callable:
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Return the exception as a response
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
                )

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
        self, images: List[Image.Image],metaData:{str:any}, base64_for_img: bool, tag: str
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
            index = int(file_count_in_output/2) + index
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
                byte_img_base64 = self.byte_img_to_base64(byte_img=byte_img,img_path=None)

                for b_i in byte_imgs_list:
                    b_i_base64 = self.byte_img_to_base64(byte_img=b_i,img_path=None)
                    byte_imgs_list_base64.append(b_i_base64)

                return json.dumps(
                    {"imgs_list": byte_imgs_list_base64, "img": byte_img_base64}
                )

            return byte_imgs_list, byte_img
        else:
            result_images = images[0]
            byte_img = self.get_byte_img(result_images)
            if base64_for_img is True:
                byte_img_base64 = self.byte_img_to_base64(byte_img=byte_img,img_path=None)
                return byte_img_base64
            return byte_img

    async def getImagesByType(self, imgs_type: str):
        # Define the file path
        
        f_path = f"{cwd}/output/{imgs_type}"

        # Check if the directory exists
        if not os.path.exists(f_path):
            # Return 404 response if the directory doesn't exist
            err_msg = {"message": f"Images of type '{imgs_type}' don't exist!", "img_list": "[]"}
            return err_msg

        base64_img_list = []  # List to store base64 encoded images and their associated data
        for root, directories, files in os.walk(f_path):
            # Sort directories by modification time in reverse order
            sorted_directories = sorted(
                directories,
                key=lambda d: os.path.getmtime(os.path.join(root, d)),
                reverse=True,
            )
            for sub_dir in sorted_directories:
                as_path = os.path.join(root, sub_dir)
                sub_dir_data = {"sub_dir_images": [],"date":sub_dir}
                # Get all files in the sub-directory
                all_files = [
                    f
                    for f in os.listdir(as_path)
                    if os.path.isfile(os.path.join(as_path, f))
                ]
                # Sort files in reverse order
                sorted_files = sorted(all_files, reverse=True)
                for img in sorted_files:
                    img_path = os.path.join(as_path, img)
                    img_data = {}
                    b64_img = ""
                    # sub_dirs_dict = {}
                    if img_path.endswith(".png"):
                        # Convert PNG image to base64
                        b64_img = self.byte_img_to_base64(
                            byte_img=None, img_path=img_path
                        )
                        # Append base64 encoded image to the list
                        img_data = {"img_data": {}, "enc_img": b64_img}
                        sub_dir_data["sub_dir_images"].append(img_data)

                    elif img_path.endswith(".json"):
                        # Load JSON data from the file
                        with open(img_path) as f:
                            img_data = json.load(f)
                            # Add the loaded data to the previously appended image
                            sub_dir_data["sub_dir_images"][-1]["img_data"] = img_data

                base64_img_list.append(sub_dir_data)
                # print(sub_dir_data)

        # Convert the list of base64 encoded images to JSON format
        
        
        json_img_list = json.dumps({"img_list": base64_img_list})

        return json_img_list
        # Return 200 response with the JSON data
        return JSONResponse(status_code=status.HTTP_200_OK, content=json_img_list)
    

    def render_imgs_gallery(request:Request):
        return templates.TemplateResponse("partials/imageGallery.html",{"request":request,})


   