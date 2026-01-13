# JOURNAL / DEVLOG
This section documents my ongoing thoughts, theoretical pivots, and the conceptrual roadmap as I develop the app. 
It reflects my journey of converting lecture theories into functional quantitative tools. 
Starts from **Jan 12, 2026**, I move away all the old logs and thoughts from original header for tidiness. New thoughs and logs would update under this file.

#### Jan 12, 2026
* Staring at the MC simulations running smoothly through every sample, I suddenly come up with that this simulation is set up with condition of volatility $\sigma$ is constant. But in real financial world, "clustering effects" often exists. So, in my next step, I would try to figure out the **$GARCH(1,1)$** for better forecast.
* The most troublesome question for ordinary retail investors is: "I have 5,000 dollars, and I want to play it safe. Which ETFs should I buy, and how much should I buy?", which annoyed myself quite a lot for a long time while I started investing. Individuals are noisy, ETFs are statistically "Cleaner". I am thinking of Transitioning from a single-asset forecaster to an **ETF Portfolio Advisor**: Given a fixed budget, the tool should suggest an optimized mix of Equity, Bond, and Commodity ETFs.
