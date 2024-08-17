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
       
        html_string = f"<{self.tag}>"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"

