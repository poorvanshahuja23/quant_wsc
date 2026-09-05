import pandas as pd
import os

def generate_and_store_datasets():
    # Ensure a data directory exists
    os.makedirs("data", exist_ok=True)
    days = list(range(1, 21))

    # Dataset A: Alpha Corp (Mean Reversion)
    df_a = pd.DataFrame({
        'Day': days,
        'Close': [100.1, 100.9, 99.2, 100.5, 99.6, 99.8, 100.4, 104.8, 100.1, 99.9,
                  100.2, 99.5, 100.8, 100.0, 105.2, 99.9, 95.1, 100.3, 100.8, 100.1]
    }).set_index('Day')

    # Dataset B: Beta Dynamics (Trend Following)
    df_b = pd.DataFrame({
        'Day': days,
        'Close': [50.0, 51.5, 52.0, 51.0, 53.5, 54.2, 56.8, 58.5, 57.9, 59.2,
                  60.0, 62.5, 61.5, 64.0, 66.5, 65.0, 68.0, 71.0, 70.5, 74.0]
    }).set_index('Day')

    # Dataset C: Gamma Tech (Volatility Breakout)
    # Note: K and M string suffixes are converted to actual integers for mathematical modeling
    df_c = pd.DataFrame({
        'Day': days,
        'High': [20.80, 20.60, 20.50, 20.40, 20.35, 20.30, 20.25, 20.20, 20.20, 20.15,
                 20.15, 20.12, 20.08, 20.05, 20.02, 24.50, 26.80, 29.00, 31.50, 34.00],
        'Low':  [19.20, 19.50, 19.60, 19.70, 19.75, 19.80, 19.80, 19.85, 19.85, 19.85,
                 19.85, 19.90, 19.92, 19.95, 19.98, 20.00, 23.90, 25.50, 28.00, 30.50],
        'Close':[20.10, 19.90, 20.20, 19.80, 20.10, 19.90, 20.05, 20.00, 19.95, 20.05,
                 20.00, 20.05, 20.00, 20.02, 20.00, 24.20, 26.50, 28.80, 31.20, 33.50],
        'Volume':[120000, 110000, 95000, 85000, 80000, 75000, 68000, 60000, 55000, 50000,
                  45000, 38000, 25000, 15000, 9000, 2500000, 3100000, 2800000, 3500000, 4000000]
    }).set_index('Day')

    # Dataset D: Delta & Echo (Pairs Trading)
    df_d = pd.DataFrame({
        'Day': days,
        'Delta': [60.0, 61.5, 59.0, 62.0, 58.5, 60.5, 63.0, 64.5, 61.0, 62.5,
                  63.0, 61.5, 65.0, 67.5, 68.0, 64.0, 62.0, 60.5, 59.0, 61.5],
        'Echo':  [50.0, 51.5, 49.0, 52.0, 48.5, 50.5, 53.0, 54.5, 51.0, 52.5,
                  53.0, 51.5, 48.0, 45.5, 44.0, 48.0, 50.0, 50.5, 49.0, 51.5]
    }).set_index('Day')

    # Dataset E: Omega Resources (The Random Walk / No Edge)
    df_e = pd.DataFrame({
        'Day': days,
        'Close': [45.20, 62.10, 38.40, 55.90, 41.20, 70.50, 49.80, 35.40, 68.10, 52.70,
                  32.10, 71.80, 44.50, 59.10, 38.50, 82.20, 41.00, 65.20, 51.50, 36.80]
    }).set_index('Day')

    # Export to Parquet
    df_a.to_parquet("data/alpha_corp.parquet")
    df_b.to_parquet("data/beta_dynamics.parquet")
    df_c.to_parquet("data/gamma_tech.parquet")
    df_d.to_parquet("data/delta_echo.parquet")
    df_e.to_parquet("data/omega_resources.parquet")

    print("Successfully exported all 5 datasets to Parquet format in the /data directory.")

if __name__ == "__main__":
    generate_and_store_datasets()
