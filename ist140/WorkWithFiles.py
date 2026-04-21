import pandas as pd
from pathlib import Path
f = open("/Users/ethan/CyberSecurity_classes/Random-Shit/ist140/file.txt")
#print(f.read())
#print(f.readline())
f.close()

th = open("/Users/ethan/CyberSecurity_classes/Random-Shit/ist140/treasure hunt.txt")
#print(th.read())
#print(th.readline())
th.close()

# ------ Original code ---------
print("------ Original code -------")
df = pd.read_csv('/Users/ethan/CyberSecurity_classes/Random-Shit/ist140/treasure_hunt.csv')
new_df = df.dropna()
print(new_df.to_string())

#The reason this happens is that Pandas traditionally
#uses floating-point numbers to represent
#"NaN" (missing values). Even if you use dropna() later,
#the column has already been coerced into a float.

#print(df.to_string())
#print(df)
#print(pd.options.display.max_rows)
#print(df.head(10))

#*******************************************
#****** Clean then Cast as  ****************
print("------ Clean then Cast -------")
df = pd.read_csv('/Users/ethan/CyberSecurity_classes/Random-Shit/ist140/treasure_hunt.csv')
new_df = df.dropna().copy() # .copy() prevents SettingWithCopy warnings

# Convert specific columns to int
# new_df['column_name'] = new_df['column_name'].astype(int)

# OR convert every numeric column that can be an int
new_df = new_df.astype(int, errors='ignore')

print(new_df.to_string())

#*******************************************
#****** Nullable Integers  ****************
# You can specify the type during the read
print("------ Nullable Integers -------")
df = pd.read_csv(
      '/Users/ethan/CyberSecurity_classes/Random-Shit/ist140/treasure_hunt.csv',
      na_values=['TBD'],
      dtype={
          'number_1': 'Int64',
          'number_2': 'Int64',
          'number_3': 'Int64',
          'number_4': 'Int64',
          'number_5': 'Int64'
      }
  )

new_df = df.dropna()
print(new_df.to_string())
