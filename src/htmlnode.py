class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html():
        raise NotImplementedError
    
    def props_to_html(self):
        prop_string = ""
        if not self.props:
            return ""
        for prop in self.props:
            prop_element = f'{prop}="{self.props[prop]}"'
            prop_string = prop_string + " " + prop_element
        return prop_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        self.text = value

    
    def to_html(self):
        if not self.value:
            raise ValueError
        
        if not self.tag:
            return self.value
        
        render_html_tag = f'"{self.tag}", {self.value}'
        if self.props:
            attributes = ''.join(f' {key}="{value}"' for key, value in self.props.items())
            return f'<{self.tag}{attributes}>{self.value}</{self.tag}>'
        else:
            return f'<{self.tag}>{self.value}</{self.tag}>'
    
    
        

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag = tag, value = None, children = children, props = props)
    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("NO CHILDREN")
        
        html_string = f"<{self.tag}"
        
        if self.props:
            for key in self.props:
                html_string = html_string + f' {key}="{self.props[key]}"'
        
        html_string = html_string + '>'
        
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        
        return html_string
    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode("", text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case "image":
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.alt})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")