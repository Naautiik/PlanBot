from PlanBot import scheduled
from datetime import datetime
from pandasql import sqldf
import pandas as pd
from time import sleep
subskrypcje = pd.read_csv("subskrypcje.csv")



while True:
    print("Waiting for the right time")
    sleep(60)
    if (datetime.now().strftime('%H')) == '18':
        print("sending")
        load = sqldf("SELECT * FROM subskrypcje")
        load = load.values.tolist()
        for x in load:
            scheduled(x[0], x[1])
        sleep(3600)