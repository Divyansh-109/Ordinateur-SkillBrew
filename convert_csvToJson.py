import pandas as pd

data = pd.read_csv('data.csv')
data.to_json('data.json')