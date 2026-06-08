import pandas as pd
from pathlib import Path
from collections import defaultdict

INPUT_DIR=Path("data/bhav_data")
OUTPUT_DIR = INPUT_DIR / "weekly"

weekly_data = defaultdict(list)

for file in INPUT_DIR.glob("*.csv"):
    try:
        df = pd.read_csv(file,skipinitialspace=True)

        if df.empty or df.columns[0].startswith("<?xml"):
            continue

        df["DELIV_PER"] = pd.to_numeric(df["DELIV_PER"], errors="coerce")

        df["DATE1"] = pd.to_datetime(df["DATE1"],format="%d-%b-%Y")

        trade_date = df["DATE1"].iloc[0]
        week_start = trade_date - pd.Timedelta(days=trade_date.weekday())

        weekly_data[week_start].append(df)
    except Exception as e:
        print(f"Eror reading{file}: {e}")

for week_start,dfs in weekly_data.items():
    week_df = pd.concat(dfs,ignore_index=True)

    weekly_avg = (week_df.groupby(["SYMBOL","SERIES"],as_index=False).agg(AVG_DELIV_PER=("DELIV_PER","mean")))

    output_file = OUTPUT_DIR / f"{week_start.strftime('%d%m%Y')}.csv"
    weekly_avg.to_csv(output_file,index=False)

    print(f"Saved: {output_file}")