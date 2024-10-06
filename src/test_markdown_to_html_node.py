import unittest
from Block_to_html import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_simple_paragraph(self):
        markdown = "This is a paragraph."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, 'div')
        self.assertEqual(html_node.children[0].tag, 'p')
        self.assertEqual(html_node.children[0].children[0].text, 'This is a paragraph.')

    def test_heading(self):
        markdown = "# Heading"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.children[0].tag, 'h1')
        self.assertEqual(html_node.children[0].children[0].text, 'Heading')

    def test_code_block(self):
        markdown = "```\ncode here\n```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.children[0].tag, 'pre')
        self.assertEqual(html_node.children[0].children[0].tag, 'code')
        self.assertEqual(html_node.children[0].children[0].children[0].text, 'code here')

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.children[0].tag, 'ul')
        self.assertEqual(len(html_node.children[0].children), 2)
        self.assertEqual(html_node.children[0].children[0].tag, 'li')
        self.assertEqual(html_node.children[0].children[0].children[0].text, 'Item 1')

    def test_ordered_list(self):
        markdown = "1. First\n2. Second"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.children[0].tag, 'ol')
        self.assertEqual(len(html_node.children[0].children), 2)
        self.assertEqual(html_node.children[0].children[0].children[0].text, 'First')

    def test_quote(self):
        markdown = "> This is a quote"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.children[0].tag, 'blockquote')
        self.assertEqual(html_node.children[0].children[0].text, 'This is a quote')


if __name__ == '__main__':
    unittest.main()