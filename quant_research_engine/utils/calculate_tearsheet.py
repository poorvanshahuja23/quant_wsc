import numpy as np
import pandas as pd


def calculate_metrics(strategy_returns: pd.Series, periods_per_year: int = 252) -> dict:
    clean_returns = strategy_returns.dropna()
    
    # Sharpe Ratio (assuming 0% risk-free rate for simplicity)
    mean_ret = clean_returns.mean() * periods_per_year
    std_dev = clean_returns.std() * np.sqrt(periods_per_year)
    sharpe = mean_ret / std_dev if std_dev != 0 else 0
    
    # Maximum Drawdown (peak-to-trough drop)
    cumulative = (1 + clean_returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    
    return {
        "Annualized Return": f"{mean_ret * 100:.2f}%",
        "Annualized Volatility": f"{std_dev * 100:.2f}%",
        "Sharpe Ratio": round(sharpe, 2),
        "Max Drawdown": f"{max_drawdown * 100:.2f}%"
    }
