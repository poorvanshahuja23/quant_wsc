import numpy as np
import pandas as pd


def trend_following_strategy(df: pd.DataFrame, fast_window: int = 3, slow_window: int = 7) -> pd.DataFrame:
    """
    df requires: ['Close']
    """
    data = df.copy()
    
    # 1. Moving Averages
    data['sma_fast'] = data['Close'].rolling(window=fast_window).mean()
    data['sma_slow'] = data['Close'].rolling(window=slow_window).mean()
    
    # 2. Binary Trend Signal: Fast > Slow confirms positive autocorrelation
    data['position'] = np.where(data['sma_fast'] > data['sma_slow'], 1, -1)
    
    # 3. Vectorized PnL Execution
    data['market_returns'] = data['Close'].pct_change()
    data['strategy_returns'] = data['position'].shift(1) * data['market_returns']
    
    return data


# Public entry point used by main.py and strategies.__init__.
run_trend_following = trend_following_strategy
