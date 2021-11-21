# PyML
A python HTML builder library.


# Goals
- [x] Fully functional html builder similar to the javascript node manipulation.
- [ ] Implement an html parser that returns a Document instance with the proper properties and children.
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
title = doc.create_element("title")
title.append_child(doc.create_text_node("Example title!"))

doc.head.append_child(title)
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


# Contributing
Anybody is free to contribute if they want, just make sure you follow the points listed below:
- Don't rename/move methods/objects without consulting me first.
- Don't introduce new functionality without explaining in-depth why we need said functionality (unless its from the [Goals](#goals) section)
- Your code must be PEP-8 compliable.
