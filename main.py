import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import csv


def main(start, end):
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
    start_date = datetime.strptime(str(start), '%Y-%m-%d')
    end_date = datetime.strptime(str(end), '%Y-%m-%d')
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

    # Organize keywords for each dataframe
    misc_browser_keys = ['stat', 'panda', 'ipynb', 'science', 'udemy', 'algorithm', 'regression', 'data', 'machine', 'learning', 'stackoverflow', 'geeks', 'w3school', 'github', 'seaborn', 'matplotlib', 'kaggle', 'dev', 'kite', 'thesaurus', 'w3resource', 'finance', 'invest', 'coin', 'correlation', 'fourier', 'excel']
    browser_keys = ['linkedin','mail','youtube','search','instagram','cibc','bmo','royalbank','netflix','twitch']
    activity_keys = ['python','Chrome','Microsoft Word','Microsoft Excel','PyCharm','Adobe Acrobat Reader']

    # Search through datasets for keywords
    browser_df = pd.DataFrame(columns=browser_keys)
    misc_df = pd.DataFrame(columns=misc_browser_keys)
    activity_df = pd.DataFrame(columns=activity_keys)

    for i in range(len(browser_keys)):
        keyword = str(browser_keys[i])
        findings = []
        for i in browser['url']:
            url = str(i)

            if url.find(keyword) != -1:
                findings.append(1)
            else:
                findings.append(0)

        browser_df[keyword] = findings
    for i in range(len(misc_browser_keys)):
        keyword = str(misc_browser_keys[i])
        findings = []
        for i in browser['url']:
            url = str(i)

            if url.find(keyword) != -1:
                findings.append(1)
            else:
                findings.append(0)

        misc_df[keyword] = findings
    for i in range(len(activity_keys)):
        keyword = str(activity_keys[i])
        findings = []
        for i in activity['AppName']:
            app = str(i)

            if app.find(keyword) != -1:
                findings.append(1)
            else:
                findings.append(0)

        activity_df[keyword] = findings

    # Sum results of keywords search
    self_improv = sum(misc_df.sum())
    browsing = browser_df.sum()
    browsing['Self Improvement'] = self_improv
    apps = activity_df.sum()
    browsing['finance'] = browsing['cibc'] + browsing['bmo'] + browsing['royalbank']
    browsing['streaming'] = browsing['netflix'] + browsing['twitch']
    browsing.drop(labels=['cibc', 'bmo', 'royalbank', 'netflix', 'twitch'], axis=0,inplace=True)

    # Generate plots
    fig = plt.figure(figsize=[30,20])
    plt.pie(np.squeeze(np.array(browsing)), labels=browsing.index, counterclock=False)
    plt.title('Weekly Browsing Breakdown')
    plt.show()
    fig = plt.figure(figsize=[30,20])
    plt.pie(np.squeeze(np.array(apps)), labels=apps.index, counterclock=False)
    plt.title('Weekly Laptop Activity Breakdown')
    plt.show()

    # Calculate and print Weekly Self Improvement Score
    score = browsing['Self Improvement']/(browsing.sum() - browsing['youtube'] - browsing['linkedin'] - browsing['search'])
    score = '{0:.1g}'.format(score)
    print('Weekly Self Improvement Score:',score)

    # Add Weekly Self Improvement Score to historical dataset
    with open(r'C:\Users\amind\Google Drive\Files\Productivity_Tracker Data\Self Improvement Scores.csv', mode='a') as score_log:
        score_log_writer = csv.writer(score_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        score_log_writer.writerow([start_date, end_date, score])
    score_log.close()

    # Generate bar chart to view past Weekly Self Improvement Scores
    score_log = pd.read_csv(r'C:\Users\amind\Google Drive\Files\Productivity_Tracker Data\Self Improvement Scores.csv')
    x_coor = str(score_log['End Date'].values.tolist())
    height = score_log['Score']
    plt.bar(x_coor, height)
    plt.title('Weekly Self Improvement Score Log')
    return
