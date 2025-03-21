import pandas as pd


def user_loop(file):
    # Read excel file
    df = pd.read_excel(file)

    # Select the columns you want (e.g.: B, D, and H)
    columnas_deseadas = df.iloc[:, [3]]

    links = []

    # Iterate over the rows and obtain the values.
    for index, fila in columnas_deseadas.iterrows():
        # Access by name or column index
        link = fila.iloc[0]
        links.append(link)

    return tuple(links)
