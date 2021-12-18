# PyML
A python HTML builder library.


# Goals
- [x] Fully functional html builder similar to the javascript node manipulation.
- [x] Implement an html parser that returns a Document instance with the proper properties and children.
- [ ] Prettify JavaScript to fit in with the prettified html.
- [ ] Add more API methods.
- [ ] Add CSS selector support.
- [ ] Add styling configuration.

# Usage
If you have ever manipulated html using JavaScript then this should be really intuitive.
You just use the document to create a node.
You then modify the node with the properties and children that you want.
And insert that node into the document.

```python
from PyML import Document

doc = Document()
doc.title = "Example title!"

print(doc)
```
results in
```html
<html>
    <head>
        <title>Example title!</title>
    </head>
    <body></body>
</html>
```

# Parsing html as a Document
Note: The parser is very experimental, that means that it might not be able to properly parse some html.
```python
from PyML.parser import doc_from_string

html = """
<html>
    <head>
        <title>Example title!</title>
    </head>
    <body>
        <div class="heh">
            <img src="myImage.png">
        </div>
    </body>
</html>
"""

doc = doc_from_string(html)
print(doc.title)
print(doc.find("img").properties["src"])
```


# Contributing
Anybody is free to contribute if they want, just make sure you follow the points listed below:
- Don't rename/move methods/objects without consulting me first.
- Don't introduce new functionality without explaining in-depth why we need said functionality (unless its from the [Goals](#goals) section)
- Your code must be PEP-8 compliable.
