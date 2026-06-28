

import os
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["ALL_PROXY"] = ""

import efinance as ef

# 场内ETF统一走 stock.get_quote_history
#df = ef.stock.get_quote_history("510300")
df = ef.stock.get_quote_history("510300", beg="20240101", end="20260601")


print(df.head())
# utf-8-sig 防止Excel打开乱码
df.to_csv("510300_4.csv", index=False, encoding="utf-8-sig")
print("数据保存完成")
