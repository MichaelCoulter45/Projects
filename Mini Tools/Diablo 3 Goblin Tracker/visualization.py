# visualization.py
# Reads CSV and makes the charts to visualize the data
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import tracker


def load_data() -> pd.DataFrame:
    """ Reads the goblin CSV into a DataFrame with 'timestamp' and 'goblin' columns."""
    if not tracker.DS.exists():
        return pd.DataFrame(columns=['timestamp', 'goblin'])
    
    try:
        return pd.read_csv(
            tracker.DS,
            header=None,
            names=["timestamp", "goblin"],
            parse_dates=["timestamp"],
        )
    except pd.errors.EmptyDataError:
        # The file exists but has no rows.
        return pd.DataFrame(columns=["timestamp", "goblin"])


def goblins_per_day(df: pd.DataFrame) -> pd.DataFrame:
    """ Returns a table: one row per day, one column per goblin type, values are counts."""
    df = df.copy()
    df["date"] = df["timestamp"].dt.normalize() # <- Strips the time by setting each timestamp to Midnight
    counts = df.groupby(["date", "goblin"]).size().unstack(fill_value=0)
    return counts.asfreq("D", fill_value=0) # <- Adds days with no goblins as zeros


def plot_goblins_per_day() -> None:
    """ Shows a line graph of goblins found per day, one line per goblin type."""
    df = load_data()
    if df.empty:
        print("No goblin data to plot.")
        return
    
    counts = goblins_per_day(df)
    
    ax = counts.plot(marker="o", figsize=(10,6))
    ax.set_title("Goblins Found Per Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Goblins Found")
    # ax.yaxis.set_major_locator(MaxNLocator(interger=True))
    ax.legend(title="Goblin Type")
    plt.tight_layout()
    plt.show()

# if __name__ == "__main__":
#     plot_goblins_per_day()