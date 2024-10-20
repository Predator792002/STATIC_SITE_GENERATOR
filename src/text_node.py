class TextNode:
    def __init__(self, text, text_type, url=None, alt=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.alt = alt

    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url and self.alt == other.alt)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url}, {self.alt})"
    
    