import re
from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
from selenium.webdriver.chrome.options import Options
import sys
import requests
import json

def postRequest(url, body):
    # Path: postRequest.py    
    # URL to send the POST request to

    # Data to be sent in the POST request
    # bodyinit = "%7B%22group%22%3A%22code%3A"

    # department = ""

    # percent = "%"
    
    # body = bodyinit + department + percent + 
    
    # APRD 2001 
    # %7B%22group%22%3A%22code%3AAPRD%202001%22%2C%22key%22%3A%22crn%3A21777%22%2C%22srcdb%22%3A%222237%22%2C%22matched%22%3A%22crn%3A21777%22%7D
    # APRD 1004
    # %7B%22group%22%3A%22code%3AAPRD%201004%22%2C%22key%22%3A%22crn%3A21785%22%2C%22srcdb%22%3A%222237%22%2C%22matched%22%3A%22crn%3A21785%22%7D
    # ACCT 3220
    # %7B%22group%22%3A%22code%3AACCT%203220%22%2C%22key%22%3A%22%22%2C%22srcdb%22%3A%222237%22%2C%22matched%22%3A%22crn%3A19089%2C19090%2C19091%2C19092%2C19093%2C19094%2C19095%2C19096%2C19097%22%7D
    # %7B%22group%22%3A%22code%3AACCT%203220%22%2C%22key%22%3A%22%22%2C%22srcdb%22%3A%222237%22%2C%22matched%22%3A%22crn%3A19089%2C19090%2C19091%2C19092%2C19093%2C19094%2C19095%2C19096%2C19097%22%7D
    # ACCT 3230
    # %7B%22group%22%3A%22code%3AACCT%203230%22%2C%22key%22%3A%22%22%2C%22srcdb%22%3A%222237%22%2C%22matched%22%3A%22crn%3A40118%2C19098%2C19099%22%7D    
    # ASEN 1009
    # %7B%22group%22%3A%22code%3AASEN%201009%22%2C%22key%22%3A%22crn%3A23624%22%2C%22srcdb%22%3A%222237%22%2C%22matched%22%3A%22crn%3A23624%22%7D
    
    # Optional headers if needed
    #headers = {
    #    'Authorization': 'Bearer YOUR_TOKEN_HERE',
    #    'Content-Type': 'application/json'
    #}

    # Send the POST request
    #response = requests.post(url, data=body, headers=headers)
    response = requests.post(url, data=body);
    response = response.json()
    # data = s(response)
    hours = (response["credit_html"])
    code = (response["code"])
    title = (response["title"])
    description = (response["description"])
    instmode = (response["instmode_html"])
    instructorparse = (response["instructor_info_html"])
    # Regular expression pattern to match the name inside the anchor tag
    pattern = r">(.+)<"

    # Use re.search to find the name within the anchor tag
    match = re.search(pattern, instructorparse)

    # Check if a match is found and extract the name from the first capturing group
    if match:
        instructor = match.group(1) # Output: "Harsha Gangadharbatla"
    else:
        instructor = "Name not found."

    dates = (response["dates_html"])
    eval_links = (response["eval_links"])
    regreq = (response["restrict_info"])

    # Regular expression pattern to extract the link
    pattern  = r"<a\s+href=\"(https://[^\"]+)\""

    # Find the first match
    match = re.search(pattern, eval_links)

    if match:
        eval = match.group(1)  # Extract the link from the match
    else:
        print("No link found.")
    
    #sections = response["allInGroup"]
    #for section in sections

    writer.writerow([code, title, hours, description, instmode, instructor, dates, regreq, eval])
    file.flush()
        # Print the response
    print(code, title, hours, description, instmode, instructor, dates, regreq, eval)

    
with open('message.txt', 'r') as file:
    contents = file.read()

file = open("CUScrape.csv", "w", newline='')
writer = csv.writer(file)
writer.writerow(["Class Code", "Class Name", "Credit Hours", "Class Description", "Instruction Mode", "Instructor(s)", "Dates", "Registration Requirements", "Class Evaluation Link"])

url = "https://courses.yale.edu/api/?page=fose&route=details"

contents = json.loads(contents)
courses = contents["results"]
classCode = "ACCT 3220"
number = 0
for course in courses:
    if classCode == course["code"]:
        continue
    classCode = (course["code"])
    parts = classCode.split()
    department = parts[0]
    crn = (course["crn"])
    srcdb = "5037"

    bodyTemplate = f'%7B%22group%22%3A%22code%3A{department}%20{classCode}%22%2C%22key%22%3A%22crn%3A{crn}%22%2C%22srcdb%22%3A%22{srcdb}%22%2C%22matched%22%3A%22crn%3A{crn}%22%7D'
    number = number + 1
    print(number)
    postRequest(url, bodyTemplate) # Input generic url and POST body into postRequest function


