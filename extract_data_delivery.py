import requests
import pandas as pd
from datetime import datetime,timedelta

start_date = datetime(2020,6,15)
end_date = datetime(2026,5,26)

current = start_date

failed_date =[]

while current<=end_date:
    date_str=current.strftime("%d%m%Y")

    url=f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{date_str}.csv"

    try:
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=2
        )

        if r.status_code==200 and len(r.content) > 100:
            with open(f"data/bhav_data/{date_str}.csv","wb") as f:
                f.write(r.content)
            print("Downloaded: " , date_str)

        else:
            failed_date.append(date_str)
            print("Missing: ",date_str)
    except Exception as e:
        failed_date.append(date_str)
        print("Error: ",date_str,e)

    current+=timedelta(days=1)
