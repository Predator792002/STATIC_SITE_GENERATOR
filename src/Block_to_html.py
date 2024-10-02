from split_blocks import markdown_to_block, block_to_block_type
def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
