from typing import List, Union
from PyML import Document, HtmlNode

class Table(HtmlNode):
    def __init__(self):
        self.__doc = Document()
        super().__init__("table")
        self.append_child(self.__doc.create_element("thead"))
        self.append_child(self.__doc.create_element("tbody"))
    
    def add_header(self, name: str):
        th = self.__doc.create_element("th")
        th.append_child(self.__doc.create_text_node(name))
        self.find("thead").append_child(th)
    
    def add_headers(self, headers: List[str]):
        for header in headers:
            self.add_header(header)
    
    def add_col(self, fields: Union[List[str], str]):
        if type(fields) is str:
            fields = [fields]
        tr = self.__doc.create_element("tr")
        for field in fields:
            td = self.__doc.create_element("td")
            td.append_child(self.__doc.create_text_node(field))
            tr.append_child(td)
        self.find("tbody").append_child(tr)
