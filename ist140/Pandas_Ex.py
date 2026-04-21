import pandas as pd

data2D_array = {
    "calories":[420, 380, 390],
    "duration": [50, 40, 45]
}

#load data into a DataFrame object:
df =pd.DataFrame(data2D_array)

print(df)