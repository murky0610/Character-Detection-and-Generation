import requests
import json
import base64
from PIL import Image
from io import BytesIO
import re

def text_to_image(keywords, batch_count=2, batch_size=2):
    url = 'http://demo.zktech.solutions:17861/sdapi/v1/txt2img'

    # Payload that contains the request data for the text-to-image generation
    payload = {
        "prompt": f"{keywords}, highly detailed, photorealistic, vibrant colors, clear focus",
        "batch_size": batch_size,
        "cfg_scale": 7,
        "comments": {},
        "denoising_strength": 0.7,
        "disable_extra_networks": False,
        "do_not_save_grid": False,
        "do_not_save_samples": False,
        "enable_hr": False,
        "height": 512,
        "hr_negative_prompt": '',
        "hr_prompt": '',
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_scale": 2,
        "hr_second_pass_steps": 0,
        "hr_upscaler": 'Latent',
        "n_iter": batch_count,  # Number of batches to generate
        "negative_prompt": 'nsfw, (deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation',
        "override_settings": {},
        "override_settings_restore_afterwards": True,
        "restore_faces": False,
        "s_churn": 0,
        "s_min_uncond": 0,
        "s_noise": 1,
        "s_tmax": None,
        "s_tmin": 0,
        "sampler_name": 'Euler a',
        "scheduler": 'Automatic',
        "script_args": [],
        "script_name": None,
        "seed": -1,
        "seed_enable_extras": True,
        "seed_resize_from_h": -1,
        "seed_resize_from_w": -1,
        "steps": 70,
        "styles": [],
        "subseed": -1,
        "subseed_strength": 0,
        "tiling": False,
        "width": 512,
    }

    # Send POST request to the API endpoint
    response = requests.post(url, data=json.dumps(payload), headers={"Content-Type": "application/json"})

    # Handle the response
    if response.status_code == 200:
        result = response.json()
        
        # Assuming the image is returned as a base64 string
        if 'images' in result:
            # Extract base64 image string from the response
            image_base64 = result['images'][0]  # Get the first image

            # Decode the base64 string into bytes
            image_data = base64.b64decode(image_base64)

            # Save the image to a file
            return Image.open(BytesIO(image_data))
        else:
            print("No image data in the response.")
    else:
        print(f"Failed with status code {response.status_code}")
        return None

# Function to extract character descriptions from the text
def extract_character_descriptions(text):
    # Using regex to find character descriptions
    character_descriptions = re.findall(r"(\d+\.\s+[^\n]+): (.+?)(?=\n\d+\.\s|$)", text, re.DOTALL)
   
    return character_descriptions

# Example usage
with open('character_descriptions.txt', 'r', encoding='utf-8') as file:
    keywords = file.read().strip()

# Extract character descriptions
character_descriptions = extract_character_descriptions(keywords)

# Loop through the descriptions and generate images
for index, (name, description) in enumerate(character_descriptions, start=1):
    print(f"Generating image for {name}...")
    
    # Generate image using the character's name and description as prompt
    prompt = f"{name}: {description}"
    image = text_to_image(prompt)
    print(prompt)
    if image:
        image_path = f"generated_image_{name}.png"
        image.save(image_path)
        print(f"Image saved to {image_path}")
    else:
        print(f"Failed to generate image for {name}.")
