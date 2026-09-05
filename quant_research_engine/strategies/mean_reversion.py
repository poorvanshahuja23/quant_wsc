import numpy as np
import pandas as pd

def mean_reversion_strategy(df: pd.DataFrame, window: int = 20, z_thresh: float = 2.0) -> pd.DataFrame:
    """
    df requires: ['Close']
    """
    data = df.copy()
    
    # 1. Feature Engineering: Rolling mean and rolling standard deviation
    data['mu'] = data['Close'].rolling(window=window).mean()
    data['sigma'] = data['Close'].rolling(window=window).std()
    
    # 2. Z-Score Calculation: Z = (Price - mu) / sigma
    data['z_score'] = (data['Close'] - data['mu']) / data['sigma']
    
    # 3. Signal Generation
    # Long when stretched below (-2 sigma), Short when stretched above (+2 sigma)
    data['signal'] = np.nan
    data.loc[data['z_score'] < -z_thresh, 'signal'] = 1   # Buy / Long
    data.loc[data['z_score'] > z_thresh, 'signal'] = -1   # Sell / Short
    
    # Revert to cash (exit) when price crosses back over the mean (z_score crosses 0)
    data.loc[(data['z_score'] >= 0) & (data['z_score'].shift(1) < 0), 'signal'] = 0
    data.loc[(data['z_score'] <= 0) & (data['z_score'].shift(1) > 0), 'signal'] = 0
    
    # Forward fill positions until exit condition is triggered
    data['position'] = data['signal'].ffill().fillna(0)
    
    # 4. Returns (Shift signal by 1 to prevent lookahead bias)
    data['market_returns'] = data['Close'].pct_change()
    data['strategy_returns'] = data['position'].shift(1) * data['market_returns']
    
    return data


# Public entry point used by main.py and strategies.__init__.
run_mean_reversion = mean_reversion_strategy
