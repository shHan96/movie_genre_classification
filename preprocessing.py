import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('movies_data_fin.csv',encoding='cp949')
#print(df.head())
df.info()
#print(df[df['Description'].isnull()].index.to_list())
df.drop(df[df['Description'].isnull()].index.to_list(),inplace=True)
df.info()
shuffled_df = df.sample(frac=1, random_state=42)
print(shuffled_df.head())
shuffled_df.drop_duplicates(subset=['Title'],inplace=True,keep='first')
shuffled_df.info()
shuffled_df.sort_values(by='Genre',inplace=True)
print(shuffled_df)


