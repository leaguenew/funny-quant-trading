

import efinance as ef

# 获取ETF历史行情
df = ef.fund.get_quote_history("510300")
print(df.head())
df.to_csv("510300_2.csv", index=False, encoding="utf-8-sig")
