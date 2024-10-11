INIT_DEVICE = "init_device"
CHECKPOINT = "checkpoint"
CHECKPOINTS = "checkpoints"
VAE = "vae"
LORAS = "loras"
LORA = "lora"
CONTROLNET = "controlnet"
CLIP = "clip"
CLIP_VISION = "clip_vision"
EMBEDDINGS = "embeddings"
UNET = "unet"
UPSCALE_MODELS = "upscale_models"
INPUT = "input"
OUTPUT = "output"
TEXT2IMG_TAG = "text2img"
IMG2IMG_TAG = "img2img"
TEXT2IMG_XL_TAG = "text2img_xl"
IMG2IMG_XL_TAG = "img2img_xl"
DEFAULT_FORM_DATA = {
    "prompt": "",
    "negative_prompt": "",
    "scheduler": "eular",
    "seed": -1,
    "width": 512,
    "height": 512,
    "steps": 20,
    "use_kerras": False,
    "use_lora": False,
    "lora_scale": 0.75,
    "guidance_scale": 8.0,
    "batch_size": 1,
    "fixed_seed": False,
}




