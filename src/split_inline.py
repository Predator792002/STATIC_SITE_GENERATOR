from text_node import TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == "text":
            parts = node.text.split(delimiter)
            if len(parts) == 1:
                # No delimiter found, keep the original node
                new_nodes.append(node)
            else:
                if len(parts) % 2 == 0:
                    raise ValueError(f"Invalid Markdown syntax: Unclosed {delimiter} delimiter")
                for i in range(len(parts)):
                    if i % 2 == 0:
                        # Even index: "text" type
                        new_nodes.append(TextNode(parts[i], "text"))
                    else:
                        if not parts[i]:
                            raise ValueError(f"Invalid Markdown syntax: Empty {delimiter} section")
                        new_nodes.append(TextNode(parts[i], text_type))
        else:
            # Node is not "text" type, keep it as is
            new_nodes.append(node)
    
    return new_nodes


def extract_markdown_images(text):
    images_list = re.findall(r"\!\[(.*?)\]\((.*?)\)",text)
    return images_list

def extract_markdown_links(text):
    link_list = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)",text)
    return link_list

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        while True:
            images_link_list = extract_markdown_images(node.text)
            if not images_link_list:
                new_nodes.append(node)
                break

            image_alt, image_link = images_link_list[0]
            sections = node.text.split(f"![{image_alt}]({image_link})", 1)
            section_text = sections[0]
            if section_text:
                new_nodes.append(TextNode(section_text, "text"))

            new_nodes.append(TextNode(image_alt, "image", image_link))

            remaining_text = sections[1] if len(sections) > 1 else None
            if not remaining_text:
                break 

            node = TextNode(remaining_text, node.text_type)

    return new_nodes


def split_nodes_link(old_nodes):
    new_node = []
    for node in old_nodes:
        while True:
            link_list = extract_markdown_links(node.text)
            if not link_list:
                new_node.append(node)
                break

            link_alt, link = link_list[0]
            sections = node.text.split(f"[{link_alt}]({link})", 1)
            sections_text = sections[0]
            if sections_text:
                new_node.append(TextNode(sections_text, "text"))
            
            new_node.append(TextNode(link_alt, "link", link))

            remaining_text = sections[1] if len(sections) > 1 else None
            if not remaining_text:
                break

            node = TextNode(remaining_text, node.text_type)
    return new_node




def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    
    return nodes
