from split_blocks import markdown_to_block, block_to_block_type
from split_inline import text_to_textnodes
from htmlnode import text_node_to_html_node, ParentNode
from text_node import TextNode
import re
def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == "Code":
            code_content = block.strip('```\n')
            children = [text_node_to_html_node(TextNode(code_content, "code"))]
            block_node = ParentNode(tag='pre', children=[ParentNode(tag='code', children=children)])
            block_nodes.append(block_node)

        elif block_type == "Heading":
            level = determine_heading_level(block)
            heading_text = block[level:].strip()
            children = text_to_children(heading_text)
            block_node = ParentNode(tag=f'h{level}', children=children)
            block_nodes.append(block_node)

        elif block_type == "Quote":
            quote_text = block[2:]  # Strip '> ' marker
            children = text_to_children(quote_text)
            block_node = ParentNode(tag='blockquote', children=children)
            block_nodes.append(block_node)

        elif block_type == "Unordered list":
            items = create_list_items(block)
            block_node = ParentNode(tag='ul', children=items)
            block_nodes.append(block_node)

        elif block_type == "Ordered list":
            items = create_list_items(block, True)
            block_node = ParentNode(tag='ol', children=items)
            block_nodes.append(block_node)

        elif block_type == "Paragraph":
            paragraphs = block.split('\n')  # Split by line breaks
            for para in paragraphs:
                para = para.strip()  # Strip leading/trailing whitespace
                if para:  # Only create a paragraph node if it's not empty
                    children = text_to_children(para)
                    block_node = ParentNode(tag='p', children=children)
                    block_nodes.append(block_node)

    root_node = ParentNode(tag='div', children=block_nodes)
    return root_node


def text_to_children(text):
    # Step 1: Convert text into text nodes
    text_nodes = text_to_textnodes(text)
    
    # Step 2: Convert text nodes to HTML nodes
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    
    return html_nodes

def determine_heading_level(block):
    # Count the number of '#' characters at the start of the block
    count = 0
    for char in block:
        if char == '#':
            count += 1
        else:
            break
    return count

def create_list_items(block, ordered=False):
    items = []
    lines = block.split('\n')

    for line in lines:
        if ordered:
            match = re.match(r'^(\d+)\.\s+(.*)', line)
            if match:
                number, item_text = match.groups()
            else:
                item_text = line
        else:
            match = re.match(r'^[-*+]\s+(.*)', line)
            if match:
                item_text = match.group(1)
            else:
                item_text = line

        child_nodes = text_to_children(item_text)
        items.append(ParentNode(tag='li', children=child_nodes))
        
    return items

