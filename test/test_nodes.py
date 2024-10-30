import unittest

import nodes


class PrimitiveBBOXTest(unittest.TestCase):
    def test_xywh_box(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("XYWH", "XYWH",100, 200, 512, 512)

        expected = ([(100, 200, 512, 512)], 100, 200, 612, 712, 512, 512)

        self.assertEqual(expected, actual)

    def test_xyxy_box(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("XYXY", "XYWH",100, 200, x_max=612, y_max=712)

        expected = ([(100, 200, 512, 512)], 100, 200, 612, 712, 512, 512)

        self.assertEqual(expected, actual)

    def test_cxcywh_box(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("CXCYWH", "XYWH",356, 456, width=512, height=512)

        expected = ([(100, 200, 512, 512)], 100, 200, 612, 712, 512, 512)

        self.assertEqual(expected, actual)

    def test_unsupported_bbox_type(self):
        box = nodes.PrimitiveBBOX()
        with self.assertRaises(ValueError) as captured:
            box.primitive_bbox("UKN", "XYWH",356, 456, width=512, height=512)

        self.assertEqual("Unsupported bbox type 'UKN'", str(captured.exception))

    def test_xywh_box_output_xyxy(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("XYWH", "XYXY",100, 200, 512, 512)

        expected = ([(100, 200, 612, 712)], 100, 200, 612, 712, 512, 512)
        self.assertEqual(expected, actual)

    def test_xywh_box_output_cxcywh(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("XYWH", "CXCYWH",100, 200, 512, 512)

        expected = ([(356, 456, 512, 512)], 100, 200, 612, 712, 512, 512)
        self.assertEqual(expected, actual)
        
