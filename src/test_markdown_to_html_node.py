import unittest
from Block_to_html import markdown_to_html_node, extract_title

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
    
    def test_empty_string(self):
        markdown = ""
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, 'div')  # Assuming root is a div
        self.assertEqual(len(html_node.children), 0)  # No children

    def test_whitespace_string(self):
        markdown = "    "
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.tag, 'div')  # Assuming root is a div
        self.assertEqual(len(html_node.children), 0)  # No children

    def test_mixed_content(self):
        markdown = "This is a paragraph.\n\n# Heading\n\n- Item 1\n- Item 2"
        html_node = markdown_to_html_node(markdown)
        
        self.assertEqual(html_node.tag, 'div')  # Assuming root is a div
        self.assertEqual(html_node.children[0].tag, 'p')
        self.assertEqual(html_node.children[0].children[0].text, 'This is a paragraph.')
        self.assertEqual(html_node.children[1].tag, 'h1')
        self.assertEqual(html_node.children[1].children[0].text, 'Heading')
        self.assertEqual(html_node.children[2].tag, 'ul')
        self.assertEqual(len(html_node.children[2].children), 2)

    def test_invalid_markdown(self):
        markdown = "**This is bold but not closed"
        with self.assertRaises(ValueError):
            markdown_to_html_node(markdown)

    def test_line_breaks(self):
        markdown = "This is a line.\nThis is another line."
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.children[0].tag, 'p')  # Assuming root is a div
        self.assertEqual(len(html_node.children), 2)
        self.assertEqual(html_node.children[0].tag, 'p')
        self.assertEqual(html_node.children[0].children[0].text, 'This is a line.')
        self.assertEqual(html_node.children[1].tag, 'p')
        self.assertEqual(html_node.children[1].children[0].text, 'This is another line.')

    def test_heading(self):
        markdown = "# Hello World.\n## this is test case"
        heading = extract_title(markdown)
        self.assertEqual(heading, "Hello World.")

    def test_no_heading(self):
        markdown = "This is a paragraph\nAnother paragraph"
        with self.assertRaises(ValueError):
            extract_title(markdown)


    def test_header_not_first(self):
        markdown = "Some text\n# The Title\nMore text"
        heading = extract_title(markdown)
        self.assertEqual(heading, "The Title")

    def test_extra_spaces(self):
        markdown = "#    Spaced    Title    "
        heading = extract_title(markdown)
        self.assertEqual(heading, "Spaced    Title")

    def test_empty_title(self):
        markdown = "#\nSome content"
        heading = extract_title(markdown)
        self.assertEqual(heading, "")

if __name__ == '__main__':
    unittest.main()