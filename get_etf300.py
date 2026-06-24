import akshare as ak
import pandas as pd

df = ak.fund_etf_hist_em(
    symbol="510300",
    period="daily",
    adjust="qfq"
)

print(df.head())

df.to_csv("510300.csv", index=False)
