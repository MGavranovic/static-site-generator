import unittest
from htmlnode import HTMLNode, LeafNode

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

if __name__ == "__main__":
    unittest.main()