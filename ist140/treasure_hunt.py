import pandas as pd
from pathlib import Path
base_dir = Path(__file__).parent
"""
f=open(base_dir / "file.txt")
print(f.read())
f.close()

th=open(base_dir / "treasure_hunt.csv")
print(th.read())
th.close()
"""

df=pd.read_csv(base_dir / "treasure_hunt.csv")
print(df.to_string())
