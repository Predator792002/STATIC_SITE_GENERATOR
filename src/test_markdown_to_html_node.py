import unittest
from Block_to_html import markdown_to_html_node

class TestMarkdownToHTMLNode(unittest.TestCase):
    
    def test_single_paragraph(self):
        markdown = "This is a paragraph."
        expected_html = "<div><p>This is a paragraph.</p></div>"

        # Assuming markdown_to_html_node returns HTML in string form, or equivalent representation
        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected_html)

    def test_heading(self):
        markdown = "# Heading 1"
        expected_html = "<div><h1>Heading 1</h1></div>"
        
        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected_html)
    
    def test_code_block(self):
        markdown = "```\nprint('Hello, world!')\n```"
        expected_html = "<div><pre><code>print('Hello, world!')</code></pre></div>"

        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected_html)

    def test_nested_elements(self):
        markdown = "# Heading\n\n- List item\n- Another item"
        expected_html = "<div><h1>Heading</h1><ul><li>List item</li><li>Another item</li></ul></div>"

        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected_html)


if __name__ == '__main__':
    unittest.main()