from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image
import torch
# Load model to GPU
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
).to("cuda")

def generate_image(prompt, image_path, output_format):
    # Open and prepare image
    image = Image.open(image_path).convert("RGB").resize((512, 512))

    # Generate with Stable Diffusion pipeline
    result = pipe(prompt=prompt, image=image, strength=0.7, guidance_scale=8.5)

    # Define output filename
    extension = output_format.lower()
    if extension not in ["png", "jpg"]:
        raise ValueError("Unsupported format. Use 'png' or 'jpg'.")

    output_path = f"generated_image.{extension}"

    # Save image in chosen format
    if extension == "jpg":
        result.images[0].save(output_path, format="JPEG", quality=95)
    else:
        result.images[0].save(output_path, format="PNG")

    return output_path
# def generate_image(image_path):

#     openai.api_key = "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"

#     response = openai.Image.create_variation(
#         image=open(image_path, "rb"),  # Must be square PNG
#         n=1,
#         size="512x512"
#     )
#     image_url = response["data"][0]["url"]
#     # Download the image from the URL
#     image_data = requests.get(image_url).content

#     # Generate unique filename
#     output_path = "generated_image.png"

#     # Save image to disk
#     with open(output_path, "wb") as f:
#         f.write(image_data)

#     print(f"✅ Variation saved to: {output_path}")
#     return output_path
