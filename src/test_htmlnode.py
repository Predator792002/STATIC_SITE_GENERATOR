import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_basic_attributes(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_empty_properties(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), '')

    def test_none_properties(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')
    
    def test_mixed_characters(self):
        node = HTMLNode(props={"data-info": "some info", "class": "my-class"})
        self.assertEqual(node.props_to_html(), ' data-info="some info" class="my-class"')

# Leaf node test
    def test_no_child(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", value=None).to_html()
    
    def test_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_with_props(self):
        node = LeafNode("p", "Hello World!", {"class":"hello"})
        self.assertEqual(node.to_html(), '<p class="hello">Hello World!</p>')

if __name__ == "__main__":
    unittest.main()