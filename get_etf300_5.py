import baostock as bs
import pandas as pd

# 登录（无需账号）
lg = bs.login()
rs = bs.query_history_k_data_plus(
    "sh.510300",
    fields="date,open,high,low,close,volume",
    start_date='2024-01-01',
    end_date='2026-06-24',
    frequency="d"
)
data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())
df = pd.DataFrame(data_list, columns=rs.fields)
df.to_csv("510300_5.csv", index=False, encoding="utf-8-sig")
bs.logout()
print(df.head())