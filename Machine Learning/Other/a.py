import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("titanic.csv")
df['male'] = df["Sex"] == "male"

X = df.loc[:, ~df.columns.isin(["Survived", "Sex"])].values   # Selecting all columns except some
Y = df["Survived"].values

print(Y)
