import re

def markdown_to_block(markdown):
    Blocks = []
    block_list = markdown.split("\n\n")
    for block in block_list:
        block = block.strip()
        if block != "":
            Blocks.append(block)

    return Blocks


def is_sequential_ordered_list(block):
    lines = block.split("\n")
    expected_num = 1  # Start at 1 for ordered lists
    for line in lines:
        match = re.match(r"^(\d+)\.\s", line)
        if match:
            num = int(match.group(1))
            if num != expected_num:
                return False
            expected_num += 1
        else:
            return False
    return True

def block_to_block_type(block):

    if block.startswith("```") and block.endswith("```"):
        return "Code"

    elif re.match(r"^#{1,6}\s",block):
        return "Heading"
    
    elif re.match(r"^>\s",block):
        return "Quote"
    
    elif re.match(r"^[-*]\s",block):
        return "Unordered list"
    
    elif is_sequential_ordered_list(block):
        return "Ordered list"
    
    elif re.match(r"^(?!(```|>|[-*+]\s|\d+\.\s)).+",block):
        return "Paragraph"