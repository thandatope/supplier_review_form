from pdfrw import PdfWriter, PdfString, PdfDict, PdfName
from xhtml2pdf import pisa
from html.parser import HTMLParser
from bs4 import BeautifulSoup as bs
from io import TextIOWrapper
from bs4.diagnose import diagnose


def gen_pdf():
    with open('reports/html/report.html') as h:
        # soup = bs(h, 'html5lib')
        soup = h

        pdf_name = "test.pdf"
        result = open(pdf_name, "w+b")
        p = pisa.CreatePDF(
            src=soup,
            dest=result,
        )
        result.close()
        print(p)
        return p


if __name__ == "__main__":
    gen_pdf()
