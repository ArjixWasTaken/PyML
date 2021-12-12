from typing import Dict, List, Tuple
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
    return Token(lexer.row, lexer.col, *pair)


HTML_SYNTAX = flexicon.Lexer(_process_token).simple(
    (r'[ \t\r\n]+', lambda: ('WS',)),
    (r'(<\w+(?:.*?)?/>)', lambda val: ('SELF_CLOSING_TAG', val)),
    (r'(<\w+(?:.*?)?>)', lambda val: ('OPENING_TAG', val)),
    (r'(</\w+>)', lambda val: ('CLOSING_TAG', val)),
    (r'([\d\w]*)', lambda val: ("TEXT", val))
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
        while self.name is name:
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


if __name__ == "__main__":
    from PyML import HtmlNode, TextNode, Document

    sample = """
        <html hmm="2px">
            <head></head>
            <body>
                <div>
                    <a href="https://google.com"></a>
                    <br />
                </div>
                <p></p>
                <p></p>
            </body>
        </html>
    """

    stack: List[HtmlNode] = []
    doc = None
    tokens = HTML_SYNTAX.lex(sample)
    depth = 0
    itr = TokenIterator(tokens)

    while itr.token is not None:
        itr.burn('WS')
        if itr.token:
            if itr.token.name == "OPENING_TAG":
                tag, attributes = parse_tag(itr.token.value)
                node = HtmlNode(tag)

                for key, value in attributes.items():
                    node.set_attribute(key, value)

                if stack:
                    stack[-1].append_child(node)
                stack.append(node)

            elif itr.token.name == "SELF_CLOSING_TAG":
                tag, attributes = parse_tag(itr.token.value)
                node = HtmlNode(tag)

                for key, value in attributes.items():
                    node.set_attribute(key, value)

                if len(stack) == 0:
                    doc = Document()
                    stack.extend([doc, doc.body])

                stack[-1].append_child(node)

            elif itr.token.name == "CLOSING_TAG":
                tag, attributes = parse_tag(itr.token.value)
                node = HtmlNode(tag)

                for key, value in attributes.items():
                    node.set_attribute(key, value)

                current_node = stack.pop()

                if current_node.tag != node.tag:
                    raise Exception(
                        "Closed an outer tag without closing the inner tag.")
                else:
                    pass
                if not len(stack):
                    stack.append(current_node)

                #  tag = re.sub(r'[<>/]', "", itr.token.value).strip()

            elif itr.token.name == "TEXT":
                node = TextNode(itr.token.value)
                if stack:
                    stack[-1].append_child(node)
            itr.next()
    print(stack[0])
