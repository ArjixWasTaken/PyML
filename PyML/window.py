from PyML.main import Document, HtmlNode, TextNode, indent, INDENT_LEVEL
from bs4.element import NavigableString, Stylesheet, Script
from requests import get as get_html
from bs4 import BeautifulSoup
from typing import Optional


def parse_soup_into_tag(soup: BeautifulSoup):
    node = HtmlNode(soup.name)

    if type(soup) in (NavigableString, Stylesheet, Script):

        if type(soup) is NavigableString:
            node = TextNode(str(soup))
        else:
            node = TextNode(indent(str(soup), INDENT_LEVEL))
    try:
        for key, value in soup.attrs.items():
            node.set_attribute(key, " ".join(
                value) if type(value) is list else value)

        for child in soup.childGenerator():
            node.append_child(parse_soup_into_tag(child))
    except AttributeError:
        pass

    return node


class Location:
    def __init__(self, window: "Window") -> None:
        self.__window = window
        self.__href = None

    @property
    def href(self) -> Optional[str]:
        return self.__href

    @href.setter
    def href(self, url: str):
        html = get_html(url)
        self.__href = html.url

        soup = BeautifulSoup(html.text, "html.parser")
        self.__window.document = parse_soup_into_tag(soup.find("html"))

    def refresh(self):
        html = get_html(self.__href).text
        soup = BeautifulSoup(html, "html.parser")

        self.__window.document = parse_soup_into_tag(soup.find("html"))


class Window:
    def __init__(self) -> None:
        self.location = Location(self)
        self.document = Document()
