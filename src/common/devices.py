import logging
import subprocess
import torch
from common.shared import save_shared_values
from common.const import INIT_DEVICE

CUDA = "cuda"
CPU = "cpu"


def get_gpu_names() -> set:
    gpu_names = set()
    out = subprocess.check_output(["nvidia-smi", "-L"])
    for l in out.split(b"\n"):
        if len(l) > 0:
            gpu_names.add(l.decode("utf-8").split(" (UUID")[0])
    return gpu_names


async def set_device_in_shared(device: str):
    init_device = {}
    init_device[INIT_DEVICE] = device

    save_shared_values(init_device,save=True)


async def set_device():
    if torch.cuda.is_available():
        gpu_name = get_gpu_names().pop()
        await set_device_in_shared(CUDA)
        print(f"Using GPU {gpu_name}")
        logging.info(f"Using GPU {gpu_name}")
    else:
        await set_device_in_shared(CPU)
        print(f"Using CPU For All Tasks")
        logging.info(f"Using CPU For All Tasks")
