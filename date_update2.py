# data_update.py
import os
import pandas as pd
import akshare as ak

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

def update_etf_data(code="510300", start_date="20180101", full=False):
    csv_file = f"{code}.csv"

    # 全量模式：删除文件，重新下载全部历史
    if full:
        if os.path.exists(csv_file):
            os.remove(csv_file)
        df_old = pd.DataFrame()
        df_new = ak.fund_etf_hist_sina(symbol=code)
    elif os.path.exists(csv_file):
        # 日常增量：只补最新行情
        df_old = pd.read_csv(csv_file, encoding="utf-8-sig")
        df_full = ak.fund_etf_hist_sina(symbol=code)
        df_new = df_full[df_full["date"] > df_old["date"].iloc[-1]]
    else:
        df_old = pd.DataFrame()
        df_new = ak.fund_etf_hist_sina(symbol=code)

    df_total = pd.concat([df_old, df_new], ignore_index=True)
    df_total = df_total.drop_duplicates(subset=["date"]).sort_values("date")
    df_total.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print(f"✅ {code} 完成，总K线：{len(df_total)}")
    return df_total

if __name__ == "__main__":
    # 第一次运行打开full=True，下载全部历史数据
    # update_etf_data("510300", full=True)

    # 以后每日只运行这一行做增量更新
    update_etf_data("510300")