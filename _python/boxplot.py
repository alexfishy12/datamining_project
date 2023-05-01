#!/usr/bin/python3
# Import all necessary modules
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import json
import os

print("Content-Type: application/json\n\n")

image_path = '../uploads'
if not os.path.exists(image_path):
    pass
    os.makedirs(image_path)

mydb = mysql.connector.connect(host="imc.kean.edu", user="fisheral", password="1117936")
cursor = mydb.cursor(dictionary = True, buffered = True)

json_response = {}

query = "use 2023S_fisheral;"
cursor.execute(query)

# Question 6

query = "select * from County where home_value is not null and education_college_or_above is not null;"
cursor.execute(query)
rows = cursor.fetchall()

home_values = np.array([])
for row in rows:
    home_values = np.append(home_values, row['home_value'])

fig = plt.figure(figsize=(6, 8))

plt.boxplot(home_values.tolist())
plt.title("County home values")
plt.ylabel("Value (Millions of US dollars)")
plt.show()
plt.savefig(os.path.join(image_path, 'boxplot.png'))

median = np.nanmedian(home_values)
q1 = np.nanquantile(home_values, 0.25)
q3 = np.nanquantile(home_values, 0.75)
IQR = q3 - q1
Q6lower = q1 - IQR * 1.5
Q6upper = q3 + IQR * 1.5
outlier_counties = []
outlier_home_values = []

for row in rows:
    if row['home_value'] > Q6upper or row['home_value'] < Q6lower:
        outlier_counties.append([row['state'], row['county']])
        outlier_home_values.append(row['home_value'])

json_response['Q6'] = {
    'image_path': os.path.join(image_path, 'boxplot.png'),
    "data": {
        "lower": Q6lower,
        "upper": Q6upper,
        "median": median,
        "quartile_1": q1,
        "quartile_3": q3,
        "outliers": {
            'counties': outlier_counties,
            'home_values': outlier_home_values
        }
    }
}

# get outliers for Q6
query = "select * from County where home_value is not null and education_college_or_above is not null and (home_value < " + str(Q6lower) + "or home_value > " + str(Q6upper) + ");"
cursor.execute(query)
Q6_outliers = cursor.fetchall()

# get states with most outliers from Q6
query = "select state, count(*) as count from County where home_value is not null and education_college_or_above is not null and (home_value < " + str(Q6lower) + " or home_value > " + str(Q6upper) + ") group by state order by count(*) desc limit 5;"
cursor.execute(query)
Q6_most_outliers = cursor.fetchall()

# Question 7

education_college_or_above = np.array([])
for row in rows:
    education_college_or_above = np.append(education_college_or_above, row['education_college_or_above'])

fig = plt.figure(figsize=(6, 8))

plt.boxplot(education_college_or_above.tolist())
plt.title("% of county population with college education")
plt.ylabel("Percentage of population")
plt.show()
plt.savefig(os.path.join(image_path, 'boxplot1.png'))

median = np.nanmedian(education_college_or_above)
q1 = np.nanquantile(education_college_or_above, 0.25)
q3 = np.nanquantile(education_college_or_above, 0.75)
IQR = q3 - q1
Q7lower = q1 - IQR * 1.5
Q7upper = q3 + IQR * 1.5

outlier_counties = []
outlier_education = []

for row in rows:
    if row['education_college_or_above'] > Q7upper or row['education_college_or_above'] < Q7lower:
        outlier_counties.append([row['state'], row['county']])
        outlier_education.append(row['education_college_or_above'])

json_response['Q7'] = {
    'image_path': os.path.join(image_path, 'boxplot1.png'),
    "data": {
        "lower": Q7lower,
        "upper": Q7upper,
        "median": median,
        "quartile_1": q1,
        "quartile_3": q3,
        "outliers": {
            'counties': outlier_counties,
            'education': outlier_education
        }
    }
}

# get outliers for Q7
query = "select * from County where home_value is not null and education_college_or_above is not null and (education_college_or_above < " + str(Q7lower) + " or education_college_or_above > " + str(Q7upper) + ");"
cursor.execute(query)
Q7_outliers = cursor.fetchall()

# get states with most outliers from Q7
query = "select state, count(*) as count from County where home_value is not null and education_college_or_above is not null and (education_college_or_above < " + str(Q7lower) + " or education_college_or_above > " + str(Q7upper) + ") group by state order by count(*) desc limit 5;"
cursor.execute(query)
Q7_most_outliers = cursor.fetchall()

# get outliers for both plots
query = "select * from County where home_value is not null and education_college_or_above is not null and (home_value > " + str(Q6upper) + " or home_value < " + str(Q6lower)  + ") and (education_college_or_above < " + str(Q7lower) + " or education_college_or_above > " + str(Q7upper) + ");"
cursor.execute(query)
both_outliers = cursor.fetchall()

# get states with most outliers from intersection of both plots
query = "select state, count(*) as count from County where home_value is not null and education_college_or_above is not null and (education_college_or_above < " + str(Q7lower) + " or education_college_or_above > " + str(Q7upper) + ") and (home_value < " + str(Q6lower) +" or home_value > " + str(Q6upper) + ") group by state order by count(*) desc limit 5;"
cursor.execute(query)
both_most_outliers = cursor.fetchall()


json_response['outliers'] = {
    "Q6": Q6_outliers,
    "Q6_most_outliers": Q6_most_outliers,
    "Q7": Q7_outliers,
    "Q7_most_outliers": Q7_most_outliers,
    "both": both_outliers,
    "both_most_outliers": both_most_outliers
}

print(json.dumps(json_response))