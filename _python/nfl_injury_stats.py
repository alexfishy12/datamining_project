#!/usr/bin/python3
print("Content-Type: application/json\n\n")

# Import all necessary modules

import pandas as pd
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from datetime import datetime
import json
import os

json_response = {'tables': {}, 'analyses': {}}


# Ensure uploads path is there

image_path = '../../CPS5721/NFL/charts'
if not os.path.exists(image_path):
    pass
    os.makedirs(image_path)


### Initialize DB connection

mydb = mysql.connector.connect(host="imc.kean.edu", user="fisheral", password="1117936")
cursor = mydb.cursor(dictionary = True, buffered = True)

query = "use 2023S_patpanka;"
cursor.execute(query)


json_response['tables']['InjuryRecord'] = {'count': 0, 'data': []}
json_response['tables']['PlayList'] = {'count': 0, 'data': []}
json_response['tables']['PlayerTrackData'] = {'count': 0, 'data': []}
# Get the count of records for each table in dataset

InjuryRecord_count = 105
"""
query = "SELECT count(*) as count from InjuryRecord"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    InjuryRecord_count = row['count']
    row = cursor.fetchone()
"""

json_response['tables']['InjuryRecord']['count'] = InjuryRecord_count

PlayList_count = 320734
"""
query = "SELECT count(*) as count from PlayList"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    PlayList_count = row['count']
    row = cursor.fetchone()
"""

json_response['tables']['PlayList']['count'] = PlayList_count

PlayerTrackData_count = 75870897
"""
query = "SELECT count(*) from PlayerTrackData2 limit 5"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    PlayerTrackData_count = row['count']
    row = cursor.fetchone()
"""

json_response['tables']['PlayerTrackData']['count'] = PlayerTrackData_count


### Get first five records of each table in dataset

InjuryRecord_head = []
query = "SELECT * from InjuryRecord limit 5"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    InjuryRecord_head.append(row)
    row = cursor.fetchone()

json_response['tables']['InjuryRecord']['data'] = InjuryRecord_head

PlayList_head = []
query = "SELECT * from PlayList limit 5"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    PlayList_head.append(row)
    row = cursor.fetchone()

json_response['tables']['PlayList']['data'] = PlayList_head

PlayerTrackData_head = []
query = "SELECT * from PlayerTrackData2 limit 5"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    PlayerTrackData_head.append(row)
    row = cursor.fetchone()

json_response['tables']['PlayerTrackData']['data'] = PlayerTrackData_head


### DATA PREPROCESSING ###

# Get all playkeys for plays where injuries occurred

injury_plays = []
query = "SELECT PlayKey from InjuryRecord where PlayKey order by rand()"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    injury_plays.append(row['PlayKey'])
    row = cursor.fetchone()

# Get as many playkeys for sample plays where injuries did not occur as there are samples for injury plays

non_injury_plays = []
query = "SELECT PlayKey from Non_Injured_Samples"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    non_injury_plays.append(row['PlayKey'])
    row = cursor.fetchone()


### DATA ANALYSIS 

# ## Max Speed
# ##### Null hypothesis: There is no correlation between max speed of player and injury occurrence
# ##### Alternative hypothesis: There is a positive correlation between having a higher max speed and the probability of injury occurrence


# Get max_speed of plays where injury occurred

injury_max_speeds = []
for play in injury_plays:
    query = "SELECT injury_play_max_speed as max_speed from InjuredPlayerData2 where PlayKey = '" + play + "'"
    cursor.execute(query)
    injury_max_speeds.append(cursor.fetchone()['max_speed'])

# Get max_speed of plays where injury did not occur

non_injury_max_speeds = []
for play in non_injury_plays[:len(injury_plays)]:
    query = "SELECT max(s) as max_speed from Non_Injured_Player_Track_Data2 where PlayKey = '" + play + "'"
    cursor.execute(query)
    non_injury_max_speeds.append(cursor.fetchone()['max_speed'])


injury_max_speeds = np.array(injury_max_speeds)
non_injury_max_speeds = np.array(non_injury_max_speeds)

mean_injury_max_speed = np.mean(injury_max_speeds)
mean_non_injury_max_speed = np.mean(non_injury_max_speeds)


# Calculate variance function
def variance(data):
    # Number of observations
    n = len(data)
    # Mean of the data
    mean = sum(data) / n
    # Square deviations
    deviations = [(x - mean) ** 2 for x in data]
    # Variance
    variance = sum(deviations) / n
    return variance


import scipy.stats as stats

# Create a binary variable indicating if the play caused an injury or not
injury = [1] * len(injury_max_speeds) + [0] * len(non_injury_max_speeds)

# Perform the Pearson correlation test
correlation, p_value = stats.pearsonr(injury, np.concatenate((injury_max_speeds, non_injury_max_speeds)))


json_response['analyses']['max_speed'] = {"correlation_coefficient": correlation, "p_value": p_value}


# ### Conclusion:
# #### Because the p-value is below the significance value of 0.05, we can accept the alternative hypothesis that there is a correlation between a player's max speed during a play and the probability of an injury occuring.

