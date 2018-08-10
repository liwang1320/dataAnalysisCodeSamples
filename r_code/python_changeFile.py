
import json
import gzip
import pandas as pd


newFile = "reviews_Electronics.json.gz"


def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')


df = getDF(newFile)
# pd.DataFrame.to_csv(df)
df.to_csv("reviews_Electronics.csv")
# with  open("Music_Instrument.csv", "w") as outfile:
	
# electronicsHead = df.head(n=1000)
# electronicsHead.to_csv("reviews_Electronics_head.csv")




















