import pdfkit

pdf_out = pdfkit.from_string(["html_1.html", "html_2.html"])
pdf_out.name = "report.pdf"
