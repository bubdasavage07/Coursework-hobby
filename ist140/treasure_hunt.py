#Using the Pandas and Numpy libraries against 5 numbers
# between 1-30, drawn computer randomly
# Pandas: https://www.w3schools.com/python/pandas/default.asp
# Numpy: https://www.w3schools.com/python/numpy/default.asp

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

base_dir = Path(__file__).parent

pd.options.display.max_rows = 9999

th = pd.read_csv(base_dir / 'treasure_hunt.csv')
th.columns = th.columns.str.strip()
new_th = th.copy()
date_column = next((col for col in new_th.columns if col.lower() == 'date'), None)
number_columns = [col for col in new_th.columns if col != date_column]


new_th[number_columns] = new_th[number_columns].apply(pd.to_numeric, errors='coerce')
new_th.dropna(inplace=True)
new_th[number_columns] = new_th[number_columns].astype(int)

print(new_th)
print()

print(new_th.duplicated())
print(new_th.corr())

new_th.plot()

plt.show()


numpy_array = np.asarray(new_th)

print (numpy_array)

print("--Mean Calculation--")
x = np.mean(numpy_array)
y = stats.mode(numpy_array)
print(x)
print(y)
