from typing import Iterator, Optional, Union, List, Dict
from collections import defaultdict
from json import dumps as jsonify
import itertools
import textwrap


__all__ = ["Document", "HtmlNode", "TextNode"]

STANDALONE_TAGS = [
    "br", "source", "input", "area",
    "iframe", "link", "meta", "param",
    "img", "col", "basefont", "base",
    "hr", "isindex"
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
    @property
    def children(self):
        return self.__children

    def __init__(self, tag):
        self.tag: str = tag
        self.parent_node: Optional[HtmlNode] = None

        self.__children: List[Union[TextNode, HtmlNode]] = []
        self.properties: Dict[str, Union[str, int]] = defaultdict(lambda: dict())  # noqa

    def remove(self):
        if type(self.parent_node) is Document:
            raise Exception("You can not remove a root element. (head/body)")

        self.parent_node.eject_child(self)
        self.tag = "DELETED"
        self.__children = []
        self.properties = {}

    def eject_child(self, child: Union["HtmlNode", TextNode]):
        if type(child.parent_node) is Document:
            raise Exception("You can not eject a root element. (head/body)")
        self.__children = list(
            filter(lambda x: x is not child, self.__children))
        child.parent_node = None

    @property
    def inner_text(self):
        out = []
        for child in self.children:
            if type(child) is TextNode:
                out.append(child.content)
            else:
                out.append(child.inner_text)
        return "\n".join(list(itertools.chain(out)))

    def find(self, tag: Optional[str] = None, id: Optional[str] = None, class_: Optional[str] = None, properties: Dict[str, str] = {}) -> Optional["HtmlNode"]:
        try:
            return next(self.find_all(tag, id, class_, properties))
        except StopIteration:
            return None

    def find_all(self, tag: Optional[str] = None, id: Optional[str] = None, class_: Optional[str] = None, properties: Dict[str, str] = {}) -> Iterator["HtmlNode"]:
        for child in self.children:
            booleans: List[bool] = []
            if type(child) is HtmlNode:
                if tag is not None:
                    booleans.append(child.tag.lower() == tag.lower())
                if id is not None:
                    booleans.append(child.properties.get("id", None) == id)
                if class_ is not None:
                    booleans.append(all(x in child.properties.get("class", "").split() for x in class_.split()))  # noqa
                if properties is not None:
                    for key, value in properties.items():
                        if key == "class":
                            booleans.append(all(x in child.properties.get("class", "").split() for x in value.split()))  # noqa
                            continue
                        if key in child.properties:
                            booleans.append(value == child.properties.get(key))
                        else:
                            booleans.append(False)
                if all(booleans):
                    yield child

                grandchild = child.find_all(tag, id, class_, properties)
                if grandchild:
                    yield from grandchild

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


class Document(HtmlNode):
    def __init__(self):
        super().__init__("html")
        self.head = HtmlNode("head")
        self.body = HtmlNode("body")
        self.append_child(self.head)
        self.append_child(self.body)

        def append_child(node: Union[HtmlNode, TextNode]):
            node.parent_node = self.body
            self.body.append_child(node)

        # Hack-ish way to override this function after using it.
        self.append_child = append_child

    @property
    def title(self) -> Optional[str]:
        title_ = self.head.find("title")
        if title_ is not None:
            return title_.inner_text

    @title.setter
    def title(self, text: str):
        title_ = self.head.find("title")
        if title_ is not None:
            for child in title_.children:
                child.remove()
        else:
            title_ = self.create_element("title")
            self.head.append_child(title_)

        title_.append_child(self.create_text_node(text))

    @property
    def inner_text(self):
        return self.body.inner_text

    def create_element(self, tag: str, **kwargs) -> HtmlNode:
        node = HtmlNode(tag)
        for key in kwargs:
            node.set_attribute(key, kwargs[key])
        return node

    def create_text_node(self, text: str) -> TextNode:
        return TextNode(text)
