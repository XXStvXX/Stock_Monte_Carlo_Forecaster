import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm
from datetime import datetime, timedelta

# --- 1. 网页配置 ---
st.set_page_config(page_title="Quant Analysis Lab", layout="wide")

# 标题与署名
st.title("Quantitative Finance & Market Prediction Lab")
st.markdown("""
<style>
.small-font {
    font-size:14px !important;
    color: #808080;
}
</style>
<p class="small-font">Developed by <a href="https://github.com/XXStvXX" target="_blank">XXStvXX</a></p>
""", unsafe_allow_html=True)
st.markdown("---")

# --- 2. 侧边栏：参数设置 ---
st.sidebar.header("Data Settings")
ticker = st.sidebar.text_input("Stock Ticker:", "VFV.TO")

# 时间跨度选择
time_options = {
    "1 Month": 30,
    "3 Months": 90,
    "6 Months": 180,
    "1 Year": 365,
    "3 Years": 365*3,
    "5 Years": 365*5,
    "Max (15Y)": 365*15
}
selected_period = st.sidebar.selectbox("Historical Time Scale:", list(time_options.keys()), index=3)

st.sidebar.markdown("---")
st.sidebar.header("Model Parameters")
sim_days = st.sidebar.slider("Forecast Horizon (Days):", 30, 365, 252)
num_sims = st.sidebar.slider("Number of Simulations:", 100, 1000, 500)

st.sidebar.subheader("Macro Scenario Analysis")
macro_drift = st.sidebar.slider("Annual Macro Bias:", -0.2, 0.2, 0.0)

# --- 3. 数据获取与处理 ---
start_date = (datetime.now() - timedelta(days=time_options[selected_period])).strftime('%Y-%m-%d')

if ticker:
    with st.spinner(f'Analyzing {selected_period} of {ticker} data...'):
        # 获取历史数据
        data = yf.download(ticker, start=start_date)
        
        # 兼容 yfinance 多级索引
        if isinstance(data.columns, pd.MultiIndex):
            prices = data['Close'][ticker]
        else:
            prices = data['Close']
            
        returns = prices.pct_change().dropna()
        mu = returns.mean()
        sigma = returns.std()
        last_price = float(prices.iloc[-1].item())

    # --- 4. 历史收益率分布 (交互式磁吸版) ---
    st.subheader(f"Historical Returns Analysis ({selected_period})")
    
    # 准备统计曲线
    x_range = np.linspace(returns.min(), returns.max(), 100)
    y_norm = norm.pdf(x_range, mu, sigma)

    fig_hist = go.Figure()

    # 蓝色柱状图 (块状)
    fig_hist.add_trace(go.Histogram(
        x=returns,
        nbinsx=100,
        name='Actual Returns',
        marker_color='#2E86C1',
        opacity=0.7,
        histnorm='probability density'
    ))

    # 红色拟合曲线
    fig_hist.add_trace(go.Scatter(
        x=x_range, y=y_norm,
        mode='lines',
        name='Normal Dist',
        line=dict(color='#E74C3C', width=2.5)
    ))

    # 配置磁吸感交互
    fig_hist.update_layout(
        template="simple_white",
        hovermode="x unified",
        xaxis=dict(
            title="Daily Return (%)",
            tickformat=".2%",
            showspikes=True,
            spikemode="across",
            spikesnap="data",
            spikethickness=1,
            spikecolor="#999999",
            spikedash="dash"
        ),
        yaxis=dict(title="Probability Density", showgrid=True, gridcolor='rgba(200, 200, 200, 0.3)'),
        showlegend=False,
        height=450,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # --- 5. 蒙特卡洛预测 (全宽显示 + 置信区间) ---
    st.subheader(f"Monte Carlo Projection ({num_sims} paths)")
    
    import matplotlib.pyplot as plt
    
    # 算法核心
    sim_results = np.zeros((sim_days, num_sims))
    daily_macro_adj = (mu + (macro_drift / 252))
    
    for i in range(num_sims):
        random_returns = np.random.normal(daily_macro_adj, sigma, sim_days)
        price_path = last_price * (1 + random_returns).cumprod()
        sim_results[:, i] = price_path
    
    # 计算分位数
    mean_path = sim_results.mean(axis=1)
    lower_bound = np.percentile(sim_results, 5, axis=1)
    upper_bound = np.percentile(sim_results, 95, axis=1)

    # 绘图
    fig_sim, ax_sim = plt.subplots(figsize=(12, 6))
    ax_sim.plot(sim_results, color='#2E86C1', alpha=0.015) 
    ax_sim.plot(mean_path, color='#C0392B', linewidth=2.5, label="Expected Mean")
    ax_sim.plot(lower_bound, color='#212F3D', linestyle='--', linewidth=1, label="5th Percentile")
    ax_sim.plot(upper_bound, color='#212F3D', linestyle='--', linewidth=1, label="95th Percentile")
    
    days_array = np.arange(sim_days)
    ax_sim.fill_between(days_array, lower_bound, upper_bound, color='gray', alpha=0.25, label="90% CI")

    ax_sim.set_xlabel("Trading Days into Future")
    ax_sim.set_ylabel("Price (Currency)")
    ax_sim.set_title(f"Simulation of Future Price Action: {ticker}", fontweight='bold')
    ax_sim.grid(True, linestyle='--', alpha=0.5)
    ax_sim.legend(loc='upper left', fontsize='small')
    
    st.pyplot(fig_sim)

    # --- 6. 底部量化指标卡片 ---
    st.divider()
    expected_val = float(mean_path[-1])
    var_95 = float(np.percentile(sim_results[-1, :], 5))
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Current Price", f"${last_price:.2f}")
    c2.metric("Projected Mean", f"${expected_val:.2f}", f"{((expected_val/last_price)-1):.2%}")
    c3.metric("95% Value-at-Risk", f"${var_95:.2f}", "Downside Limit", delta_color="inverse")

    st.markdown("<p style='font-size:12px; color:gray; text-align:center;'>Model: Geometric Brownian Motion (GBM) with Monte Carlo Method. Parameters derived from historical volatility.</p>", unsafe_allow_html=True)
