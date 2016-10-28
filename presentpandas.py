import pandas as pd
data = pd.read_csv("/home/paul/Schreibtisch/test.csv", delimiter=",")
data.plot(x='Col1', y='Col2')