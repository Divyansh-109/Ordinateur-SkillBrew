import fitz  # PyMuPDF

doc = fitz.open("Resume 2 (3).pdf")
text = ""

for page in doc:
    text += page.get_text()

with open("output.txt", "w", encoding="utf-8") as f:
    f.write(text)

with open("output.txt", "r", encoding="utf-8") as f:
    content = f.readlines()
    
txt = "".join(content)

pdf = fitz.open()
page = pdf.new_page()
page.insert_text((50, 50), txt, fontsize=16)
pdf.save("output.pdf")
pdf.close()

print("PDF text extraction and re-creation completed.")



