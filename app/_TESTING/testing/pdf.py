import pandas
from fpdf import FPDF
import faker
import numpy as np
import dataframe_image as dfi
from PIL import Image
import io


def generate_test_dataframe():
    df = pandas.DataFrame(columns=["a", "b", "c", "d"])
    a = []
    b = []
    c = []
    d = []

    for i in range(100):
        a.append(faker.generator.random.random())
        b.append(faker.generator.random.random())
        c.append(faker.generator.random.random())
        d.append(faker.generator.random.random())

    df["a"] = a
    df["b"] = b
    df["c"] = c
    df["d"] = d

    return df


def generate_report(dataframe):
    b = io.BytesIO()
    dfi.export(dataframe, b)
    img = Image.open(b)
    img.split()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=16)
    pdf.cell(txt="Supplier Review", align="C", w=0)
    pdf.image("tmp.png", h=pdf.eph)
    pdf.output("a_1.pdf")


if __name__ == "__main__":
    df = generate_test_dataframe()
    generate_report(df)
