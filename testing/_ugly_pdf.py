from weasyprint import HTML, CSS
import pandas as pd
import numpy as np
import string
import random
from io import BytesIO

message_start = """
<html lang=en>
<head>
  <meta charset=utf-8">
  <title>Questionnaire Response</title>"""

message_style = """
    <style type="text/css" media="screen">
    html {
        hyphens: auto;
    }
    .dataframe {
      font-size: 12px;
      font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
      border-collapse: collapse;
      width: 100%;
      border: 2px black;
      background-color: #F3F0EE;
      white-space: pre-wrap;
      overflow-wrap: break-word;
    }

    .dataframe td {
        border: 2px black;
    }

    .dataframe tr:nth-child(even) {
        background-color: #E6E7E8;
    }

    .dataframe tr:hover {
        background-color: lightgrey;
    }

    .dataframe th {
      text-align: center;
      font-weight: bold;
      background-color: #fb9dd4;
      padding: 0.25em;
      border: 2px black;
    }
    .dataframe th:nth-child(1) {
        width: 15%;
        white-space: pre-wrap;
        overflow-wrap: break-word;
        max-width: 300px;
    }
    .dataframe tr {
        text-align: center;
        border: 2px black;
    }
    .report-title {
        font-size: 20px;
        color: #58595B;
        font-weight: bold;
        font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
    }
    .report-subtitle {
        font-size: 16px;
        color: #58595B;
        font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
    }
    .report-footer {
        font-size: 12px;
        font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
        text-align: center;
        width: 100%;
        font-weight: bold;
    }
  </style>
</head>
<body>

"""

supplier = "Bobs Lab Supplies"
date = "01/01/2001"
email = "bob@labsupplies.com"
message_header = f"""
                <h1 class="report-title" align="center">Supplier Questionnaire From {supplier}</h1>
                <h2 class="report-subtitle" align="center">Completed by: {email}</h2>
                <h2 class="report-subtitle" align="center">Completed on: {date}</h2>
                """

today = "10/10/2021"
message_end = f"""
            <footer class="report-footer">
            <p>Report generated on: {today}</p>
            <p>RSSL QAU</p>
            </footer>
            </body>
            </html>"""


css_string = """

    html {
        lang: eng;
        hyphens: auto;
    }
    @page { size: A3; margin: 1cm }

    .dataframe {
      font-size: 12px;
      font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
      border-collapse: collapse;
      width: 100%;
      border: 2px black;
      background-color: #F3F0EE;
      white-space: pre-wrap;
      overflow-wrap: break-word;
    }

    .dataframe td {
        border: 2px black;
    }

    .dataframe tr:nth-child(even) {
        background-color: #E6E7E8;
    }

    .dataframe tr:hover {
        background-color: lightgrey;
    }

    .dataframe th {
      text-align: center;
      font-weight: bold;
      background-color: #fb9dd4;
      padding: 0.25em;
    }
    .dataframe th:nth-child(1) {
        width: 15%;
        white-space: pre-wrap;
        overflow-wrap: break-word;
        max-width: 300px;
    }
    .dataframe tr {
        text-align: center;
    }
    .report-title {
        font-size: 20px;
        color: #58595B;
        font-weight: bold;
        font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
    }
    .report-subtitle {
        font-size: 16px;
        color: #58595B;
        font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
    }
    .report-footer {
        font-size: 12px;
        font-family: Calibri,Candara,Segoe,Segoe UI,Optima,Arial,sans-serif;
        text-align: center;
        width: 100%;
        font-weight: bold;
    }"""


def prettify_df(dataframe):
    df_html = dataframe.to_html()
    data = message_start + message_header + message_style + df_html + message_end
    return data


def form_to_pdf(dataframe):

    # actually need to get email/date/company at some point - from session?
    # email = session['email']
    pdf_buffer = BytesIO()
    html = prettify_df(dataframe)
    # add "attachment=x" to write_pdf to attach form files etc to pdf
    pdf_buffer.write(HTML(string=html).write_pdf(stylesheets=[CSS(string=css_string)]))

    pdf_buffer.name = "Report.pdf"
    pdf_buffer.seek(0)
    return pdf_buffer

if __name__ == "__main__":
    num_strings = 50
    q = []
    a = []
    for i in range(num_strings):
        letters = string.ascii_letters
        s1 = ''
        s1 = s1.join(random.choice(letters) for i in range(100))
        s2 = ''
        s2 = s2.join(random.choice(letters) for i in range(400))
        q.append(s1)
        a.append(s2)

    df = pd.DataFrame(data=a, index=q, columns=['Answer'])
    form_to_pdf(df)
