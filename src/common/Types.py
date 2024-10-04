from typing import Any
from fastapi import UploadFile, File, Form
from pydantic import BaseModel
from dataclasses import dataclass


@dataclass
class Text2Image_Type:
    prompt: str = Form(...)
    negative_prompt: str = Form(...)
    width: int = Form(512)
    height: int = Form(512)
    scheduler: str = Form(...)
    steps: int = Form(20)
    use_kerras: bool = Form(False)
    seed: int = Form(...)
    guidance_scale: float = Form(7.5)
    use_lora: bool = Form(False)
    batch_size: int = Form(1)
    want_enc_imgs: bool = Form(False)
    lora_scale: float = Form(0.75)

    # prompt: str
    # negative_prompt: str
    # width: int | int = 512
    # height: int | int = 512
    # scheduler: str
    # steps: int | int = 20
    # use_kerras: bool | bool = False
    # seed: int | None = None
    # guidance_scale: float | float = 7.0
    # use_lora: bool | bool = False

    # @model_validator(mode='before')
    # @classmethod
    # def validate_to_json(cls, value: Any) -> Any:
    #     print(value)
    #     if isinstance(value, str):
    #         return cls(**json.loads(value))
    #     return value


@dataclass
class Image2Image_Type(Text2Image_Type):
    strength: float = Form(...)
    image: UploadFile = File(...)


class Text_Emmbed_Type(BaseModel):
    prompt: str
    negative_prompt: str
    pipeline: Any


class Model_Request_Type(BaseModel):
    model_name: str
    model_type: str
