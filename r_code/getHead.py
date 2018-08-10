
import json
import gzip
import pandas as pd


homeKitchenBig = pd.read_csv("reviews_Home_and_Kitchen.csv")
homeKitchenSmall = homeKitchenBig.head(n=1000)
homeKitchenSmall.to_csv("HK_small.csv")