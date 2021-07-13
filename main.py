import pandas as pd
from datetime import datetime

# Load browser history data then reformat
browser_raw = pd.read_csv(r'C:\Users\amind\Google Drive\Files\Productivity_Tracker Data\BrowserHistory.csv')
browser = browser_raw['Browser History'].str.split(' url:', expand=True)
browser = browser[1].str.split('time_usec:', expand=True)
browser.rename(columns={0:'url', 1:'time_usec'}, inplace=True)
temporary = browser['time_usec'].str.split('}', expand=True)
browser['time_usec'] = temporary[0]

# Load laptop activity data then reformat
activity_raw = pd.read_csv(r'C:\Users\amind\Google Drive\Files\Productivity_Tracker Data\ProductAndServiceUsage.csv')
activity = activity_raw.drop(labels=['EndDateTime', 'DeviceId', 'Aggregation', 'AppPublisher'], axis=1)
activity['DateTime'] = activity['DateTime'].str.split(' ', expand=True)
activity_date_list = activity['DateTime'].values.tolist()
date_list = []
for i in range(len(activity_date_list)):
    date = datetime.strptime(activity_date_list[i], '%m/%d/%Y')
    date_list.append(date)
activity['Date'] = date_list
activity = activity.drop(columns='DateTime')

# Set time range for period of interest
start_date = datetime.strptime('2021-07-1', '%Y-%m-%d')
end_date = datetime.strptime('2021-07-08', '%Y-%m-%d')
start_epoch = (start_date.timestamp() * 1000000)
end_epoch = (end_date.timestamp() * 1000000)

# Remove data outside the period of interest
browser = browser.loc[(browser['time_usec'].astype(float) <= end_epoch) & (browser['time_usec'].astype(float) >= start_epoch)]
browser.reset_index(drop=True, inplace=True)
activity = activity.loc[(activity['Date'] <= end_date) & (activity['Date'] >= start_date)]

# Convert epoch to human-readable date for browser data
epoch_list = (browser['time_usec'].astype(float)/1000000).values.tolist()
date_list = []
for i in range(len(epoch_list)):
    temp = epoch_list[i]
    date = datetime.fromtimestamp(temp)
    date_list.append(date)
browser['time_usec'] = date_list
browser['Date'] = [d.date() for d in browser['time_usec']]
browser = browser.drop(columns='time_usec')

# Add column with day to both dataframes
browser['Month'] = pd.to_datetime(browser['Date']).dt.day
activity['Month'] = pd.to_datetime(activity['Date']).dt.day

# Organize keywords for each dataframe
browser_keywords = {1:'linkedin', 2:'mail', 3:'youtube', 4:'search', 5:'instagram', 6:'cibc', 7:'bmo', 8:'royalbank', 9:'netflix', 10:'twitch'}
misc_browser_keywords = ['stat', 'panda', 'ipynb', 'science', 'udemy', 'algorithm', 'regression', 'data', 'machine', 'learning', 'stackoverflow', 'geeks', 'w3school', 'github', 'seaborn', 'matplotlib', 'kaggle', 'dev', 'kite', 'thesaurus', 'w3resource', 'finance', 'invest', 'coin', 'correlation', 'fourier']
activity_keywords = {1:'python', 2:'Chrome', 3:'Microsoft Word', 4:'Microsoft Excel', 5:'PyCharm', 6:'Adobe Acrobat Reader'}