import yfinance as yf
df = yf.download("510300.SS", start="2026-06-01", end="2026-06-11")
print(df)