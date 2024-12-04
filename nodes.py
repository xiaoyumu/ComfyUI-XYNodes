from .box_nodes import PrimitiveBBOX, StringToBBOX
from .image_nodes import AppyColor

NODE_CLASS_MAPPINGS = {
    "PrimitiveBBOX": PrimitiveBBOX,
    "StringToBBOX": StringToBBOX,
    "AppyColorToImage": AppyColor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PrimitiveBBOX": "Primitive BBOX",
    "StringToBBOX": "String To BBOX",
    "AppyColorToImage": "Apply Color To Image",
}
