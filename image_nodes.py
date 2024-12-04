import cv2
import numpy as np
import torch

from .constants import PARENT_CATEGORY


class AppyColor:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "r": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "g": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
                "b": ("INT", {"default": 0, "min": 0, "max": 255, "step": 1}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "apply_color"

    CATEGORY = f"{PARENT_CATEGORY}/Color Adjustments"

    @staticmethod
    def apply_color(image: torch.Tensor, r: int, g: int, b: int):
        batch_size, height, width, _ = image.shape
        new_bgr_color = (r, g, b)
        result = torch.zeros_like(image)
        for index in range(batch_size):
            img = image[index].numpy()
            image_array = (img * 255).astype(np.uint8)
            grayscale_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            normalized_gray = grayscale_image / 255.0  # Normalize the grayscale image to [0, 1]
            for i in range(3):  # Iterate over each channel (B, G, R)
                image_array[:, :, i] = normalized_gray * new_bgr_color[i]
            image_array = np.clip(image_array, 0, 255).astype(np.uint8)
            image_array = image_array / 255
            result[index] = torch.from_numpy(image_array).unsqueeze(0)

        return (result,)
