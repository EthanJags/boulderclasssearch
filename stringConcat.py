import requests

with open('filename.txt', 'r') as file:
    contents = file.read()

# URL to send the POST request to
url = 'https://example.com/api'

# Data to be sent in the POST request
data = {
    'key1': 'value1',
    'key2': 'value2'
}

# Optional headers if needed
headers = {
    'Authorization': 'Bearer YOUR_TOKEN_HERE',
    'Content-Type': 'application/json'
}

# Send the POST request
response = requests.post(url, json=data, headers=headers)

# Print the response
print(response.text)
