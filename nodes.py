PARENT_CATEGORY = "XY NODES"


class PrimitiveBBOX:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "box_type": (["XYWH", "XYXY", "CXCYWH"]),
                "x": ("INT", {"default": 0, "min": 0, "step": 1}),
                "y": ("INT", {"default": 0, "min": 0, "step": 1}),
                },
            "optional": {
                "width": ("INT", {"default": 512, "min": 1, "step": 1}),
                "height": ("INT", {"default": 512, "min": 1, "step": 1}),
                "x_max": ("INT", {"default": 0, "min": 0, "step": 1}),
                "y_max": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }

    CATEGORY = PARENT_CATEGORY + "/bbox"

    RETURN_TYPES = ("BBOX", "INT", "INT", "INT", "INT", "INT", "INT")
    RETURN_NAMES = ("bbox", "x_min", "y_min", "x_max", "y_max", "width", "height")
    FUNCTION = "primitive_bbox"

    def primitive_bbox(self, box_type: str, x: int, y: int, width=0, height=0, x_max=0, y_max=0):
        if box_type == "XYWH":
            bbox = (x, y, width, height)
            x_max = x + width
            y_max = y + height

            return bbox, x, y, x_max, y_max, width, height

        if box_type == "XYXY":
            assert x and x_max > x, "x_max must be greater than x"
            assert y and y_max > y, "y_max must be greater than y"
            width = x_max - x
            height = y_max - y
            bbox = (x, y, width, height)

            return bbox, x, y, x_max, y_max, width, height
        if box_type == "CXCYWH":
            half_width = int(width / 2)
            half_height = int(height / 2)

            x = x - half_width
            y = y - half_height

            bbox = (x, y, width, height)

            x_max = x + width
            y_max = y + height

            return bbox, x, y, x_max, y_max, width, height

        raise ValueError(f"Unsupported bbox type '{box_type}'")


NODE_CLASS_MAPPINGS = {
    "PrimitiveBBOX": PrimitiveBBOX
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PrimitiveBBOX": "Primitive BBOX"
}
