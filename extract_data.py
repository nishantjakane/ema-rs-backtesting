from tvDatafeed import TvDatafeed, Interval
import pandas as pd

tv = TvDatafeed()

df = pd.read_csv("failed.csv")
failed =[]
for symbol in df.symbols:
    try:
        data = tv.get_hist(symbol=f'{symbol}',exchange='NSE',interval=Interval.in_weekly,n_bars=312)
        if data is not None and not data.empty:
            data.to_csv(f"data/{symbol}.csv")
            print(f"Saved : {symbol}")
        else:
            failed.append(symbol)
            print(f"Error for {symbol}")
    except Exception as e:
        print(f"Error {e}")

failed_df = pd.DataFrame(failed,columns=['symbols'])
failed_df.to_csv("failed.csv")