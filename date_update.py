import os
import time
import pandas as pd
import baostock as bs

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

def update_etf_data(code: str, start_date="2022-01-01") -> pd.DataFrame:
    csv_file = f"{code}.csv"
    bs.login()

    print(pd.DataFrame.size)
    # 判断是否已有本地文件，做增量更新
    if os.path.exists(csv_file):
        df_old = pd.read_csv(csv_file, encoding="utf-8-sig")
        last_date = df_old["date"].iloc[-1]
        start = last_date
    else:
        df_old = pd.DataFrame()
        start = start_date

    # 拉取增量数据
    rs = bs.query_history_k_data_plus(
        code=code,
        fields="date,open,high,low,close,volume",
        start_date=start,
        end_date=pd.Timestamp.now().strftime("%Y-%m-%d"),
        frequency="d"
    )
    new_data = []
    while rs.error_code == "0" and rs.next():
        new_data.append(rs.get_row_data())

    df_new = pd.DataFrame(new_data, columns=rs.fields)
    bs.logout()

    # 合并新旧数据，去重
    df_total = pd.concat([df_old, df_new], ignore_index=True)
    df_total = df_total.drop_duplicates(subset=["date"])
    df_total.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print(f"{code} 更新完成，共{len(df_total)}条K线")
    return df_total

if __name__ == "__main__":
    # 沪深300ETF
    update_etf_data("sh.510300")