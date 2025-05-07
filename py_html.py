class PyHTML:
    def __init__(self, title: str, stylesheet: str = None) -> None:
        self.doc = []
        if stylesheet is None:
            stylesheet = "https://classless.de/classless.css"
        head =f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <link rel="stylesheet" href="{stylesheet}">
          <title>{title}</title>
        </head>        
        """
        self.doc.append(head)
        self.doc.append("<body>\n")
        self.doc.append("</body>\n</html>")

    def h1(self, content: str) -> None:
        self.doc.insert(-1, f"<h1>{content}</h1>")

    def h2(self, content: str) -> None:
        self.doc.insert(-1, f"<h2>{content}</h2>")

    def h3(self, content: str) -> None:
        self.doc.insert(-1, f"<h3>{content}</h3>")

    def p(self, content: str) -> None:
        self.doc.insert(-1, f"<p>{content}</p>")

    def table(self, headers: list, rows: list[tuple]) -> None:
        tbl = []
        tbl.append(f"<table>")
        tbl.append(f"<tr>")
        for col in headers:
            tbl.append(f"<th>{col}</th>")
        tbl.append(f"</tr>")
        for row in rows:
            tbl.append(f"<tr>")
            for col in row:
                tbl.append(f"<td>{col}</td>")
            tbl.append(f"</tr>")
        tbl.append(f"</table>")
        self.doc.insert(-1, "\n".join(tbl))

    def render(self, filename: str) -> None:
        """
        Writes the HTML file to the file specified in the filename parameter.
        :param filename: The name of the HTML file that will be written
        :return: None
        """
        f = open(filename, "w")
        f.writelines(self.doc)
        f.close()

if __name__ == "__main__":
    test_html = PyHTML("Test")
    test_html.h1("Testing h1")
    test_html.h2("Testing h2")
    headers = ['Number', 'Letter']
    data = [(1, 'A'), (2, 'B'), (3, 'C')]
    test_html.table(headers, data)
    test_html.render("test.html")




