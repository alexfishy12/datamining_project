#!/usr/bin/python3

# Import all necessary modules
import numpy as np
import mysql.connector
import json

print("Content-Type: application/json\n\n")

mydb = mysql.connector.connect(host="imc.kean.edu", user="fisheral", password="1117936")
cursor = mydb.cursor(dictionary = True, buffered = True)

json_response = {}

query = "use 2023S_fisheral;"
cursor.execute(query)


# Question 1

query = "select * from County;"
cursor.execute(query)
rows = cursor.fetchall()

json_response['Q1'] = {"html_table": "", "query": query, "numrows": cursor.rowcount}
json_response['Q1']['html_table'] = "<div class='table'><table border=1>"
json_response['Q1']['html_table'] += "<tr><th>state<th>county<th>income<th>population<th>home_value<th>education_college_or_above"

for row in rows:
    json_response['Q1']['html_table']  += "<tr><td>" + str(row['state']) + "<td>" + str(row['county']) + "<td>" + str(row['income']) + "<td>" + str(row['population']) + "<td>" + str(row['home_value']) + "<td>" + str(row['education_college_or_above'])

json_response['Q1']['html_table'] += "</table></div>"


# Question 2

query = "select * from County where income is not null and education_college_or_above is not null;"
cursor.execute(query)
rows = cursor.fetchall()

data = []
for row in rows:
    data.append([row['income'], row['education_college_or_above']])
    

json_response['Q2'] = {
    "title": "Income and percentage of population with college education or higher",
    "x_label": "Income (USD)",
    "y_label": "% college educated or higher",
    "data": data
}

# Question 3

data = [
    ["<20", 0],
    ["20-40", 0],
    ["40-60", 0],
    ["60-80", 0],
    ["80-100", 0],
    [">100", 0],    
]
for row in rows:
    income = row['income']
    if income < 20000:
        data[0][1] += 1 
    elif income >= 20000 and income < 40000:
        data[1][1] += 1 
    elif income >= 40000 and income < 60000:
        data[2][1] += 1
    elif income >= 60000 and income < 80000:
        data[3][1] += 1 
    elif income >= 80000 and income < 100000:
        data[4][1] += 1
    elif income >= 100000:
        data[5][1] += 1

json_response["Q3"] = {
    "title": "Number of counties in each income range",
    "x_label": "Average income of county ($20k intervals)",
    "y_label": "Number of counties",
    "data": data
}

# Question 4

data = [
    ["<20", 0],
    ["20-40", 0],
    ["40-60", 0],
    ["60-80", 0],
    ["80-100", 0],
    [">100", 0],    
]
for row in rows:
    income = row['income']
    population = row['population'] * (row['education_college_or_above'] / 100)
    if income < 20000:
        data[0][1] += population
    elif income >= 20000 and income < 40000:
        data[1][1] += population
    elif income >= 40000 and income < 60000:
        data[2][1] += population
    elif income >= 60000 and income < 80000:
        data[3][1] += population
    elif income >= 80000 and income < 100000:
        data[4][1] += population
    elif income >= 100000:
        data[5][1] += population

   
json_response["Q4"] = {
    "title": "Population of college educated individuals in each income range",
    "x_label": "Average income of county ($20k intervals)",
    "y_label": "Population of college educated individuals",
    "data": data
}


# Question 5

print(json.dumps(json_response))