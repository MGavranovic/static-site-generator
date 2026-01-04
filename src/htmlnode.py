from textnode import TextType, TextNode

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        return_string = ""
        for k, v in self.props.items():
            return_string = return_string + f" {k}=\"{v}\""
        return return_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode must have a value")
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have a tag")
        if self.children == None: 
            raise ValueError("ParentNode must have children")
        children_html = ""
        for c in self.children:
            children_html += c.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
             return LeafNode(None, f"{text_node.text}")
        case TextType.BOLD:
            return LeafNode("b", f"{text_node.text}")
        case TextType.ITALIC:
            return LeafNode("i", f"{text_node.text}")
        case TextType.CODE:
            return LeafNode("code", f"{text_node.text}")
        case TextType.LINK:
            return LeafNode("a", f"{text_node.text}", text_node.props)
        case TextType.IMAGE:
            props = []
            for p in text_node.props:
                props.append(p)
            return LeafNode("img", "", [text_node.src, text_node.alt])

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    rtrn_list = []
    for on in old_nodes:
        if on.text_type != TextType.NORMAL:
            rtrn_list.append(on)
            continue
        if on.text.count(delimiter) % 2 != 0:
            raise SyntaxError("Incorrect Markdown syntax")
        separated = on.text.split(delimiter)
        for i, s in enumerate(separated):
            if len(s) == 0:
                continue
            if i % 2 == 0:
                rtrn_list.append(TextNode(s, TextType.NORMAL))
            if i % 2 != 0:
                rtrn_list.append(TextNode(s, text_type))
    return rtrn_list        
        