# Plot max speed comparison

x = injury_max_speeds
y = non_injury_max_speeds

plt.hist(x, alpha=0.5, bins=range(0, 13), label='Injury-causing plays')
plt.hist(y, alpha=0.5, bins=range(0, 13), label='Non-injury-causing plays')
plt.legend(loc='upper right')
plt.xlabel("Player's max speed during a play (yards per second)")
plt.ylabel("Frequency")
plt.title("Comparison of max speed of player during injury and non-injury causing plays")
figure_name = "max_speed_hist.png"
plt.savefig(os.path.join(image_path, figure_name))
json_response['analyses']['max_speed']['figure_name'] = figure_name
plt.clf()

# ## Field types
# ##### Null hypothesis: There is no correlation between field type and the probability of an injury occuring.
# ##### Alternative hypothesis: There is a correlation between field type and the probability of an injury occuring.

# Data gathering


injury_field_types = []
query = "select Surface from InjuryRecord"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    field_type = row['Surface']
    injury_field_types.append(field_type)
    row = cursor.fetchone()


# Get field types from 5000 random plays

population_field_types = []
query = "select FieldType from PlayList order by rand() limit 5000"
cursor.execute(query)
row = cursor.fetchone()
while row is not None:
    field_type = row['FieldType']
    population_field_types.append(field_type)
    row = cursor.fetchone()


# Print ratios for population and injury sample

population_field_types = pd.DataFrame(population_field_types)
injury_field_types = pd.DataFrame(injury_field_types)

population_table = pd.crosstab(index=population_field_types[0], columns="count")
injury_table = pd.crosstab(index=injury_field_types[0], columns="count")

population_field_types_ratio = population_table / len(population_field_types)

observed = injury_table
expected = population_field_types_ratio * len(injury_field_types)


chi_squared_stat = (((observed-expected)**2)/expected).sum()


crit = stats.chi2.ppf(q = 0.95, # Find the critical value for 95% confidence
                     df = 1) # DF = number of variable categories - 1

p_value = 1 - stats.chi2.cdf(x = chi_squared_stat, df = 1)

json_response['analyses']['field_type'] = {"critical_value": crit, "p_value": float(p_value)}

# PLOT THE FINDINGS

X = ['Natural', 'Synthetic']
  
X_axis = np.arange(len(X))
  
plt.bar(X_axis - 0.2, expected.values.ravel().astype(int), 0.4, label = 'Expected value')
plt.bar(X_axis + 0.2, observed.values.ravel().astype(int), 0.4, label = 'Observed value')
  
plt.xticks(X_axis, X)
plt.xlabel("Field Type")
plt.ylabel("Number of plays that caused injuries")
plt.title("Comparison of injuries on natural or synthetic fields")
plt.legend()
plt.show()
figure_name = "field_type_ratios.png"
plt.savefig(os.path.join(image_path, figure_name))
json_response['analyses']['field_type']['figure_name'] = figure_name
plt.clf()

### BOXPLOT OF PLAY LENGTH

try:
    conn = mysql.connector.connect(
        host="imc.kean.edu",
        user="patpanka",
        password="1129006",
        database="2023S_patpanka"
    )

    if conn.is_connected():
        
        maxSpeed_nonInjured_arr = np.empty(0);
        maxSpeed_injured = np.empty(0)
        data = np.empty(0)

        cursor = conn.cursor(buffered= True)
        cursor.execute("SELECT MAX(time) FROM 2023S_patpanka.Non_Injured_Player_Track_Data niptd GROUP BY PlayKey")

        cursor2= conn.cursor(buffered= True)
        cursor2.execute ("SELECT MAX(time) FROM 2023S_patpanka.test GROUP BY PlayKey")

        result_non_injured = cursor.fetchall()
        result_injured = cursor2.fetchall()

        for row in result_non_injured:
            maxSpeed_nonInjured_arr  = np.append(maxSpeed_nonInjured_arr, row)

        for row2 in result_injured:
            maxSpeed_injured = np.append(maxSpeed_injured, row2)

        data =  [maxSpeed_injured, maxSpeed_nonInjured_arr]
        
      
        boxplot = plt.boxplot(data)
        plt.title("Play Length of Injured and Non Injured Players")
        plt.ylabel("Play Length in Seconds")
        plt.xlabel("Category")
        plt.xticks([1,2], ["Injured Players", "Non Injured Players"])
        
                
        median_injured = np.median(maxSpeed_injured)
        median_noninjured = np.median(maxSpeed_nonInjured_arr)

        json_response['analyses']['play_length'] = {"median_injured": median_injured, "median_noninjured": median_noninjured}
        
        # show plot
        figure_name = "play_length_boxplot.png"
        plt.savefig(os.path.join(image_path, figure_name))
        json_response['analyses']['play_length']['figure_name'] = figure_name
        plt.clf()

except mysql.connector.Error as e:
    print(json.dumps({'error': 'could not connect to db'}))


print(json.dumps(json_response))