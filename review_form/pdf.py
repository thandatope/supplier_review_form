"""
https://towardsdatascience.com/simple-little-tables-with-matplotlib-9780ef5d0bc4

Some info

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from io import BytesIO



def generate_pdf(dataframe):
    # define figure and axes
    fig, ax = plt.subplots()

    rcolors = np.full(len(dataframe.index), 'linen')
    ccolors = np.full(len(dataframe.columns), 'lavender')

    ax.axis('off')

    # create table
    table = ax.table(cellText=dataframe.values,
                     colColours=ccolors,
                     colLabels=dataframe.columns,
                     cellLoc='center',
                     rowColours=rcolors,
                     rowLabels=dataframe.index,
                     fontsize=12,
                     loc='center'
                     )
    table.scale(1.25, 1.25)
    table.set_fontsize(12)

    pdf_io = BytesIO()

    # save pdf
    plt.savefig(pdf_io, format="pdf", dpi=200, bbox_inches='tight')
    pdf_io.seek(0)
    return pdf_io


if __name__ == "__main__":
    df = pd.DataFrame(np.random.randint(100,size=(50, 2)),columns=['A', 'B'])
    buffer = generate_pdf(df)
    print(buffer.getvalue())
    print(buffer)
    buffer.name = "butt.pdf"
    print(f"name: {buffer.name}")
