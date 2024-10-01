import unittest

from text_node import TextNode
from split_inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_link, text_to_textnodes




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





    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("Hello world", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(result, [node])

    def test_split_nodes_delimiter_simple(self):
        node = TextNode("Hello **world**", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(result, [
            TextNode("Hello ", "text"),
            TextNode("world", "bold"),
            TextNode("", "text")
        ])

    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("**Hello** world **again**", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(result, [
            TextNode("", "text"),
            TextNode("Hello", "bold"),
            TextNode(" world ", "text"),
            TextNode("again", "bold"),
            TextNode("", "text")
        ])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bolded** word", "text")
        result = split_nodes_delimiter([node], "**", "bold")
        self.assertEqual(result, [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word", "text")
        ])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an *italic* word", "text")
        result = split_nodes_delimiter([node], "*", "italic")
        self.assertEqual(result, [
            TextNode("This is text with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word", "text")
        ])

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code` word", "text")
        result = split_nodes_delimiter([node], "`", "code")
        self.assertEqual(result, [
            TextNode("This is text with a ", "text"),
            TextNode("code", "code"),
            TextNode(" word", "text")
        ])



    
    def test_single_image(self):
        text = "Here's an image: ![alt text](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image.jpg")])

    def test_multiple_images(self):
        text = "Two images: ![img1](https://example.com/1.jpg) and ![img2](https://example.com/2.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("img1", "https://example.com/1.jpg"), ("img2", "https://example.com/2.jpg")])

    def test_no_images(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        self.assertEqual(result, [])


        

    def test_single_links(self):
        text = "Here's an image: [alt text](https://example.com/image.jpg)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("alt text", "https://example.com/image.jpg")])

    def test_multiple_links(self):
        text = "Two images: [img1](https://example.com/1.jpg) and [img2](https://example.com/2.jpg)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("img1", "https://example.com/1.jpg"), ("img2", "https://example.com/2.jpg")])

    def test_no_links(self):
        text = "This text has no images."
        result = extract_markdown_links(text)
        self.assertEqual(result, [])
        

    
    def test_split_no_images(self):
        node = TextNode("Here is some text without images.", "text")
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("Here is some text without images.","text")
        ])

    def test_split_single_image(self):
        node = TextNode("Text with an image ![alt](link)", "text")
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("Text with an image ","text"),
            TextNode("alt","image","link")
        ])
        
    def test_split_multiple_images(self):
        node = TextNode("An image ![first](link1) and another ![second](link2)", "text")
        result = split_nodes_images([node])
        self.assertEqual(result, [
            TextNode("An image ","text"),
            TextNode("first","image","link1"),
            TextNode(" and another ","text"),
            TextNode("second","image","link2")
        ])

    def test_split_edge_cases(self):
        node = TextNode("![onlyimage](link)", "text")
        result = split_nodes_images([node])
        self.assertEqual(result,[
            TextNode("onlyimage","image","link"),
        ])



    def test_split_no_links(self):
        node = TextNode("Here is some text without links.", "text")
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Here is some text without links.","text")
        ])

    def test_split_single_links(self):
        node = TextNode("Text with a link [alt](link)", "text")
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("Text with a link ","text"),
            TextNode("alt","link","link")
        ])
        
    def test_split_multiple_links(self):
        node = TextNode("A link [first](link1) and another [second](link2)", "text")
        result = split_nodes_link([node])
        self.assertEqual(result, [
            TextNode("A link ","text"),
            TextNode("first","link","link1"),
            TextNode(" and another ","text"),
            TextNode("second","link","link2")
        ])

    def test_split_edge_links(self):
        node = TextNode("[onlylink](link)", "text")
        result = split_nodes_link([node])
        self.assertEqual(result,[
            TextNode("onlylink","link","link"),
        ])

    def test_text_to_textnodes_mixed(self):
        text = "This is **bold** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        # Now, you'd want to assert that the result matches what you expect
        self.assertEqual(result, [
    TextNode("This is ", "text"),
    TextNode("bold", "bold"),
    TextNode(" with an ", "text"),
    TextNode("italic", "italic"),
    TextNode(" word and a ", "text"),
    TextNode("code block", "code"),
    TextNode(" and an ", "text"),
    TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", "text"),
    TextNode("link", "link", "https://boot.dev"),
])
        

if __name__ == "__main__":
    unittest.main()
