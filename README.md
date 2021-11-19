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
