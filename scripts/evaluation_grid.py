import os.path

import modules.scripts as scripts
import gradio as gr

from modules import shared, sd_samplers_common,images, sd_samplers, processing, sd_models, sd_vae
from modules.processing import Processed, process_images
from modules.sd_models import get_closet_checkpoint_match

from scripts.xyz_grid import Script as XyzScript
from scripts.xyz_grid import AxisOption,axis_options

import re


evalOptions = {
    "CFG": [6, '2,5,8', []],
    "Lora Strength":[7, '', []],
    "Sampler": [9, '', ['Euler a', 'DPM++ 2M SDE', 'DPM++ SDE Karras']],
    "Clip Skip": [17, '1,2', []],
    "Pretrained model": [10, '', [x for x in ['consistentFactor_euclidV51.safetensors [dcb8523aae]',
                           'realisticVisionV30_v30VAE.safetensors [c52892e92a]',
                           'v1-5-pruned-emaonly.safetensors [6ce0161689]',
                           "doesn'texist"]
              if get_closet_checkpoint_match(x) is not None]]
}

def generateLoraStrengths(prompt):
    split_prompt = prompt.split()
    lora_file = next((s for s in split_prompt if "lora" in s.lower()), None)

    if lora_file is None:
        raise RuntimeError(f"Could not find a lora reference in your prompt")
    
    if re.match(r"<lora:.+:[0-9]+(\.[0-9]+)?>", lora_file) is None:
        raise RuntimeError(f"Wrong lora format for lora file:{lora_file}")
    

    split_lora = lora_file.split(":")
    lora_stengths = []

    for strength in [1,0.7,0.4,0]:
        split_lora[2] = str(strength)
        lora_stengths.append(":".join(split_lora) + '>')

    return lora_stengths
    


class Script(scripts.Script):
    def title(self):
        return "Evaluation grid"
    
    def ui(self, is_img2img):
        self.xyzScript = XyzScript()
        self.xyzScript.current_axis_options = [x for x in axis_options if type(x) == AxisOption or x.is_img2img == is_img2img]

        checkbox = gr.CheckboxGroup(["CFG","Sampler","Clip Skip","Pretrained model", "Lora Strength"], value=["CFG", "Sampler", "Pretrained model"], label="Evaluation Options", info="Pick 3 only !")
        return [checkbox]
    
    def run(self, p, checkbox):

        if len(checkbox) != 3:
            raise RuntimeError(f"Please select exactly 3 options")
        
        print(checkbox, self.xyzScript.title(), " prompt: ", p.prompt)

        #Special use case for Lora Strength
        if 'Lora Strength' in checkbox:
            lora_strengths = generateLoraStrengths(p.prompt)

            #replace lora reference by first lora strength (this is primordial to use the S/R function in the xyz_grid.py)
            p.prompt = [lora_strengths[0] if 'lora' in s else s for s in p.prompt.split()]
            p.prompt = " ".join(p.prompt)

            evalOptions["Lora Strength"][1] = ','.join(lora_strengths)

        #TODO: Special use case for Lora Epoch

        return self.xyzScript.run(p,evalOptions[checkbox[0]][0], 
                             evalOptions[checkbox[0]][1], evalOptions[checkbox[0]][2], evalOptions[checkbox[1]][0], 
                             evalOptions[checkbox[1]][1], evalOptions[checkbox[1]][2], evalOptions[checkbox[2]][0], 
                             evalOptions[checkbox[2]][1], evalOptions[checkbox[2]][2], True, False, False, False, 0)