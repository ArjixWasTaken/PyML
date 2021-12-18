from PyML.main import HtmlNode, TextNode, Document
from typing import Dict, List, Tuple, Union
import flexicon
import re


class Token(object):
    def __init__(self, line, column, name, value=None):
        self.line = line
        self.column = column
        self.name = name
        self.value = value

    def __repr__(self):
        return self.name


def _process_token(pair, lexer):
    if pair[0] == "STRING_WITH_TAG":
        raise NotImplemented(
            "Report this to the dev, along with the html that triggered it.:\n" + pair[1])
    return Token(lexer.row, lexer.col, *pair)


HTML_SYNTAX = flexicon.Lexer(_process_token).simple(
    (r'[ \t\r\n]+', lambda: ('WS',)),
    (r'<!(?:DOCTYPE|doctype) (.*?)>', lambda val: ("DOCTYPE", val)),
    (r'<!--((?:.|\s)*?)-->', lambda val: ("COMMENT", val)),  # noqa
    (r'<([^\/>]+)\/>', lambda val: ('SELF_CLOSING_TAG', val)),
    (r'(<\w+(?:(?:.|\s)*?)?>)', lambda val: ('OPENING_TAG', val)),
    (r'(</\w+>)', lambda val: ('CLOSING_TAG', val)),
    (r'((["\'`]).*?</?>.*?\2)', lambda val: ("STRING_WITH_TAG", val)),
    (r'(?s)(.+?)(?=</?\w+)', lambda val: ("TEXT", val))  # noqa
)


class TokenIterator(object):
    def __init__(self, tokens):
        self.tokens = tokens
        self.id = 0
        self.length = len(tokens)

    def next(self):
        self.id += 1
        return self.token

    @property
    def token(self):
        return self.tokens[self.id] if self.id < self.length else None

    @property
    def name(self):
        return self.token.name if self.id < self.length else None

    @property
    def value(self):
        return self.token.value if self.id < self.length else None

    @property
    def line(self):
        return self.token.line if self.id < self.length else None

    @property
    def column(self):
        return self.token.column if self.id < self.length else None

    def peek(self):
        return self.tokens[self.id + 1] if (self.id + 1) < self.length else None

    def expect(self, name):
        self.next()
        if self.name is not name:
            self.unexpected()
        return self

    def unexpected(self):
        val_fmt = ' ({})'.format(self.value) if self.value is not None else ''
        tkn_fmt = 'token {}'.format(
            self.name) if self.name is not None else 'EOF'
        err = Exception('unexpected {}{}'.format(tkn_fmt, val_fmt))
        err.line = self.line
        err.column = self.column
        raise err

    def burn(self, name):
        while self.name == name:
            self.next()


Attributes = Dict[str, str]


def parse_tag(tag: str) -> Tuple[str, Attributes]:
    attributes_re = r"(\b\w+\b)\s*(=\s*(\"[^\"]*\"|'[^']*'|[^\"'<>\s]+))?"
    tag, *attributes = tag.split(" ")

    if not len(attributes):
        tag = tag[:-1]

    attributes = {
        x[0]: True if not x[2] else x[2].strip('"')
        for x in re.findall(attributes_re, " ".join(attributes))
    }

    return tag.lstrip("<").lstrip("/"), attributes


def doc_from_string(html: str) -> Document:
    stack: List[HtmlNode] = []
    tokens = HTML_SYNTAX.lex(html)

    itr = TokenIterator(tokens)

    while itr.token is not None:
        itr.burn('WS')
        itr.burn('COMMENT')

        if itr.token:
            if itr.token.name == "OPENING_TAG":
                tag, attributes = parse_tag(itr.token.value)
                node = HtmlNode(tag)

                for key, value in attributes.items():
                    node.set_attribute(key, value)

                if stack:
                    stack[-1].append_child(node)

                if not node.isVoidElement():
                    stack.append(node)

            elif itr.token.name == "SELF_CLOSING_TAG":
                tag, attributes = parse_tag(itr.token.value)
                node = HtmlNode(tag)

                for key, value in attributes.items():
                    node.set_attribute(key, value)

                if stack:
                    stack[-1].append_child(node)
                else:
                    raise Exception("No 'html' tag was found.")

            elif itr.token.name == "CLOSING_TAG":
                tag, attributes = parse_tag(itr.token.value)
                node = HtmlNode(tag)

                for key, value in attributes.items():
                    node.set_attribute(key, value)

                current_node = stack.pop()

                if current_node.tag != node.tag:
                    raise Exception(
                        "Closed an outer tag ({}) without closing the inner tag ({})".format(current_node.tag, node.tag))
                else:
                    # Should be fine
                    pass
                if not len(stack):
                    stack.append(current_node)

            elif itr.token.name == "TEXT":
                node = TextNode(itr.token.value)
                if stack:
                    stack[-1].append_child(node)
            itr.next()

    doc = stack[0]
    doc.__class__ = Document
    doc.head = doc.find("head")
    doc.body = doc.find("body")

    def append_child(node: Union[HtmlNode, TextNode]):
        node.parent_node = doc.body
        doc.body.append_child(node)

    doc.append_child = append_child
    return doc
