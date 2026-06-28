# data_update.py
import os
import pandas as pd
import baostock as bs

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""

def update_etf_data(code: str, start_date="2018-01-01", full=False) -> pd.DataFrame:
    csv_file = f"{code}.csv"
    bs.login()

    # 开启全量模式：删除旧文件，重新从头下载所有历史
    if full and os.path.exists(csv_file):
        os.remove(csv_file)
        df_old = pd.DataFrame()
        start = start_date
    elif os.path.exists(csv_file):
        # 正常增量模式：只拉最新数据
        df_old = pd.read_csv(csv_file, encoding="utf-8-sig")
        last_date = df_old["date"].iloc[-1]
        start = last_date
    else:
        df_old = pd.DataFrame()
        start = start_date

    # 请求行情
    rs = bs.query_history_k_data_plus(
        code=code,
        fields="date,open,high,low,close,volume",
        start_date=start,
        end_date=pd.Timestamp.now().strftime("%Y-%m-%d"),
        frequency="d",
        adjustflag="2"  # 增加前复权，和你之前东财数据保持一致
    )
    new_data = []
    while rs.error_code == "0" and rs.next():
        new_data.append(rs.get_row_data())

    df_new = pd.DataFrame(new_data, columns=rs.fields)
    bs.logout()

    # 合并数据，去重
    df_total = pd.concat([df_old, df_new], ignore_index=True)
    df_total = df_total.drop_duplicates(subset=["date"])
    df_total.to_csv(csv_file, index=False, encoding="utf-8-sig")
    print(f"{code} 更新完成，总K线数量：{len(df_total)}")
    return df_total

if __name__ == "__main__":
    # ========== 两种运行模式 ==========
    # 1. 完整重新下载全部历史（仅第一次使用）
    update_etf_data("sh.510300", full=True)
# 
    # 2. 日常每日增量更新（平时就用这一行）
    # update_etf_data("sh.510300")