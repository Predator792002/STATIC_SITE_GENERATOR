import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from text_node import TextNode

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

#  Parent node test
    def test_no_tag_no_child(self):
        with self.assertRaises(ValueError):
            ParentNode(tag = None, children=[]).to_html()
    
    def test_no_tag(self):
        child_node = LeafNode("h2", "Child content")
        with self.assertRaises(ValueError):
            ParentNode(tag = None, children=[child_node]).to_html()

    def test_no_child(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("p", []).to_html()
        self.assertEqual(str(context.exception), "NO CHILDREN")
    
        
    def test_correct_html_string(self):
        child_node = LeafNode("h2", "Child content")
        node = ParentNode("h1", [child_node], {"class": "heading"})
        self.assertEqual(node.to_html(), '<h1 class="heading"><h2>Child content</h2></h1>')
    
    def test_nested_parentNode(self):
        child_node = LeafNode("b", "Child content")
        p1_node = ParentNode("p", [child_node])
        p2_node = ParentNode("div", [p1_node])
        self.assertEqual(p2_node.to_html(), '<div><p><b>Child content</b></p></div>')

    def test_multiple_children(self):
        child_node1 = LeafNode("b", "Child content")
        child_node2 = LeafNode("i", "New Child content")
        p_node = ParentNode("p", [child_node1, child_node2])
        self.assertEqual(p_node.to_html(), '<p><b>Child content</b><i>New Child content</i></p>')




# text_nod conversion tests
    def test_text_type_text(self):
        text_node = TextNode(text="Hello, world!", text_type="text")
        result = text_node_to_html_node(text_node)

        assert isinstance(result, LeafNode)
        assert result.tag == ""
        assert result.text == "Hello, world!"
    
    def test_text_bold_type(self):
        text_node = TextNode(text = "Hello, world!", text_type = "bold")
        result = text_node_to_html_node(text_node)

        assert isinstance(result, LeafNode)
        assert result.tag == "b"
        assert result.text == "Hello, world!"

    def test_text_italic_type(self):
        text_node = TextNode(text = "Hello, world!", text_type = "italic")
        result = text_node_to_html_node(text_node)

        assert isinstance(result, LeafNode)
        assert result.tag == "i"
        assert result.text == "Hello, world!"

    def test_text_code_type(self):
        text_node = TextNode(text = "Hello, world!", text_type = "code")
        result = text_node_to_html_node(text_node)

        assert isinstance(result, LeafNode)
        assert result.tag == "code"
        assert result.text == "Hello, world!"
    
    def test_text_link_type(self):
        text_node = TextNode(text ="World", text_type="link", url="http://www.example.com/test")
        result = text_node_to_html_node(text_node)

        assert isinstance(result, LeafNode)
        assert result.tag == "a"
        assert result.value == "World"
        assert result.props == {"href": text_node.url}
    
    def test_text_image_type(self):
        text_node = TextNode(text="Test Image", text_type="image", url="http://www.example.com/test")
        result = text_node_to_html_node(text_node)

        assert isinstance(result, LeafNode)
        assert result.tag == "img"
        assert result.text == ""
        assert result.props == {"src": text_node.url, "alt": text_node.alt}
    
if __name__ == "__main__":
    unittest.main()