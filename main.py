import numpy as np
import pandas as pd
import datetime

raw_data = pd.read_csv(r'C:\Users\amind\Google Drive\Files\Productivity_Tracker Data\BrowserHistory.csv')
chrome_data = raw_data['Browser History'].str.split(' url:', expand=True)
chrome_data = chrome_data[1].str.split('time_usec:', expand=True)
chrome_data.rename(columns={0:'url', 1:'time_usec'}, inplace=True)

epoch_list = (chrome_data['time_usec'].astype(float)/1000000).values.tolist()
date_list = []
for i in range(len(epoch_list)):
    temp = epoch_list[i]
    date = datetime.datetime.fromtimestamp(temp)
    date_list.append(date)

chrome_data['time_usec'] = date_list