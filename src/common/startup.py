from common.devices import set_device
from common.Folder_Paths import add_folders_in_models_folder, models_dir
from common.shared import save_shared_values, load_shared_values
from common.Utils import Utils
from common.const import CHECKPOINTS, CHECKPOINT, VAE
from common.Folder_Paths import Folder_paths, models_dir
import asyncio


commonUtils = Utils()
folder_path = Folder_paths()


async def startUp():

    print("start up function running")
    startup_event = asyncio.Event()
    await set_device()
    folder_path.add_init_folders()
    add_folders_in_models_folder()

    all_models = {}
    all_models = commonUtils.get_all_models()
    if CHECKPOINT not in all_models or VAE not in all_models:
        checkpoint_url = "https://huggingface.co/Lykon/DreamShaper/resolve/main/DreamShaper_8_pruned.safetensors"
        checkpoint_output_path = (
            f"{models_dir}/{CHECKPOINTS}/DreamShaper_8_pruned.safetensors"
        )
        vae_url = "https://huggingface.co/stabilityai/sd-vae-ft-ema-original/resolve/main/vae-ft-ema-560000-ema-pruned.safetensors"
        vae_output_path = f"{models_dir}/{VAE}/vae-ft-ema-560000-ema-pruned.safetensors"
        await commonUtils.download_with_wget(checkpoint_url, checkpoint_output_path)
        await commonUtils.download_with_wget(vae_url, vae_output_path)
        all_models = commonUtils.get_all_models()

    default_checkpoint = {}
    shard_values = load_shared_values()
    if CHECKPOINT not in shard_values or shard_values[CHECKPOINT] == "":
        checkpoint_name, checkpoint_path = next(
            iter(all_models.get(CHECKPOINTS, {}).items()), (None, None)
        )
        default_checkpoint[CHECKPOINT] = checkpoint_path

    if VAE not in shard_values or shard_values[VAE] == "":
        checkpoint_name, checkpoint_path = next(
            iter(all_models.get(VAE, {}).items()), (None, None)
        )
        default_checkpoint[VAE] = checkpoint_path

    save_shared_values(default_checkpoint, save=True)
    await startup_event.wait()
