from typing import Optional, Union, List, Dict
from collections import defaultdict
from json import dumps as jsonify
import textwrap


__all__ = ["Document"]

STANDALONE_TAGS = [
    "br",
    "source",
    "input"
]
INDENT_LEVEL = 4


def indent(text, num):
    return textwrap.indent(text, num * " ")


class TextNode:
    def __init__(self, text):
        self.content = text

    def __repr__(self) -> str:
        return self.content


class HtmlNode:
    def __init__(self, tag):
        self.tag: str = tag
        self.parent_node: Optional[HtmlNode] = None

        self.__children: List[Union[TextNode, HtmlNode]] = []
        self.properties: Dict[str, Union[str, int]] = defaultdict(lambda: dict())  # noqa

    def append_child(self, node):
        if self.tag.lower() in STANDALONE_TAGS:
            raise Exception(
                "You can't append an element inside a self closing tag.")
        node.parent_node = self
        self.__children.append(node)

    def set_attribute(self, name, value, isProperty=True):
        if isProperty:
            name = "class" if name == "class_" else name
            self.properties[name] = value
        else:
            self.__setattr__(name, value)

    def __repr__(self) -> str:
        templ = "<{tag}{properties}>{children}</{tag}>" if self.tag.lower(
        ) not in STANDALONE_TAGS else "<{tag}{properties} />"
        return templ.format(
            tag=self.tag,
            properties=(" " if len(self.properties) else "") + " ".join(
                "{}=\"{}\"".format(key, value if type(
                    value) is not dict else jsonify(value))
                for key, value in self.properties.items()
            ),
            children="\n".join(str(x) for x in self.__children) if all(type(x) is TextNode for x in self.__children) else ("" if not len(self.__children) else "\n") + indent("\n".join(str(e) for e in self.__children), INDENT_LEVEL) + "\n"  # noqa
        )


class Document:
    def __init__(self):
        # Declaring at initialization so that it's not static.
        self.head = HtmlNode("head")
        self.body = HtmlNode("body")

    def create_element(self, tag: str, **kwargs) -> HtmlNode:
        node = HtmlNode(tag)
        for key in kwargs:
            node.set_attribute(key, kwargs[key])
        return node

    def create_text_node(self, text: str) -> TextNode:
        return TextNode(text)

    def append_child(self, node: Union[HtmlNode, TextNode]):
        node.parent_node = self.body
        self.body.append_child(node)

    def __repr__(self):
        return "<html>\n{}\n</html>".format(
            indent(str(self.head), INDENT_LEVEL) + "\n" +
            indent(str(self.body), INDENT_LEVEL)
        )
