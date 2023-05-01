# Import all necessary modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from datetime import datetime
import json
import mysql.connector
import os

# Import all necessary modules

print("Content-Type: application/json\n\n")

image_path = '../uploads'
if not os.path.exists(image_path):
    pass
    os.makedirs(image_path)

mydb = mysql.connector.connect(host="imc.kean.edu", user="fisheral", password="1117936")
cursor = mydb.cursor(dictionary = True, buffered = True)

query = "use 2023S_patpanka;"
cursor.execute(query)

# json stoing data for the three analyses
json_response = {
    "num_non-injury_plays": None,
    "num_injury_plays": None,
    "max_speed": {},
    "play_length": {},
    "field_type": {},
} 

# Data preprocessing



# Max Speed


# 