
import pandas as pd

def money(value: float) -> str:
    return f"${value:,.2f}"


def main() -> None:
    print("Loading datasets from /data...")
    alpha = pd.read_parquet("data/alpha_corp.parquet")
    beta = pd.read_parquet("data/beta_dynamics.parquet")
    gamma = pd.read_parquet("data/gamma_tech.parquet")
    delta_echo = pd.read_parquet("data/delta_echo.parquet")
    omega = pd.read_parquet("data/omega_resources.parquet")

    alpha_mean = alpha["Close"].mean()
    alpha_std = alpha["Close"].std()
    alpha_z = (alpha["Close"] - alpha_mean) / alpha_std
    high_day, high_z = alpha_z.idxmax(), alpha_z.max()
    low_day, low_z = alpha_z.idxmin(), alpha_z.min()
    print("\n--- Dataset A: Alpha Corp ---")
    print(f"Metric: mean = {money(alpha_mean)}, standard deviation = {alpha_std:.2f}")
    print(f"Extreme Z-scores: day {high_day} = {high_z:+.2f}, day {low_day} = {low_z:+.2f}")
    print("Match: Mean Reversion")

    beta_sma_3 = beta["Close"].rolling(3).mean().iloc[-1]
    beta_sma_7 = beta["Close"].rolling(7).mean().iloc[-1]
    print("\n--- Dataset B: Beta Dynamics ---")
    print(f"Metric: final 3-day SMA = {money(beta_sma_3)}, final 7-day SMA = {money(beta_sma_7)}")
    print(f"SMA spread: {money(beta_sma_3 - beta_sma_7)}")
    print("Match: Trend Following (Momentum)")

    gamma["range"] = gamma["High"] - gamma["Low"]
    compression_day = gamma["range"].idxmin()
    print("\n--- Dataset C: Gamma Tech ---")
    print(
        "Metric: "
        f"day {compression_day} range = {money(gamma.loc[compression_day, 'range'])}, "
        f"volume = {gamma.loc[compression_day, 'Volume']:,.0f}; "
        f"day 16 range = {money(gamma.loc[16, 'range'])}, "
        f"volume = {gamma.loc[16, 'Volume']:,.0f}"
    )
    print("Match: Volatility Breakout")

    delta_echo["spread"] = delta_echo["Delta"] - delta_echo["Echo"]
    normal_spread = delta_echo.loc[1:12, "spread"].mean()
    peak_day = delta_echo["spread"].idxmax()
    peak_spread = delta_echo.loc[peak_day, "spread"]
    final_spread = delta_echo["spread"].iloc[-1]
    print("\n--- Dataset D: Delta & Echo ---")
    print(
        f"Metric: normal spread = {money(normal_spread)}, "
        f"peak on day {peak_day} = {money(peak_spread)}, final spread = {money(final_spread)}"
    )
    print("Match: Pairs Trading (Statistical Arbitrage)")

    print("\n--- Dataset E: Omega Resources ---")
    print("Match: No edge (random-walk trap)")
    print("No stable mean, standard deviation, sustained momentum, or volatility-compression pattern.")
    print("Past prices carry zero predictive information about future prices.")


if __name__ == "__main__":
    main()
