import unittest
from textnode import TextNode, TextType
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("Text node", TextType.CODE)
        node2 = TextNode("Text node", TextType.CODE, "test")
        self.assertNotEqual(node, node2)

        node3 = TextNode("Text node", TextType.CODE)
        node4 = TextNode("Text node", TextType.BOLD)
        self.assertNotEqual(node3, node4)

        node5 = TextNode("Text node", TextType.IMAGE)
        node6 = TextNode("Text node", TextType.ITALIC, "")
        self.assertNotEqual(node5, node6)

if __name__ == "__main__":
    unittest.main()