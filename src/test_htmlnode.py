import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_link, extract_markdown_images
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_href(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    
    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertTrue(
            result == ' href="https://www.google.com" target="_blank"' or 
            result == ' target="_blank" href="https://www.google.com"'
        )
    
    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "test", {"href":"https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">test</a>')

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_empty_string_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")
    
    def test_leaf_to_html_multiple_props(self):
        node = LeafNode("img", "Image description", {"src": "img.jpg", "alt": "An image", "width": "100"})
        self.assertEqual(node.to_html(), '<img src="img.jpg" alt="An image" width="100">Image description</img>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_delimiter(self):
        node = TextNode("This is **bold** node", TextType.NORMAL)
        split = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split, 
            [ 
                TextNode("This is ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" node", TextType.NORMAL),
            ]
        )

    def test_code_delimiter(self):
        node = TextNode("This is `code` node", TextType.NORMAL)
        split = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            split, 
            [ 
                TextNode("This is ", TextType.NORMAL),
                TextNode("code", TextType.CODE),
                TextNode(" node", TextType.NORMAL),
            ]
        )

    def test_italic_delimiter(self):
        node = TextNode("This is _code_ node", TextType.NORMAL)
        split = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            split, 
            [ 
                TextNode("This is ", TextType.NORMAL),
                TextNode("code", TextType.ITALIC),
                TextNode(" node", TextType.NORMAL),
            ]
        )

    def test_node_not_normal_delimiter(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("This is a bold node", TextType.BOLD)])

    def test_node_delimiter_not_closed(self):
        node = TextNode("This is a **bold node", TextType.NORMAL)
        with self.assertRaises(SyntaxError):  
            split_nodes_delimiter([node], "**", TextType.BOLD)
    
    def test_extract_markdown_images(self):
        text = "This is md image ![image alt text](https://i.imgur.com/zjjcJKZ.png)"
        self.assertListEqual(
            [("image alt text", "https://i.imgur.com/zjjcJKZ.png")], extract_markdown_images(text)    
        )

    def test_extract_markdown_link(self):
        text = "This is md link [link](https://www.boot.dev)"
        self.assertListEqual(
            [("link", "https://www.boot.dev")], 
            extract_markdown_link(text)    
        )

    def test_extract_markdown_link_multiple(self):
        text = "This is md link [link](https://www.boot.dev), This is md link2 [link2](https://www.boot.dev2)"
        self.assertListEqual(
            [
                ("link", "https://www.boot.dev"),
                ("link2", "https://www.boot.dev2")
            ], 
            extract_markdown_link(text)    
        )


if __name__ == "__main__":
    unittest.main()