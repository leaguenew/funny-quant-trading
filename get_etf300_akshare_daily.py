import os
import pandas as pd
import akshare as ak

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

def update_etf(code="sh510300", full_download=False):
    csv_name = "510300_etf_kline_daily.csv"
    # 拉取场内二级市场交易K线
    df_raw = ak.fund_etf_hist_sina(symbol=code)
    # 统一英文列名，兼容回测脚本
    df_raw.rename(columns={
        "日期": "date",
        "开盘价": "open",
        "最高价": "high",
        "最低价": "low",
        "收盘价": "close",
        "成交量": "volume"
    }, inplace=True)

    if full_download:
        df_final = df_raw
    else:
        # 增量更新，只补充新交易日
        if os.path.exists(csv_name):
            df_old = pd.read_csv(csv_name, encoding="utf-8-sig")
            df_old["date"] = pd.to_datetime(df_old["date"]).dt.date

            last_trade_day = df_old["date"].iloc[-1]
            df_new = df_raw[df_raw["date"] > last_trade_day]
            df_final = pd.concat([df_old, df_new], ignore_index=True)
            df_final = df_final.drop_duplicates(subset="date")
        else:
            df_final = df_raw

    df_final.sort_values("date", inplace=True)
    df_final.to_csv(csv_name, index=False, encoding="utf-8-sig")
    print(f"更新完成，总K线条数：{len(df_final)}")
    return df_final

if __name__ == "__main__":
    # 首次全量下载：update_etf(full_download=True)
    # 日常每日增量更新
    update_etf()