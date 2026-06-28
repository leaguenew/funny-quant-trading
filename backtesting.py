import pandas as pd
import vectorbt as vbt

# 1.读取清洗好的场内ETF日线数据
print("=============== read data start ===============")
df = pd.read_csv("510300_etf_kline_daily_2025_2026.csv", encoding="utf-8-sig")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
print("=============== read data end ===============")


# 提取收盘价做均线计算
price = df["close"].astype(float)
print("=============== 提取收盘价做均线计算 end ===============")

# 2.设置策略参数：20日均线、60日均线
fast_ma_period = 20
slow_ma_period = 60

# 计算两条均线
fast_ma = vbt.MA.run(price, window=fast_ma_period)
slow_ma = vbt.MA.run(price, window=slow_ma_period)

# 3.生成买卖信号
entries = fast_ma.ma_crossed_above(slow_ma)   # 金叉买入
exits = fast_ma.ma_crossed_below(slow_ma)     # 死叉卖出

print("=============== start to back testing ===============")

# 4.模拟实盘交易：手续费万1，每日频率回测
portfolio = vbt.Portfolio.from_signals(
    price,
    entries,
    exits,
    fees=0.0001,   # 佣金万一，模拟真实交易成本
    freq="1d"
)

# 5.打印全套回测绩效指标（重点看这几个）
print("=============== 回测绩效报表 ===============")
stats = portfolio.stats()
print(stats)

# 关键指标释义（你重点关注）
# Annual Return: 年化收益率（目标10%-20%）
# Max Drawdown: 最大回撤（控制在15%以内最优）
# Sharpe Ratio: 夏普比率，>1.5代表风险收益比优秀

# 6.绘制可视化图表：价格曲线、买卖点、账户净值曲线
# fig = portfolio.plot(subplots=["signals", "cum_returns", "drawdowns"])
# fig.show()
stats = portfolio.stats()
print(stats)



# # 额外单独画出价格+双均线，方便对照买卖点
import matplotlib.pyplot as plt
plt.figure(figsize=(14,6))
plt.plot(price, label="收盘价", lw=1)
plt.plot(fast_ma.ma, label=f"MA{fast_ma_period}", lw=1.2)
plt.plot(slow_ma.ma, label=f"MA{slow_ma_period}", lw=1.2)
plt.title("510300 价格与均线")
plt.legend()
plt.show()