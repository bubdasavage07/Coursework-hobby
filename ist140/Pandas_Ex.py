from sympy import true
import pandas as pd

pd.options.display.max_rows = 9999


from pathlib import Path
base_dir = Path(__file__).parent

data2D_array = {
    "calories":[420, 380, 390],
    "duration": [50, 40, 45]
}

#load data into a DataFrame object:
df =pd.DataFrame(data2D_array)
df2 = pd.read_csv(base_dir / 'workoutData.csv')
df2.dropna(inplace = True)

th = pd.read_csv(base_dir / 'treasure_hunt.csv')
new_th = th.dropna().copy()

new_th = new_th.astype(int, errors="ignore")
print(new_th)
#print(df2)

#print(df)
#print(df.loc[0])
#print(df.loc[[0,1]])
#print(df.info())

print()
#df.corr()
#print(df2.corr())
print(new_th.corr())