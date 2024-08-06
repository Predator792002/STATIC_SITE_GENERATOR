import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test_differ_text(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("Different text", "bold")
        self.assertNotEqual(node, node2)

    def test_differ_text_type(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_None_type(self):
        node = TextNode(None, "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a text node", "bold", url=None)
        node2 = TextNode("This is a text node", "bold", url="http://example.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
