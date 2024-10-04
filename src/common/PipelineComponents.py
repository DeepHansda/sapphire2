from diffusers import AutoencoderKL, StableDiffusionPipeline
import common.shared as sharedValues
import torch
from typing import Optional
from common.const import INIT_DEVICE, CHECKPOINT, LORA, VAE
from diffusers import (
    DPMSolverMultistepScheduler,
    DPMSolverSinglestepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    HeunDiscreteScheduler,
    KDPM2AncestralDiscreteScheduler,
    KDPM2DiscreteScheduler,
    LMSDiscreteScheduler,
    UniPCMultistepScheduler,
)


class PipelineComponents:
    def __init__(self):
        self.component_pipeline: StableDiffusionPipeline = None
        self.torch_float = torch.float16
        self.loaded_sharedValues = sharedValues.load_shared_values()
        self.device = self.loaded_sharedValues.get(INIT_DEVICE)

    def pipeline_setup(self):
        if self.device == "cpu":
            self.torch_float = torch.float32

        if CHECKPOINT in self.loaded_sharedValues:
            sd_model_path = self.loaded_sharedValues.get(CHECKPOINT)
        else:
            sd_model_path = "Lykon/DreamShaper"
        if self.device == "cuda":
            torch.cuda.empty_cache()
        if VAE in self.loaded_sharedValues:
            vae_path = self.loaded_sharedValues.get(VAE)
            vae = AutoencoderKL.from_single_file(
                vae_path, torch_dtype=self.torch_float
            ).to(self.device)
        else:
            vae = None

        comp_pipeline: StableDiffusionPipeline = (
            StableDiffusionPipeline.from_single_file(
                sd_model_path,
                torch_dtype=self.torch_float,
                use_safetensors=True,
                safety_checker=None,
            ).to(self.device)
        )
        if vae:
            comp_pipeline.vae = vae
        self.component_pipeline = comp_pipeline

    def get_pipeline(self, ues_lora: Optional[bool] = False) -> StableDiffusionPipeline:
        if ues_lora == True:

            lora_path = self.loaded_sharedValues.get(LORA)
            print(lora_path)
            # lora = "sapphire/backend/src/models/loras/ghibli_style_offset.safetensors"
            lora_weight_name = lora_path.split("/")[-1]
            lora_apdapter_name = lora_weight_name.split(".")[0]

            active_adapters = self.component_pipeline.get_active_adapters()
            if len(active_adapters) > 0 and lora_apdapter_name == active_adapters[0]:
                print(active_adapters)
                return self.component_pipeline

            # print(lora_weight_name)
            # print(lora_apdapter_name)
            if len(active_adapters) > 0:
                self.component_pipeline.unload_lora_weights()
                self.component_pipeline.unfuse_lora()
            self.component_pipeline.load_lora_weights(
                lora_path, weight_name=lora_weight_name, adapter_name=lora_apdapter_name
            )
            # self.component_pipeline = lora_pipeline
            return self.component_pipeline
        else:
            self.component_pipeline.unload_lora_weights()
            self.component_pipeline.unfuse_lora()
            active_adapters = self.component_pipeline.get_active_adapters()
            print(active_adapters)
            return self.component_pipeline

    def get_scheduler(self, scheduler_name: str, use_kerras: bool = False):

        scheduler_name = scheduler_name.lower()
        config = self.component_pipeline.scheduler.config

        scheduler_classes = {
            "eular": EulerDiscreteScheduler,
            "eular_a": EulerAncestralDiscreteScheduler,
            "heun": HeunDiscreteScheduler,
            "lms": LMSDiscreteScheduler,
            "unipc": UniPCMultistepScheduler,
            "dpm_2": KDPM2DiscreteScheduler,
            "dpm_2_a": KDPM2AncestralDiscreteScheduler,
            "dpmpp_2m": DPMSolverMultistepScheduler,
            "dpmpp_sde": DPMSolverSinglestepScheduler,
            "dpmpp_2m_sde": DPMSolverMultistepScheduler,
        }
        scheduler_class = scheduler_classes.get(scheduler_name)
        if scheduler_class:
            scheduler = scheduler_class.from_config(config)
            if use_kerras is True:
                scheduler.use_karras_sigmas = use_kerras
                # self.component_pipeline.scheduler.config.use_karras_sigmas = use_kerras
            return scheduler
        else:
            raise ValueError(f"Unsupported scheduler: {scheduler_name}")
