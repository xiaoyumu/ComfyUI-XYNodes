import cv2
import numpy as np
import torch
from PIL import Image, ImageEnhance

from .constants import PARENT_CATEGORY


class AppyColor:
    @classmethod
    def INPUT_TYPES(cls):
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
        new_rgb_color = (r, g, b)
        result = torch.zeros_like(image)
        for index in range(batch_size):
            img = image[index].numpy()
            image_array = (img * 255).astype(np.uint8)
            grayscale_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            normalized_gray = grayscale_image / 255.0  # Normalize the grayscale image to [0, 1]
            for i in range(3):  # Iterate over each channel (R, G, B)
                image_array[:, :, i] = normalized_gray * new_rgb_color[i]
            image_array = np.clip(image_array, 0, 255).astype(np.uint8)
            image_array = image_array / 255
            result[index] = torch.from_numpy(image_array).unsqueeze(0)

        return (result,)


class ColorAdjust:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "temperature": ("FLOAT", {"default": 0, "min": -100, "max": 100, "step": 5}),
                "hue": ("FLOAT", { "default": 0, "min": -180, "max": 180, "step": 5}),
                "brightness": ("FLOAT", {"default": 0, "min": -100, "max": 100, "step": 5}),
                "contrast": ("FLOAT", {"default": 0, "min": -100, "max": 100, "step": 5}),
                "saturation": ("FLOAT", {"default": 0, "min": -100, "max": 100, "step": 5}),
                "gamma": ("FLOAT", {"default": 1, "min": 0.2, "max": 2.2, "step": 0.1 }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "color_adjust"

    CATEGORY = f"{PARENT_CATEGORY}/Color Adjustments"

    @staticmethod
    def color_adjust(image: torch.Tensor,
                     temperature: float,
                     hue: float,
                     brightness: float,
                     contrast: float,
                     saturation: float,
                     gamma: float):

        batch_size, height, width, _ = image.shape
        result = torch.zeros_like(image)

        brightness /= 100
        contrast /= 100
        saturation /= 100
        temperature /= 100

        brightness = 1 + brightness
        contrast = 1 + contrast
        saturation = 1 + saturation

        for index in range(batch_size):
            img = image[index].numpy()

            img = Image.fromarray((img * 255).astype(np.uint8))

            # Adjust brightness
            img = ImageEnhance.Brightness(img).enhance(brightness)

            # Adjust contrast
            img = ImageEnhance.Contrast(img).enhance(contrast)

            img_array: np.ndarray = np.array(img).astype(np.float32)

            # Adjust color temperature
            if temperature > 0:
                img_array[:, :, 0] *= 1 + temperature
                img_array[:, :, 1] *= 1 + temperature * 0.4
            elif temperature < 0:
                img_array[:, :, 2] *= 1 - temperature
            img_array = np.clip(img_array, 0, 255)/255

            # Adjust gamma
            img_array = np.clip(np.power(img_array, gamma), 0, 1)

            # Adjust saturation
            hls_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2HLS)
            hls_img[:, :, 2] = np.clip(saturation*hls_img[:, :, 2], 0, 1)
            img_array = cv2.cvtColor(hls_img, cv2.COLOR_HLS2RGB) * 255

            # Adjust hue
            hsv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            hsv_img[:, :, 0] = (hsv_img[:, :, 0] + hue) % 360
            img_array = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)

            img_array = img_array.astype(np.uint8) / 255
            result[index] = torch.from_numpy(img_array).unsqueeze(0)

        return (result, )
