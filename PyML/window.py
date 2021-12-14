from PyML.main import Document
from PyML.parser import doc_from_string
from requests import get as get_html
from typing import Optional


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

        self.__window.document = doc_from_string(html.text)

    def refresh(self):
        html = get_html(self.__href).text

        self.__window.document = doc_from_string(html)


class Window:
    def __init__(self) -> None:
        self.location = Location(self)
        self.document = Document()
