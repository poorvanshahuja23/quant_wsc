def pairs_trading_strategy(price_a: pd.Series, price_b: pd.Series, window: int = 20) -> pd.DataFrame:
    data = pd.DataFrame({'Price_A': price_a, 'Price_B': price_b})
    
    # 1. Rolling Ordinary Least Squares (OLS) to derive dynamic Beta (Hedge Ratio)
    covariance = data['Price_A'].rolling(window).cov(data['Price_B'])
    variance = data['Price_B'].rolling(window).var()
    data['beta'] = covariance / variance
    
    # 2. Synthetic Stationary Spread
    data['spread'] = data['Price_A'] - (data['beta'] * data['Price_B'])
    
    # 3. Spread Z-score
    data['spread_mu'] = data['spread'].rolling(window).mean()
    data['spread_sigma'] = data['spread'].rolling(window).std()
    data['z_spread'] = (data['spread'] - data['spread_mu']) / data['spread_sigma']
    
    # 4. Market-Neutral Signals:
    # If spread is deeply negative (< -2): Long A, Short B
    # If spread is deeply positive (> +2): Short A, Long B
    data['pos_A'] = np.where(data['z_spread'] < -2.0, 1, np.where(data['z_spread'] > 2.0, -1, 0))
    data['pos_B'] = -data['pos_A'] * data['beta']
    
    # 5. PnL Attribution
    ret_A = data['Price_A'].pct_change()
    ret_B = data['Price_B'].pct_change()
    data['strategy_returns'] = (data['pos_A'].shift(1) * ret_A) + (data['pos_B'].shift(1) * ret_B)
    
    return data
