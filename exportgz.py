import pandas as pd
import pathlib
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
pd.read_csv(
        DATA_PATH.joinpath("USDCHF.csv.gz"), index_col=1, parse_dates=["Date"]
    ).to_csv('USDCHF.csv')