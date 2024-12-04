import re
from typing import List, Tuple

from .constants import PARENT_CATEGORY


class BBOXBase:
    @staticmethod
    def build_output_box(output_box_type: str,
                         x_min: int, y_min: int, width=0, height=0, x_max=0, y_max=0) -> (int, int, int, int):
        if output_box_type == "XYWH":
            return x_min, y_min, width, height

        if output_box_type == "XYXY":
            return x_min, y_min, x_max, y_max

        if output_box_type == "CXCYWH":
            return x_min + int(width / 2), y_min + int(height / 2), width, height
        return None


class PrimitiveBBOX(BBOXBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_box_type": (["XYWH", "XYXY", "CXCYWH"],),
                "output_box_type": (["XYWH", "XYXY", "CXCYWH"],),
                "x": ("INT", {"default": 0, "min": 0, "step": 1}),
                "y": ("INT", {"default": 0, "min": 0, "step": 1}),
                },
            "optional": {
                "width": ("INT", {"default": 0, "min": 0, "step": 1}),
                "height": ("INT", {"default": 0, "min": 0, "step": 1}),
                "x_max": ("INT", {"default": 0, "min": 0, "step": 1}),
                "y_max": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    CATEGORY = PARENT_CATEGORY + "/bbox"

    RETURN_TYPES = ("BBOX", "INT", "INT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("bboxes", "x_min", "y_min", "x_max", "y_max", "width", "height")
    FUNCTION = "primitive_bbox"

    def primitive_bbox(self, input_box_type: str, output_box_type: str, x: int, y: int, width=0, height=0, x_max=0, y_max=0):
        if input_box_type == "XYWH":
            x_max = x + width
            y_max = y + height
            return ([self.build_output_box(output_box_type, x, y, width, height, x_max, y_max)],
                    x, y, x_max, y_max, width, height)

        if input_box_type == "XYXY":
            assert x and x_max > x, "x_max must be greater than x"
            assert y and y_max > y, "y_max must be greater than y"
            width = x_max - x
            height = y_max - y

            return ([self.build_output_box(output_box_type, x, y, width, height, x_max, y_max)],
                    x, y, x_max, y_max, width, height)

        if input_box_type == "CXCYWH":
            half_width = int(width / 2)
            half_height = int(height / 2)

            x = x - half_width
            y = y - half_height

            x_max = x + width
            y_max = y + height

            return ([self.build_output_box(output_box_type, x, y, width, height, x_max, y_max)],
                    x, y, x_max, y_max, width, height)

        raise ValueError(f"Unsupported bbox type '{input_box_type}'")


class StringToBBOX(BBOXBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_box_type": (["XYWH"],),
                "output_box_type": (["XYWH", "XYXY", "CXCYWH"],),
                "text": ("STRING", {"multiline": True, "default": "(123, 456, 640, 480), (522, 356, 320, 240)"}),
            },
        }

    CATEGORY = PARENT_CATEGORY + "/bbox"

    RETURN_TYPES = ("BBOX",)
    RETURN_NAMES = ("bboxes",)
    FUNCTION = "string_to_bbox"

    _BOX_PATTERN = re.compile(r"\((\d+),\s*(\d+),\s*(\d+),\s *(\d+)\)")

    def string_to_bbox(self, input_box_type: str, output_box_type: str, text: str) -> List[Tuple[int, int, int, int]]:
        matches = re.findall(self._BOX_PATTERN, text)
        if not matches:
            raise ValueError(f"The text '{text}' does not contain any valid XYWH box.")
        boxes = []
        for x, y, width, height in matches:
            x = int(x)
            y = int(y)
            width = int(width)
            height = int(height)
            x_max = x + width
            y_max = y + height
            boxes.append(self.build_output_box(output_box_type, x, y,
                                               width=width, height=height, x_max=x_max, y_max=y_max))
        return boxes
