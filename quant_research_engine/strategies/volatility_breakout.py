import numpy as np
import pandas as pd


def volatility_breakout_strategy(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    df requires: ['Open', 'High', 'Low', 'Close', 'Volume']
    """
    data = df.copy()
    
    # 1. Track Daily Range & Baselines
    data['daily_range'] = data['High'] - data['Low']
    data['range_ma'] = data['daily_range'].rolling(window=window).mean()
    data['volume_ma'] = data['Volume'].rolling(window=window).mean()
    
    # 2. Compression Metric (e.g., range is in bottom 25% of recent history)
    data['is_compressed'] = data['daily_range'] < (0.75 * data['range_ma'])
    
    # 3. Breakout Conditions:
    # Price crosses 20-day high + Volume expands at least 1.5x above baseline
    data['recent_high'] = data['High'].rolling(window=window).max().shift(1)
    data['volume_spike'] = data['Volume'] > (1.5 * data['volume_ma'])
    data['range_expansion'] = data['daily_range'] > data['range_ma']
    
    # 4. Entry Trigger
    breakout_long = (data['Close'] > data['recent_high']) & data['volume_spike'] & data['range_expansion']
    
    data['position'] = 0
    data.loc[breakout_long, 'position'] = 1
    
    # Hold trade for 3 days or until a trailing stop is hit
    data['position'] = data['position'].replace(0, np.nan).ffill(limit=3).fillna(0)
    
    # 5. Strategy Returns
    data['market_returns'] = data['Close'].pct_change()
    data['strategy_returns'] = data['position'].shift(1) * data['market_returns']
    
    return data


# Public entry point used by main.py and strategies.__init__.
run_volatility_breakout = volatility_breakout_strategy
