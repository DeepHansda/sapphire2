from common.Folder_Paths import cwd
from common.const import OUTPUT
from fastapi import Response, status
from fastapi.responses import JSONResponse
import os, json

from common.Utils import Utils


common_utils = Utils()


class ImagesControllers:
    def __init__(self):
        pass

    # @common_utils.exception_handler
    async def getImagesByType(self, imgs_type: str):
        # Define the file path
        f_path = f"/kaggle/working/sapphire/backend/src/output/{imgs_type}"

        # Check if the directory exists
        if not os.path.exists(f_path):
            # Return 404 response if the directory doesn't exist
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": f"Images of type '{imgs_type}' don't exist!", "data": "[]"},
            )

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
                        b64_img = common_utils.byte_img_to_base64(
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
        # Return 200 response with the JSON data
        return JSONResponse(status_code=status.HTTP_200_OK, content=json_img_list)
