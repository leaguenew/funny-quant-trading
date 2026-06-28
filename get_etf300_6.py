import os
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

import akshare as ak

# 必须填写 sh+代码！！沪市ETF sh开头
df = ak.fund_etf_hist_sina(symbol="sh510300")
# df = ak.stock_etf_hist_sina(symbol="sh510300", start_date="20240101", end_date="20260601")


# 先打印查看有没有数据
print(f"数据行数：{len(df)}")
print(df.columns)

if len(df) > 0:
    df.rename(columns={
        "日期":"date",
        "开盘价":"open",
        "最高价":"high",
        "最低价":"low",
        "收盘价":"close",
        "成交量":"volume"
    }, inplace=True)
    df.to_csv("510300_etf_kline.csv", index=False, encoding="utf-8-sig")
    print("保存成功")
else:
    print("接口无返回数据，新浪接口已失效")