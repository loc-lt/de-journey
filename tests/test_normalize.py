from __future__ import annotations

import unittest

from tiki_crawler.normalize import normalize_description


class NormalizeDescriptionTests(unittest.TestCase):
    def test_normalize_description_extracts_text_and_images(self) -> None:
        html_text = """
        <p>Product <strong>Name</strong></p>
        <ul><li>Feature A</li><li>Feature B</li></ul>
        <p><img src="https://example.com/image.jpg" /></p>
        <p>Giá sản phẩm trên Tiki đã bao gồm thuế theo luật hiện hành.</p>
        """

        description, images = normalize_description(html_text)

        self.assertIn("Product Name", description)
        self.assertIn("- Feature A", description)
        self.assertIn("- Feature B", description)
        self.assertNotIn("Giá sản phẩm trên Tiki", description)
        self.assertEqual(images, ["https://example.com/image.jpg"])


if __name__ == "__main__":
    unittest.main()
