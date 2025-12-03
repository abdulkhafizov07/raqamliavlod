import markdown

with open("masala.md", "r", encoding="utf-8") as file:
    md_text = file.read()

html_text = markdown.markdown(md_text)
print(html_text)