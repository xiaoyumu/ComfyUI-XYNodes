import unittest

import nodes


class PrimitiveBBOXTest(unittest.TestCase):
    def test_xywh_box(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("XYWH", 100, 200, 512, 512)

        expected = ((100, 200, 512, 512), 100, 200, 612, 712, 512, 512)

        self.assertEqual(expected, actual)

    def test_xyxy_box(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("XYXY", 100, 200, x_max=612, y_max=712)

        expected = ((100, 200, 512, 512), 100, 200, 612, 712, 512, 512)

        self.assertEqual(expected, actual)

    def test_cxcywh_box(self):
        box = nodes.PrimitiveBBOX()
        actual = box.primitive_bbox("CXCYWH", 356, 456, width=512, height=512)

        expected = ((100, 200, 512, 512), 100, 200, 612, 712, 512, 512)

        self.assertEqual(expected, actual)

    def test_unsupported_bbox_type(self):
        box = nodes.PrimitiveBBOX()
        with self.assertRaises(ValueError) as captured:
            box.primitive_bbox("UKN", 356, 456, width=512, height=512)

        self.assertEqual("Unsupported bbox type 'UKN'", str(captured.exception))
