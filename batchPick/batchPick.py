import pandas
import pathlib

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
FILE_NAME = 'df_lines.csv'

df = pandas.read_csv(f"{CURRENT_DIRECTORY}/{FILE_NAME}")

print(df)