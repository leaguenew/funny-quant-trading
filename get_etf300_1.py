

import akshare as ak
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 1. 构建带重试、浏览器头的session
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
new_session = requests.Session()
new_session.mount("https://", adapter)
new_session.mount("http://", adapter)
new_session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://quote.eastmoney.com/"
})

# 2. 覆盖akshare底层用的requests全局session
requests.Session = lambda: new_session

# 3. 延时防爬
time.sleep(1)

# 不再传session、timeout参数，原版调用
df = ak.fund_etf_hist_em(
    symbol="510300",
    period="daily",
    adjust="qfq"
)

print(df.head())
df.to_csv("510300.csv", index=False, encoding="utf-8-sig")
print("数据保存完成")
